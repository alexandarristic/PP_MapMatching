# PP_MapMatching
Post-processing map matching script developed with ArcPy

---
**Introduction**

   Post-processed Map Matching describes the task of matching a user’s  existing trajectories  recorded from a GPS unit to appropriate roads/links in a transportation network. Typically planar networks which treat streets and intersections as distinct points and lines are used to model such tasks due to computational efficiency, yet such a simple format prevents actionable information from being derived due to an absence of topology and connnectivity. 
  
  Thus, the only suitable alternative is a route-based analysis within ESRI's ArcGIS platform that treats the first and last points as the origin and destination of a trip and derives a path from the intermediate recordings. Such a task is easy to perform but is tedious and is therefore an ideal canditate for automation via Python 2.7 and the ArcPy site package.
  
---
**Data included in the ZIP file**

1. A single CSV file titled SampleRoute.csv containing 431 records representing travel from Parkplaza Dr. to Rockway Ct
2. A selected portion of CanMap’s Content Suite representing a network dataset for the City of Hamilton.
3. A file called MapMatch.py containing the script.
4. An ArcGIS Toolbox which implements the script. 
