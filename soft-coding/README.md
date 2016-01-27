# Sewer Maintenance soft-coding
## Configuration instructions
This script utilizes the ArcPy functions.  Shapefiles, layers, and attribute names will need to be adjusted to reflect the user’s data. 
The script is set up to be used in an ArcGIS toolbox.  Before you use the script it will need to be saved to an ArcGIS toolbox.  

###Step 1. Create toolbox
If you do not already have a personal tool box you will need to add one.  In AcrMap or ArcCatalog go to the AcrToolbox window. 

![Picture1](https://farm2.staticflickr.com/1707/24436856032_cd8a5ac8fd_z.jpg)

Right click on the white space and select Add Toolbox…

![Picture2](https://farm2.staticflickr.com/1675/24249608550_fab494a1bc_z.jpg)

This opens the browsing dialog box.  If you have a pre-existing toolbox you can add it to your map this way or brows to the location where you would like your toolbox to be stored and create a new toolbox in this location.  Use the create toolbox button at the top right hand corner of the dialog box and name the file something unique to you. 

![Picture3](https://farm2.staticflickr.com/1479/24436855852_611c22b62c_b.jpg)

###Step 2. Add script to toolbox
To add the script as a tool that can be used like any other tool in ArcMap right click on the appropriate toolbox.  Navigate to Add, hovering over Add will bring up more option.  Click on Script.  

![Picture4](https://farm2.staticflickr.com/1527/24545150075_0a9bd0c906_z.jpg)

The dialog box will allow you to name the script and provide descriptive information that can be used to remind you and others in your organization what this script does.   Keep the name short and the other boxes are optional.  Once you have filled out the first three boxes to your satisfaction hit next.  (I have had problems with names with spaces, underscored, or longer than 8 characters.) 

![Picture5](https://farm2.staticflickr.com/1678/23918350863_526d5618c3_z.jpg)

This dialog box allows you to associate the script obtained from this Git with your toolbox.  Click on the folder browser button.

![Picture6](https://farm2.staticflickr.com/1660/24177535589_9ae8b43e6a_z.jpg)

 Go to the location where you saved the script from this Git and open the script.  This will return you to the Add Script window where you may hit next. 

![Picture7](https://farm2.staticflickr.com/1476/24437009522_404487fb91_z.jpg)

This next window is very important.  The names that are input will be displayed in the gui tool when accessed through the toolbox to guide users on what information to input. 

![Picture8](https://farm2.staticflickr.com/1480/23919744373_f12210d3f3_z.jpg)

The data type column provides a dropdown box with a large number of choices on the type of data that the code should be interacting with. 

![Picture9](https://farm2.staticflickr.com/1694/24251313160_84e634fb4b_z.jpg)

It is important that the display names and the data types are in the same order that they are called in the script found on this git.  Feel free to make the display names fit your data. 

| Index | Display Name | Data Type | Direction | Filter | Obtained from |
|*------|*------------*|*---------*|*---------*|*------*|*-------------*|
| 0     | Workspace    | Workspace | Input     | I used File System |   |
| 1     | Sewer Lines  | Feature Layer | Input | Polyline |             |
| 2     | All work order points | Feature Layer | Input | Point |       |
| 3     | Streams      | Feature Layer | Input | Polyline |             |
| 4     | MAJOR ROADS  | Feature Layer | Input | Polyline |             |
| 5     | Parcels      | Feature Layer | Input | Polygon |              |
| 6     | ROUTINE MAINTENANCE | Feature Layer | Input | Polyline |      |
| 7     | Sewer Diameter Field | Field | Input |        | Sewer Lines   |
| 8     | Sewer Diameter Field | Field | Input |        | Sewer Lines   |
| 9     | Largest Sewer Diameter | String | Input |     |               | 
| 10    | Select the STOP WO| SQL Expression | Input |  | work order    |
| 11    | Select SSO WO | SQL Expression | Input |      | work order    |
| 12    | Select commercial and residential parcels | SQL Expression | Input |  | Parcels |
| 13    | Risk         | File      | Output    | shp    |               |




## A file manifest (list of files included)
## Copyright and licensing information
The MIT License (MIT)
Copyright (c) 2015 City of Bryan Water Department
## Contact information for the distributor or programmer
Elizabeth Rentschlar
## Known bugs
The hot spot analysis will break the script if run inside of ArcMap.  
## Troubleshooting
## Credits and acknowledgments
