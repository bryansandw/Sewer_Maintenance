#############################################################################
# Name: Elizabeth Rentschlar                                                #
# Purpose: Sewer Maintenance based on Risk Prioritization                   #
# Created: 1/22/2016                                                        #
# Copyright: (c) City of Bryan                                              #
# ArcGIS Version: 10.2.2                                                    #
# Python Version: 2.7                                                       #
#############################################################################

# Set the necessary product code
# import arcinfo
from arcpy import env
import arcpy
#import datetime
#import numpy
env.overwriteOutput = True
env.autoCancelling = False

## This is important! Where all of the outputs are saved! 
env.workspace = arcpy.GetParameterAsText(0)

##### Local variables: #####
Risk_shp = arcpy.GetParameterAsText(1) 
MH = arcpy.GetParameterAsText(2) 
#May not use
maint = env.workspace + "\\Maintenance.lyr"
target_MH = env.workspace + "\\target_MH.shp"
map_output_folder = env.workspace + "\\Maps\\"
map = arcpy.mapping.MapDocument("CURRENT") #env.workspace + "\\Sewer2.mxd"
#single_MH_lyr = env.workspace + "\\single_MH.shp"
high_risk_lines = env.workspace + "\\high_risk_lines.shp"
risky_line = env.workspace + "\\Target_Line.shp"

risk_list = []
cur = arcpy.SearchCursor(Risk_shp)
for cur1 in cur:
    risk_list.append(cur1.Risk)
del cur

arcpy.SetProgressorLabel("Sort list of the risk values to identify the " + \
    "highest risk lines")
# Sort list of the risk values to identify the highest risk lines
sorted_risk = sorted(risk_list, reverse = True)
# Identify the 10th highest risk value
place_ten = sorted_risk[9]

arcpy.SetProgressorLabel("Process: Make Layer where the risk is the same " + \
    "or greater than the tenth highest list value")
# Define where clause that the Risk is greater than or equal to the 10th
# risk value
where_clause = "\"Risk\" >= " + str(place_ten)
# Make layer of the SS lines that are greater than or equal to the 10th
# risk value
arcpy.MakeFeatureLayer_management(Risk_shp, "High_Risk_lyr", where_clause)
# Copy the layer to make it a feature that process may be run on
arcpy.CopyFeatures_management("High_Risk_lyr", high_risk_lines)

arcpy.SetProgressorLabel("Process: Make Layer where the Manholes are adjacent to the high risk sewer lines")
# Create layer version of manholes
arcpy.MakeFeatureLayer_management(MH, "MH_lyr")
# Select the manholes that intersect with the high risk sewer lines
arcpy.SelectLayerByLocation_management("MH_lyr", "INTERSECT",
    "High_Risk_lyr")
# Copy the selected Manholes as their own feature 
arcpy.CopyFeatures_management("MH_lyr", target_MH)

arcpy.SetProgressorLabel("Create a Update Cursor to select the lines")
risky_lines = arcpy.SearchCursor(high_risk_lines)
date = str(datetime.date.today())
rline_FID_list =[]

for line in risky_lines:
    rline_FID_list.append(line.FID)
del risky_lines
print rline_FID_list

arcpy.SetProgressorLabel("Set up map document environment to create exported map documents as pdfs in map folder")

#print slyr.symbology
#print slyr.symbologyType
#print slyr
#styleItem = arcpy.mapping.ListStyleItems("USER_STYLE", "Legend Items")#[0] 
#print styleItem

'''
for FID in rline_FID_list:
    where_clause2 = "\"FID\" = " + str(FID) + ""
    print where_clause2
    single_risky_line = risky_line  #+ str(FID) + ".shp" 
    arcpy.Select_analysis(high_risk_lines, single_risky_line, where_clause2)
    arcpy.MakeFeatureLayer_management(maint, "maint_lyr")
    arcpy.SelectLayerByLocation_management("maint_lyr", "INTERSECT", 
        single_risky_line)

    maintDis = arcpy.SearchCursor("maint_lyr")
    for m in maintDis:
        district = m.District
	#newlayer = arcpy.mapping.Layer(single_risky_line)
    #arcpy.mapping.AddLayer(data_frame, newlayer,"BOTTOM")
	
    mapdoc = arcpy.mapping.MapDocument(map)

    # need to loop through the target MH
    # May need to loop through based on the FID value???
    print "exporting maps"
    #Data Frame 
    data_frame = arcpy.mapping.ListDataFrames(mapdoc)[0]
    print data_frame.name
    print data_frame.scale
    scale = data_frame.scale

    legend = arcpy.mapping.ListLayoutElements(mapdoc, "LEGEND_ELEMENT",
        "Legend")[0]
    legend.autoAdd = True
    for text in arcpy.mapping.ListLayoutElements(mapdoc, "TEXT_ELEMENT"):
        if text.text == "Text":
            text.text = district + "\n" + date
		

    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()


    wildcard = "Target Line" #+ str(FID)
    print wildcard
    print arcpy.mapping.ListLayers(mapdoc)
    try:
        lyr = arcpy.mapping.ListLayers(mapdoc, wildcard)[0]
        print lyr
        data_frame.extent = lyr.getExtent(True)
        arcpy.RefreshActiveView()     	
	
        print data_frame.extent
 
        scale = data_frame.scale
        print data_frame.scale
	
        # Don't really need this.... 
        # Need to find a way to change the scale to be 
        # proportionate to length of line	
        if scale < 500.00:
            new_scale = 500.00
        elif scale > 500.00 and scale < 1000.00:
            new_scale = 1000.00
        elif scale > 1000.00 and scale < 1500.00:
            new_scale = 1500.00		
        elif scale > 1500.00 and scale < 2000.00:
            new_scale = 2000.00		
        elif scale > 2000.00 and scale < 2500.00:
            new_scale = 2500.00
        elif scale > 2500.00 and scale < 3000.00:
             new_scale = 3000.00		
        elif scale > 3000.00 and scale < 3500.00:
             new_scale = 3500.00
        else:
            new_scale = data_frame.scale
        
        data_frame.scale = new_scale
        print data_frame.scale	
		
        arcpy.RefreshActiveView()     		
	    
		#Improve naming convention?
        map_output = map_output_folder + str(FID) + "_" + date + ".pdf"
        arcpy.mapping.ExportToPDF(mapdoc, map_output)		
        print "Created Map for " + wildcard + " " + str(FID + 1)
        
        #arcpy.Delete_management(data_frame, single_risky_line)
		
        del mapdoc
    except:
        print "Could not find " + wildcard
'''
