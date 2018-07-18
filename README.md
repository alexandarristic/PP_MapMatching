# PP_MapMatching
Post-processing map matching script developed with ArcPy

---
## Introduction

&nbsp; &nbsp; Post-processed Map Matching describes the task of matching a user’s  existing trajectories  recorded from a GPS unit to appropriate roads/links in a transportation network. Typically planar networks which treat streets and intersections as distinct points and lines are used to model such tasks due to computational efficiency, yet such a simple format restricts actionable information from being derived due to an absence of spatial relationships(topology) and connnectivity. Such models particularily fail in specific regions such as cloverleaf interchanges (see below) due to these issues, and thus a network model that implements such considerations is vital.
  
  ![cloverleaf_interchange](https://qph.fs.quoracdn.net/main-qimg-c373337d25adbfb36a9b7bad3ef9363b)
  
  
&nbsp; &nbsp; ESRI's shortest route algorithm can serve as a suitable model. In this algorithm, the beginning (origin) and ending (destination) points/nodes are associated with appropriate roads/links provided in a network dataset (CanMap for this case) in a topologically coherent manner, and a path that minimizes travel cost while considering imposed barriers and restrictions to travel is derived. Further, any intermediate points can be used to constrain the derived path so that it acurately mimics the user's recorded trajectories (see methodology for more details). Although such a task is trivial, it can be tedious to implement and thus is an ideal candidate for automation using Python and the ArcPy site package.  

---
## Data included in the ZIP file

1. A single CSV file titled SampleRoute.csv containing 431 records representing travel from Parkplaza Dr. to Rockway Ct
2. A selected portion of CanMap’s Content Suite representing a network dataset for the City of Hamilton.
3. A file called **MapMatch.py** containing the script.
4. An ArcGIS Toolbox which implements the script. 

---
## Methodology

### Logic

&nbsp; &nbsp; Earlier, it was alluded to that the intermediate transit points can be used to constrain the resulting route ESRI's route algorithm provides. However, it is impracticle and memory intensive to load all points when solving a route and so it would be better to treat these points as a restriction. If such points were converted to a line and buffered to account for horizontal dilution of precision (HDOP; essentially GPS error), this region could be intersected with the network dataset to create a set of point restrictions to travel. Such an approach would be exponentially less memory intensive and would increase processing efficiency.

 ### Trajectories
 
&nbsp; &nbsp; In most cases, GPS trajectories from common units like Garmin, TomTom and DeLorme can be exported as comma seperated value (CSV) files which typically contain some point ID, waypoint name, and an associated latitude and longitude. These files can be iterated over to dervive a point shapefile for each longitude/latitude (x,y) tuple which will later be reprojected to align with CanMap's network dataset coordinate system (NAD 1983 UTM Zone 17N for Hamilton). 
  
 ### Point to Line conversion, buffering and intersection 
 
&nbsp; &nbsp; The earlier points were seperated into 2 datasets: one for the trip origin and destination and the other for intermediate points. The intermediate points were converted to lines using the built-in points to line tool. Following this, the lines were buffered by some user-specified distance which was restricted to be about 5-6 times HDOP (about 50-60 meters) to allow for accurate matching (according to Dalumpines, R. and Scott,D.M (2011)).  
&nbsp; &nbsp; This polygonal region was then intersected with CanMap's network dataset to form a series of point restrictions. These were finally fed into the make route layer tool alongside the origin and destination points from earlier to derive the shortest path. This path, which is saved as a layer file, is saved in a user-specified location.
  

 
  
 
 
