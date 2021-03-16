#Post-Processing Map Matching tool by Alexandar Ristic, December 2017. 

#Import necessary modules/site packages
import arcpy,os

#Set Parameters
work = arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True
NetworkDataset = arcpy.GetParameterAsText(1)
HamNetwork = arcpy.GetParameterAsText(2)
BufferDistance = arcpy.GetParameterAsText(3)
RouteName = arcpy.GetParameterAsText(4)


#Output Folder for intermediate data is derived if it does not exist.
scratchfolder = work + "/Scratch"
if not os.path.exists(scratchfolder):    
    os.makedirs(scratchfolder)


#Check if network analyst is available. If so, check out for later else print appropriate message to user.
if arcpy.CheckExtension("Network") == "Available":
        arcpy.CheckOutExtension("Network")
else:
        arcpy.AddError("Network Analyst license is unavailable.")

    
#Part 1 - Making points from each CSV in the user-specified environment.
for csv in arcpy.ListFiles("*.csv"):
    lyr = "CSV_layer"
    outShapeName = arcpy.Describe(csv).baseName + ".shp"
    outPRJNAME = "projected_" + outShapeName #reference this for stops later on.

    #CSVs to Shapefiles conversion.
    arcpy.MakeXYEventLayer_management(csv,"LONG","LAT",lyr,4326) 
    arcpy.FeatureClassToFeatureClass_conversion(lyr,scratchfolder,outShapeName)

    #Reprojecting Shapefiles to NAD 1983 UTM Zone 17N for later.
    arcpy.env.workspace = scratchfolder
    arcpy.Project_management(outShapeName,outPRJNAME,26917)

#Part 2 - Turn points into seperate line FCs. These will be used to make point barriers.
arcpy.env.workspace = scratchfolder
shapeList = [fc for fc in arcpy.ListFeatureClasses("projected_*","Point") if not 'intersect' in fc] #lists only CSV shapefiles.
for shape in shapeList:
    outlineFC = arcpy.Describe(shape).basename + "line.shp"
    arcpy.PointsToLine_management(shape,outlineFC)

#Part 3 - Make point barriers via buffer and intersect with network dataset.
LineFCList = arcpy.ListFeatureClasses("*line","Polyline") + arcpy.ListFeatureClasses("projected_*","Polyline") # This lists all the line FCs made above.
for line in LineFCList:
    outBarriersName = arcpy.Describe(line).baseName + "intersect.shp" #use to reference point barriers.
    outfc = arcpy.Describe(line).baseName + "buffer.shp"
    arcpy.Buffer_analysis(line,outfc,BufferDistance)
    arcpy.Intersect_analysis([HamNetwork,outfc],outBarriersName,"#","#","POINT")
    
   
#Part 4 - Create route analysis layer with proper settings and solve.
stops = outPRJNAME
StopCount = arcpy.GetCount_management(stops)
intCount = int(StopCount.getOutput(0))
lastRow = intCount - 1  #This is used to get the last FID row in the stops shapefile. 

Query = """{0} = 0 or {0} = {1}""".format(arcpy.AddFieldDelimiters(stops,"FID"),lastRow) #Equates to "FID" = 0 or "FID" = N-1, where N = # of rows. This query is used to select origin/destination points.


stopsLayer = arcpy.MakeFeatureLayer_management(stops,"stops.lyr")
selectedStops = arcpy.SelectLayerByAttribute_management("stops.lyr","NEW_SELECTION",Query)
pointBarriers = outBarriersName

Route = arcpy.MakeRouteLayer_na(NetworkDataset,RouteName,"Length","USE_INPUT_ORDER","PRESERVE_BOTH","NO_TIMEWINDOWS","Length","ALLOW_UTURNS","Oneway","NO_HIERARCHY","#","TRUE_LINES_WITH_MEASURES")

arcpy.AddLocations_na(Route,"Stops",selectedStops)
arcpy.AddLocations_na(Route,"Point Barriers",pointBarriers)
arcpy.Solve_na(Route,"SKIP") #Skip invalid locations.


outRouteLayer = arcpy.SaveToLayerFile_management(Route,RouteName,"RELATIVE") #Save route as layer file to user-specified location.
arcpy.AddMessage("Route layer created successfully. Route is located at:" + " " + RouteName)

arcpy.CheckInExtension("Spatial")

