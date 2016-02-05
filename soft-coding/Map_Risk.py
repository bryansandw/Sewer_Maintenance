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
import datetime
#import numpy
env.overwriteOutput = True
env.autoCancelling = False

## This is important! Where all of the outputs are saved! 
env.workspace = arcpy.GetParameterAsText(0)

##### Local variables: #####
Risk_shp = arcpy.GetParameterAsText(1) 
MH = arcpy.GetParameterAsText(2) 
Risk_symbol = arcpy.GetParameterAsText(3)
MH_symbol = arcpy.GetParameterAsText(4)
target_line_symbology = arcpy.GetParameterAsText(5)
#May not use
target_MH = env.workspace + "\\target_MH.shp"
map_output_folder = env.workspace + "\\Maps\\"
high_risk_lines = env.workspace + "\\high_risk_lines.shp"
risky_line = env.workspace + "\\Target_Line.shp"
Risk_copy = env.workspace + "\\Risk_copy.shp"

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

mapdoc = arcpy.mapping.MapDocument("CURRENT")
data_frame = arcpy.mapping.ListDataFrames(mapdoc, "Layers")[0]

# If the user has input a 
if Risk_symbol != '':
    tar_risk_layer = Risk_copy.replace(".shp", ".lyr")
    addRisklayer = arcpy.mapping.Layer(Risk_shp)
    arcpy.mapping.UpdateLayer(data_frame, addRisklayer, arcpy.mapping.Layer(Risk_symbol), True)
    addRisklayer.name = "Line Risk"
    arcpy.mapping.AddLayer(data_frame, addRisklayer,"TOP")
else:
    pass
	
arcpy.SetProgressorLabel("Process: Make Layer where the Manholes are " + \
    "adjacent to the high risk sewer lines")
# Create layer version of manholes

tar_mh_layer = target_MH.replace(".shp", ".lyr")
tar_mh = arcpy.SelectLayerByLocation_management(MH, "INTERSECT",
    high_risk_lines)
tar_mh_feature = arcpy.CopyFeatures_management(tar_mh, target_MH)
MH_layer = arcpy.MakeFeatureLayer_management(tar_mh_feature, tar_mh_layer)
addMHlayer = arcpy.mapping.Layer(tar_mh_layer)

if MH_symbol != '':
    arcpy.mapping.UpdateLayer(data_frame, addMHlayer, arcpy.mapping.Layer(MH_symbol), True)
else:
    pass
if addMHlayer.supports("SHOWLABELS") == True: 
    addMHlayer.showLabels = True
    for lblClass in addMHlayer.labelClasses:
        if lblClass.showClassLabels:
            lblClass.expression = "[LABEL]"
addMHlayer.name = "Target Manholes"
arcpy.mapping.AddLayer(data_frame, addMHlayer,"TOP")

# Select the manholes that intersect with the high risk sewer lines

arcpy.SetProgressorLabel("Create a Update Cursor to select the lines")
risky_lines = arcpy.SearchCursor(high_risk_lines)
date = str(datetime.date.today())
rline_FID_list =[]

for line in risky_lines:
    rline_FID_list.append(line.FID)
del risky_lines
arcpy.SetProgressorLabel(rline_FID_list)

arcpy.SetProgressorLabel("Set up map document environment to create " + \
    "exported map documents as pdfs in map folder")
for FID in rline_FID_list:
    where_clause2 = "\"FID\" = " + str(FID)
    print where_clause2
    single_risky_line = risky_line  #+ str(FID) + ".shp" 
    fc = arcpy.Select_analysis(high_risk_lines, single_risky_line, where_clause2)
    
    lyr_ = risky_line.replace(".shp", ".lyr")
    
    newlayer = arcpy.MakeFeatureLayer_management(fc, lyr_)
    addlayer = arcpy.mapping.Layer(lyr_)
    old_line_name = addlayer.name
    addlayer.name = "Target Line"
    arcpy.mapping.AddLayer(data_frame, addlayer,"AUTO_ARRANGE")
    sym_layer = arcpy.mapping.ListLayers(mapdoc, "Target Line", data_frame)[0]	
    if target_line_symbology != '':
        arcpy.mapping.UpdateLayer(data_frame, sym_layer, arcpy.mapping.Layer(target_line_symbology), True)
    else:
        pass
    legend = arcpy.mapping.ListLayoutElements(mapdoc, "LEGEND_ELEMENT",
        "Legend")[0]
    legend.autoAdd = True    

    #arcpy.RefreshActiveView()
    #arcpy.RefreshTOC()

    fc_cur = arcpy.da.SearchCursor(fc, ['LENGTH', 'SHAPE@X', 'SHAPE@Y'])
    for fc_line in fc_cur:
        line_length = fc_line[0]
        cX = fc_line[1]
        cY = fc_line[2]
    del fc_cur	
    arcpy.SetProgressorLabel(cX)
    arcpy.SetProgressorLabel(cY)
	
    if line_length < 500.00:
         new_scale = 1000.00
    elif line_length > 500.00 and line_length < 1000.00:
         new_scale = 1500.00
    elif line_length > 1000.00 and line_length < 1500.00:
         new_scale = 2000.00
    elif line_length > 1500.00 and line_length < 2000.00:
         new_scale = 2500.00
    elif line_length > 2000.00 and line_length < 2500.00:
         new_scale = 3000.00
    elif line_length > 2500.00 and line_length < 3000.00:
         new_scale = 3500.00
    elif line_length > 3000.00 and line_length < 3500.00:
         new_scale = 4000.00
    else:
         new_scale = line_length + 500
	
    newExtent = data_frame.extent
    newExtent.XMin = cX - (new_scale/2)
    newExtent.XMax = cX + (new_scale/2)
    newExtent.YMin = cY - (new_scale/2)
    newExtent.YMax = cY + (new_scale/2)
    data_frame.extent = newExtent
    data_frame.scale = new_scale	
    arcpy.SetProgressorLabel(data_frame.scale)
		
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
	
	#Improve naming convention?
    map_output = map_output_folder + str(FID) + "_" + date + ".pdf"
    arcpy.mapping.ExportToPDF(mapdoc, map_output)
    remove_layer = arcpy.mapping.ListLayers(mapdoc, "Target Line", data_frame)[0]
    arcpy.mapping.RemoveLayer(data_frame, remove_layer)
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
    arcpy.SetProgressorLabel( "Created Map for " + str(FID + 1) )
del mapdoc
