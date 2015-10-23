#############################################################################
# Name: Elizabeth Rentschlar                                                #
# Purpose: Sewer Maintenance based on Risk Prioritization                   #
# Created: 8/18/15                                                          #
# Copyright: (c) City of Bryan                                              #
# ArcGIS Version: 10.2.2                                                    #
# Python Version: 2.7                                                       #
#############################################################################

# Set the necessary product code
# import arcinfo
from arcpy import env
import arcpy
import datetime
env.overwriteOutput = True
env.autoCancelling = False
env.workspace = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer"

##### Local variables: #####
### Data from Database will only be copied and not altered ###
# Used to use my database connection, but the layers work and this way other
# people should hopefully be able to run the script without having to change
# any of the variables
# Root Directories 
g4 = "G:\\4_LAYERS\\"
sss = g4 + "WATER_SERVICES\\SANITARY SEWER SYSTEM\\"
# This will be used in Process 1
SS_Lines = sss + "COB_SS_LINES (Public).lyr"
# This will be used in Process 2
All_WO = g4 + "COB_HTE_WORK_ORDERS.lyr" 
Streams = g4 + "FEMA\\BRAZOS_FEMA_CREEK_STREAM.lyr"
MAJOR_ROADS = g4 + "BRAZOS_CENTERLINES(MAJOR ROADS).lyr"
BCAD_PARCELS = g4 + "BCAD\\BCAD_PARCELS.lyr"
rm = sss + "COB_SS_ROUTINE_MAINTENANCE.lyr"
MH = sss + "COB_SS_MANHOLES.lyr"

### These are output locations for the files that are created and manipulated
### many will be deleted a the end of the script
Sewer_2_shp = env.workspace + "\\Sewer_2.shp"
WO_STOP_1 = env.workspace + "\\WO_STOP_1.shp"
WO_SSO_1 = env.workspace + "\\WO_SSO_1.shp"
Sewer_SSO_shp = env.workspace + "\\Sewer_SSO.shp"
Sewer_SSO_STOP_shp = env.workspace + "\\Sewer_SSO_STOP.shp"
parcels_select_shp = env.workspace + "\\parcels_select.shp"
low_com_impact = env.workspace + "\\low_com_impact.shp"
mod_com_impact = env.workspace + "\\mod_com_impact.shp"
high_com_impact = env.workspace + "\\high_com_impact.shp"
WO_RM_shp = env.workspace + "\\WO_RM.shp"
SS_buffer_shp = env.workspace + "\\SS_buffer.shp"
low_com_imp_buf = env.workspace + "\\low_com_imp_buffer.shp"
SS_Buffer_HS_shp = env.workspace + "\\SS_Buffer_HS.shp"
Density_Surface = ""
WO_RM_HS_join_shp = env.workspace + "\\WO_RM_HS_join.shp"
Risk_shp = env.workspace + "\\Risk.shp"
#May not use
maint = env.workspace + "\\Maintenance.lyr"
target_MH = env.workspace + "\\target_MH.shp"
map_output_folder = env.workspace + "\\Maps\\"
map = env.workspace + "\\Sewer2.mxd"
#single_MH_lyr = env.workspace + "\\single_MH.shp"
high_risk_lines = env.workspace + "\\high_risk_lines.shp"
risky_line = env.workspace + "\\Target_Line.shp"

print "1st Process: Select Sewer lines 12 inches or less"
# This creates selects the SS_Line that are < 12 
# and outputs the copy as Sewer_2_shp
# The Mainsize field is string for some reason, so I had to select 
# each variable that was less than 12
arcpy.Select_analysis(SS_Lines, Sewer_2_shp, "\"MAINSIZE\" = '10'" + 
    " OR \"MAINSIZE\" = '2' OR \"MAINSIZE\" = '2.5' OR " + 
    "\"MAINSIZE\" = '3' OR \"MAINSIZE\" = '4' OR \"MAINSIZE\" = '5.4'"
    + "	OR \"MAINSIZE\" = '6' OR \"MAINSIZE\" = '8' OR \"MAINSIZE\" = '4'" +
    "OR \"MAINSIZE\" = '12'"

print "2nd Process: Select (1)"
# This creates a shapefile of the work orders (All_WO) that have the 
# CATCODE STOP and the TASKCODE USG ect... and out puts the points 
# As WO_STOP_1
arcpy.Select_analysis(All_WO, WO_STOP_1, "\"CATCODE\" = 'STOP' AND " +
    "\"TASKCODE\" = 'USG' OR \"CATCODE\" = 'STOP' AND \"TASKCODE\" = 'US'"
    + " OR \"CATCODE\" = 'STOP' AND\"TASKCODE\" = 'USR'")

print "3rd define snapping environments"
# The snapping environments set the rules for how the snap 
# function will snap features together
snapEnv1 = [SS_Lines, "EDGE", '50 Feet']
snapEnv2 = [SS_Lines, "EDGE", '100 Feet']
snapEnv3 = [SS_Lines, "EDGE", '150 Feet']
snapEnv4 = [SS_Lines, "EDGE", '200 Feet']
snapEnv5 = [SS_Lines, "EDGE", '250 Feet']
snapEnv6 = [SS_Lines, "EDGE", '300 Feet']
snapEnv7 = [SS_Lines, "EDGE", '350 Feet']
snapEnv8 = [SS_Lines, "EDGE", '400 Feet']

print "4th Process: Snap (1)"
# The copy of the sewer STOP work orders are snapped to the sewer lines, by
# starting at 50 ft and working out at 50 ft intervals the hope is that the
# majority of the WO points will end up snapped to the line where the wo 
# occurred, but the wo's do not identify what line they occurred on and only
# identify what address the wo occurred at
arcpy.Snap_edit(WO_STOP_1, [
    snapEnv1, snapEnv2, snapEnv3, snapEnv4, 
    snapEnv5, snapEnv6, snapEnv7, snapEnv8
    ])

print "5th Process: Select (2)"
# Similar to 2nd Process, but selects SSO's instead the output file is
# WO_SSO_1
arcpy.Select_analysis(All_WO, WO_SSO_1, "\"CATCODE\" = 'SSO' AND " + 
    "\"TASKCODE\" = 'CAP' OR \"CATCODE\" = 'SSO' AND \"TASKCODE\" = 'DPR' " +
    "OR \"CATCODE\" = 'SSO' AND \"TASKCODE\" = 'GPU' OR \"CATCODE\" = 'SSO" +
    "' AND \"TASKCODE\" = 'PFPU' OR \"CATCODE\" = 'SSO' AND \"TASKCODE\" " + 
    "= 'PSF' OR \"CATCODE\" = 'SSO' AND \"TASKCODE\" = 'RPU'")

print "6th Process: Snap (2)"
# Same as 4th process, but on WO_SSO_1 instead
arcpy.Snap_edit(WO_SSO_1, [
    snapEnv1, snapEnv2, snapEnv3, snapEnv4, 
    snapEnv5, snapEnv6, snapEnv7, snapEnv8
    ])

# This was the last snapping so I am deleting these variables	
del snapEnv1, snapEnv2, snapEnv3, snapEnv4
del snapEnv5, snapEnv6, snapEnv7, snapEnv8

print "7th Adding Field mappings"
# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(Sewer_2_shp)

# Create a single field map for the SSO. I just want to know how many SSO's
# are on the line, so I set merge rule to count
fieldmap = arcpy.FieldMap()
fieldmap.addInputField(WO_SSO_1, "JOBORDER")
fieldmap.mergeRule = "count"

# Rename the field and pass the updated field object back into the field map
field = fieldmap.outputField
field.name = "SSO_Count"
field.aliasName = "SSO_Count"
fieldmap.outputField = field

# Add the field map to the field mapping object 
fieldmappings.addFieldMap(fieldmap) 

print "8th Process: Spatial Join (1) adding SSO WO" 
# The spatial join creates a new shapefile that has the fields that were 
# added in the field mappings
arcpy.SpatialJoin_analysis(Sewer_2_shp, WO_SSO_1, Sewer_SSO_shp,
    "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings)
del fieldmappings

print "9th Adding Field mappings"
# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
fieldmappings1 = arcpy.FieldMappings()
fieldmappings1.addTable(Sewer_SSO_shp)

# Create a single field map of the STOP
fieldmap1 = arcpy.FieldMap()
fieldmap1.addInputField(WO_STOP_1, "JOBORDER")
fieldmap1.mergeRule = "count"

# Rename the field and pass the updated field object back into the field map
field1 = fieldmap1.outputField
field1.name = "STOP_Count"
field1.aliasName = "STOP_Count"
fieldmap1.outputField = field1

# Add the field map to the field mapping object 
fieldmappings1.addFieldMap(fieldmap1) 

print "10th Process: Spatial Join (2) adding STOP WO and adding fields" 
arcpy.SpatialJoin_analysis(Sewer_SSO_shp, WO_STOP_1, Sewer_SSO_STOP_shp,
    "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings1)
del fieldmappings1

print "11th Adding Field mappings"
# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
fieldmappings2 = arcpy.FieldMappings()
fieldmappings2.addTable(Sewer_SSO_STOP_shp)
print "Before adding fields there are " + str(fieldmappings2.fieldCount) \
    + " fields"

fieldmappings3 = arcpy.FieldMappings()

# Create two field maps from RM
Comp_Date = arcpy.FieldMap()
Comp_Date.addInputField(rm,"Comp_Date") 
Comp_Date.mergeRule = 'max'
RM_Count = arcpy.FieldMap()
RM_Count.addInputField(rm, "OBJECTID")
RM_Count.mergeRule = "count"

# Rename the field and pass the updated field object back into the field map
RC = RM_Count.outputField
RC.name = "RM_Count"
RC.aliasName = "RM_Count"
RM_Count.outputField = RC

# Create the field maps to be added to the output
# There has got to be a better way to do this, but this is the only way I
# could figure out...

# Create the individual fields that will be used in future processes, 
# All field maps created here should be empty and hold long type variables
# Create DaySinRM
fieldmappings3.loadFromString(
    "DaySinRM \"DaySinRM\" true true false 9 Long 0 0 ,First,#;")
DaySinRM = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("DaySinRM"))

# Create To_Water
fieldmappings3.loadFromString(
    "To_Water \"To_Water\" true true false 9 Long 0 9 ,First,#;")
To_Water = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("To_Water"))

# Create To_Road
fieldmappings3.loadFromString(
    "To_Road \"To_Road\" true true false 9 Long 0 9 ,First,#,Sewer_2," +
    "To_Road,-1,-1;")
To_Road = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("To_Road"))

# Create To_Low_Pub
fieldmappings3.loadFromString(
    "To_Low_Pub \"To_Low_Pub\" true true false 9 Long 0 9 ,First,#,Sewer_2" +
    ",To_Low_Pub,-1,-1;")
To_Low_Pub = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("To_Low_Pub"))

# Create To_Mod_Pub
fieldmappings3.loadFromString(
    "To_Mod_Pub \"To_Mod_Pub\" true true false 9 Long 0 9 ,First,#,Sewer_2" +
    ",To_Mod_Pub,-1,-1;")
To_Mod_Pub = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("To_Mod_Pub"))

# Create To_High_Pu
fieldmappings3.loadFromString(
    "To_High_Pu \"To_High_Pu\" true true false 9 Long 0 9 ,First,#,Sewer_2" +
    ",To_High_Pu,-1,-1;")
To_High_Pu = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("To_High_Pu"))

# Create Con_Size
fieldmappings3.loadFromString(
    "Con_Size \"Con_Size\" true true false 9 Long 0 9 ,First,#,Sewer_2," +
    "Con_Size,-1,-1;")
Con_Size = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("Con_Size"))
	
# Create Con_Water 
fieldmappings3.loadFromString(
    "Con_Water \"Con_Water\" true true false 9 Long 0 9 ,First,#,Sewer_2," +
    "Con_Water,-1,-1;")
Con_Water = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("Con_Water"))

# Create Con_Road 
fieldmappings3.loadFromString(
    "Con_Road \"Con_Road\" true true false 9 Long 0 9 ,First,#,Sewer_2," +
    "Con_Road,-1,-1;")
Con_Road = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("Con_Road"))
	
# Create Con_Pub
fieldmappings3.loadFromString(
    "Con_Pub \"Con_Pub\" true true false 9 Long 0 9 ,First,#,Sewer_2," +
    "Con_Pub,-1,-1;")
Con_Pub = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("Con_Pub"))
	
# Create Consequenc
fieldmappings3.loadFromString(
    "Consequenc \"Consequenc\" true true false 9 Long 0 9 ,First,#,Sewer_2" +
    ",Consequenc,-1,-1;")
Consequenc = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("Consequenc"))
	
# Create WO_Weight
fieldmappings3.loadFromString(
    "WO_Weight \"WO_Weight\" true true false 9 Long 0 9 ,First,#,Sewer_2," +
    "WO_Weight,-1,-1;")
WO_Weight = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("WO_Weight"))
	
# Create Age_Con 
fieldmappings3.loadFromString(
    "Age_Con \"Age_Con\" true true false 9 Long 0 9 ,First,#,Sewer_2," +
    "Age_Con,-1,-1;")
Age_Con = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("Age_Con"))
	
# Create Phy_Con
fieldmappings3.loadFromString(
    "Phy_Con \"Phy_Con\" true true false 9 Long 0 9 ,First,#,Sewer_2," +
    "Phy_Con,-1,-1;")
Phy_Con = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("Phy_Con"))
	
# Create Failure_
fieldmappings3.loadFromString(
    "Failure_ \"Failure_\" true true false 9 Long 0 9 ,First,#,Sewer_2," + 
    "Failure_,-1,-1;")
Failure_  = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("Failure_"))
	
# Create Fail_Den
fieldmappings3.loadFromString(
    "Fail_Den \"Fail_Den\" true true false 9 Long 0 9 ,First,#,Sewer_2," +
    "Fail_Den,-1,-1;")
Fail_Den = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("Fail_Den"))
	
# Create STOP_like
fieldmappings3.loadFromString(
    "STOP_like \"STOP_like\" true true false 9 Long 0 9 ,First,#,Sewer_2," +
    "STOP_like,-1,-1;")
STOP_like = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("STOP_like"))
	
# Create Likelihood
fieldmappings3.loadFromString(
    "Likelihood \"Likelihood\" true true false 9 Long 0 9 ,First,#,Sewer_2,"
    "Likelihood,-1,-1;")
Likelihood = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("Likelihood"))
	
# Create Risk
fieldmappings3.loadFromString(
    "Risk \"Risk\" true true false 9 Long 0 9 ,First,#,Sewer_2,Risk,-1,-1;")
Risk = fieldmappings3.getFieldMap(
    fieldmappings3.findFieldMapIndex ("Risk"))

# Add the field map to the field mapping object 
fieldmappings2.addFieldMap(To_Water) 
fieldmappings2.addFieldMap(To_Road) 
fieldmappings2.addFieldMap(To_Low_Pub) 
fieldmappings2.addFieldMap(To_Mod_Pub) 
fieldmappings2.addFieldMap(To_High_Pu) 
fieldmappings2.addFieldMap(Comp_Date) 
fieldmappings2.addFieldMap(DaySinRM) 
fieldmappings2.addFieldMap(RM_Count) 
fieldmappings2.addFieldMap(Con_Size) 
fieldmappings2.addFieldMap(Con_Water) 
fieldmappings2.addFieldMap(Con_Road)
fieldmappings2.addFieldMap(Con_Pub) 
fieldmappings2.addFieldMap(Consequenc)
fieldmappings2.addFieldMap(WO_Weight) 
fieldmappings2.addFieldMap(STOP_like)
fieldmappings2.addFieldMap(Phy_Con)
fieldmappings2.addFieldMap(Age_Con)
fieldmappings2.addFieldMap(Failure_) 
fieldmappings2.addFieldMap(Fail_Den)
fieldmappings2.addFieldMap(Likelihood) 
fieldmappings2.addFieldMap(Risk)

print "After adding fields there are " + str(fieldmappings2.fieldCount) + \
    " fields."

print "12th Process: Spatial Join"
## Field 
arcpy.SpatialJoin_analysis(
    Sewer_SSO_STOP_shp, rm, WO_RM_shp, "JOIN_ONE_TO_ONE", "KEEP_ALL",
    fieldmappings2, "SHARE_A_LINE_SEGMENT_WITH", "", "")
del fieldmappings2
del fieldmappings3

print "13th Process: Near (1) how close are the sewers to streams?"
# Adds a field to WO_RM_shp called NEAR_DIST that displays the distance in 
# feet between WO_RM_shp and the nearest Stream feature
arcpy.Near_analysis(WO_RM_shp, Streams, "", "NO_LOCATION", "NO_ANGLE",
    "PLANAR")

print "14th Process: Calculate Field (1)"
# Pull the numbers from the NEAR_DIST field and use them to fill the
# currently empty To_Water field
arcpy.CalculateField_management(WO_RM_shp, "To_Water", "!NEAR_DIST!",
    "PYTHON", "")

print "15th Process: Near (2) how close are the sewers to Major Roads?"
# Replaces the NEAR_DIST with a new field of the same name, this time
# displaying the distance in feet between WO_RM_shp and the nearest major
# road
arcpy.Near_analysis(WO_RM_shp, MAJOR_ROADS, "", "NO_LOCATION", "NO_ANGLE",
    "PLANAR")

print "16th Process: Calculate Field (2)"
# Pull the numbers from the NEAR_DIST field and use them to fill the
# currently empty To_Road field
arcpy.CalculateField_management(WO_RM_shp, "To_Road", "!NEAR_DIST!",
    "PYTHON", "")

print "17th Process: Select (3) "
# I experimented with how to select just comertial and residential areas
# I ended up using the F and B values in the state cd field, I do not know
# what these mean, so this could be improved
arcpy.Select_analysis(BCAD_PARCELS, parcels_select_shp, "state_cd = 'F1'" +
   " OR state_cd = 'F2' OR state_cd LIKE 'A%' OR state_cd LIKE 'B%'")

print "18th Process: Add Field"
# Adding a text field called Type
arcpy.AddField_management(parcels_select_shp,"Type", "TEXT", "", "", "", "",
    "NULLABLE","NON_REQUIRED","")

print "20th Create a Update Cursor to update the fields"
# Create a cursor that lists the features in the parcels file, this allows 
# the user to iterate through the shapefile
parcels = arcpy.UpdateCursor(parcels_select_shp)

print "21st Classify the parcels land use type based on legal class," \
    " state_cd, and file as name."
# Iterate through parcels and update the Type field based on the values found
# in other fields, some, like the golf type, I looked at visually and made
# sure that they were correctly categorized, others, such as the commercial
# density groups are just a best guess and could be improved
for p in parcels:
    if 'F' in p.state_cd:
        # Park
        if 'PARK' in p.legal_desc:
            p.Type = 'PARK'
        # Golf
        elif 'TRADITIONS CLUB' in p.file_as_na:
            p.Type = 'GOLF'    
        elif 'GOLF' in p.file_as_na:
            p.Type = 'GOLF'        
        elif 'THE 1980 PHILLIPS GROUP LLC' in p.file_as_na:
            p.Type = 'GOLF'      
        elif 'COUNTRY CLUB' in p.file_as_na:
            p.Type = 'GOLF' 
        elif 'COUNTRY CLUB' in p.LegalDesc:
            p.Type = 'GOLF' 
        # Hospitals
        elif 'HOSPITAL' in p.file_as_na:
            p.Type = 'HOSPITAL'
        elif 'HOSP' in p.file_as_na:
            p.Type = 'HOSPITAL'
        #SCHOOL
        elif 'ISD' in p.file_as_na:
            p.Type = 'SCHOOL'    
        elif 'SCHOOL DISTRICT' in p.file_as_na:
            p.Type = 'SCHOOL'
        # Commercial Density 
        elif p.Acres > 1:
            p.Type = 'LOW DENSITY COMMERCIAL'
        else:
            p.Type = 'HIGH DENSITY COMMERCIAL'
    else:
        p.Type = 'RESIDENTIAL'
 
    parcels.updateRow(p)

del parcels	
 
print "22nd Process: Select (4) the low community impact areas, golf and" \
    " residential."
# Use the new type field and classifications select the parcels that are golf
# or residential
arcpy.Select_analysis(parcels_select_shp, low_com_impact, 
    "\"Type\" = 'GOLF' OR \"Type\" = 'RESIDENTIAL'")

print "23rd Process: Add Field"
# Add field for market value weights to the low community impact file
arcpy.AddField_management(low_com_impact,"Mark_Weigh", "LONG", "", "", "",
    "","NULLABLE","NON_REQUIRED","")

print "24th Classify the parcels land values to weights"
# Create the cursor to iterate through the low community impact file
low_parcels = arcpy.UpdateCursor(low_com_impact)

# Fill in the Mark_Weigh field based on the value of the market field
for p in low_parcels:
    if p.market > 0:
        if p.market < 75000:
            p.Mark_Weigh = 10
        elif p.market < 130000:
            p.Mark_Weigh = 7
        elif p.market < 165000:
            p.Mark_Weigh = 4
        elif p.market < 230000:
            p.Mark_Weigh = 2   
        else:
            p.Mark_Weigh = 1  
    else:
        p.Mark_Weigh = 1  
    low_parcels.updateRow(p)

del low_parcels	

print "25th Process: Select (5) the moderate community impact areas," \
    " low density commercial."
# Select the low density type parcels and export them as mod_com_impact file
# These are the moderate community impact parcels
arcpy.Select_analysis(parcels_select_shp, mod_com_impact,
    "Type = 'LOW DENSITY COMMERCIAL'")

print "26th Process: Select (6) the high community impact areas: " \
    "Hospitals, Schools, high density commercial."
# Select the high density type parcels, the hospitals, and the schools and
# export them as high_com_impact file, these are the high community impact
# parcels
arcpy.Select_analysis(parcels_select_shp, high_com_impact, "Type = " \
    "'HOSPITAL' OR Type = 'SCHOOL' OR Type = 'HIGH DENSITY COMMERCIAL'")

print "27th Process: Near (3) are the sewers near the low impact area?"
# Replaces the NEAR_DIST with a new field of the same name, this time
# displaying the distance in feet between WO_RM_shp and the low_com_impact
# parcels
arcpy.Near_analysis(WO_RM_shp, low_com_impact, "", "NO_LOCATION", "NO_ANGLE",
    "PLANAR")

print "28st Process: Calculate Field (3) fill To_Low_Pub with distance."
# Pull the numbers from the NEAR_DIST field and use them to fill the
# currently empty To_Low_Pub field
arcpy.CalculateField_management(WO_RM_shp, "To_Low_Pub", "!NEAR_DIST!",
    "PYTHON", "")

print "29th Process: Near (3) are the sewers near the moderate community" \
    " impact area?"
# Replaces the NEAR_DIST with a new field of the same name, this time
# displaying the distance in feet between WO_RM_shp and the mod_com_impact
# parcels
arcpy.Near_analysis(WO_RM_shp, mod_com_impact, "", "NO_LOCATION", "NO_ANGLE",
    "PLANAR")

print "30th Process: Calculate Field (3)"
# Pull the numbers from the NEAR_DIST field and use them to fill the
# currently empty To_Mod_Pub field
arcpy.CalculateField_management(WO_RM_shp, "To_Mod_Pub", "!NEAR_DIST!",
    "PYTHON", "")

print "31st Process: Near (3) are the sewers near the high community" \
    " impact area?"
# Replaces the NEAR_DIST with a new field of the same name, this time
# displaying the distance in feet between WO_RM_shp and the high_com_impact
# parcels
arcpy.Near_analysis(WO_RM_shp, high_com_impact, "", "NO_LOCATION",
    "NO_ANGLE", "PLANAR")

print "32nd Process: Calculate Field (3)"
# Pull the numbers from the NEAR_DIST field and use them to fill the
# currently empty To_High_Pu field
arcpy.CalculateField_management(WO_RM_shp, "To_High_Pu", "!NEAR_DIST!",
    "PYTHON", "")

print "33rd Process: Delete Field"
# Deleting the fields that will no logger be needed 
arcpy.DeleteField_management(WO_RM_shp, "NEAR_FID;NEAR_DIST")

print "34th Process: Calculate Field (4) WO_Weight"
# Fill the WO_Weight field with the sum of the SSO_Count field multiplied by
# 3 and the number in the STOP_Count field.  This will be used later to find
# the WO hot spots, SSOs are more important, which is why they are weighted 
arcpy.CalculateField_management(WO_RM_shp, "WO_Weight", 
    "(!SSO_Count! * 3) + !STOP_Count!", "PYTHON", "")

print "35th Process: Buffer"
# Hot Spot analysis can not be performer on polylines, so a buffer is
# performed with a 50 ft radius and output as SS_Buffer_shp
arcpy.Buffer_analysis(WO_RM_shp, SS_buffer_shp, "50 Feet", "FULL", "ROUND",
    "NONE", "")

print "36th Process: Buffer"
# The output, low_com_imp_buff, will be used later to determine the relative
# values of the residential areas that feed sewer lines, many sewer lines 
# are not in the parcels themselves, but are in the public areas near parcels
arcpy.Buffer_analysis(low_com_impact, low_com_imp_buf, "50 Feet", "FULL", 
    "ROUND", "NONE", "")

print "37th Process: Optimized Hot Spot Analysis"
# If the Hot Spot Analysis is run in ArcMap or ArcCataloge the python script
# will abort after finishing running this process.  The Hot Spot analysis is
# run on the WO_Weight values. 
arcpy.OptimizedHotSpotAnalysis_stats(SS_buffer_shp, SS_Buffer_HS_shp,
    "WO_Weight", "COUNT_INCIDENTS_WITHIN_FISHNET_POLYGONS", "", "",
    Density_Surface)

print "38th Create field mapping for Spatial Join"
# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
fieldmappings4 = arcpy.FieldMappings()
fieldmappings4.addTable(WO_RM_shp)
Gi_Bin = arcpy.FieldMap()
Gi_Bin.addInputField(SS_Buffer_HS_shp,"Gi_Bin") 
Gi_Bin.mergeRule = "first"
fieldmappings4.addFieldMap(Gi_Bin) 

print "39th Process: Spatial Join"
# The results of the Hot Spot analysis are added to the WO_RM_shp file with
# the spatial join.  This is needed to return the format to a polyline 
# format instead of a polygon format. 
arcpy.SpatialJoin_analysis(WO_RM_shp, SS_Buffer_HS_shp, WO_RM_HS_join_shp,
    "JOIN_ONE_TO_ONE", "KEEP_COMMON", fieldmappings4, "INTERSECT", "", "")
del fieldmappings4

print "40th create Cursor find the number of days since RM took place" 
maintenance = arcpy.UpdateCursor(WO_RM_HS_join_shp)

for m in maintenance:
    if m.Comp_Date is None:
        m.DaySinRM = 99999
    else:
        dif = datetime.datetime.now()- m.Comp_Date
        m.DaySinRM = dif.days
    maintenance.updateRow(m)
del maintenance

print "41st Create field mapping for Spatial Join"
# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
fieldmappings5 = arcpy.FieldMappings()
fieldmappings5.addTable(WO_RM_HS_join_shp)
Mark_Weigh = arcpy.FieldMap()
Mark_Weigh.addInputField(low_com_imp_buf,"Mark_Weigh") 
Mark_Weigh.mergeRule = "mean"
fieldmappings5.addFieldMap(Mark_Weigh) 

print "42nd Process: Spatial Join"
arcpy.SpatialJoin_analysis(WO_RM_HS_join_shp, low_com_imp_buf, Risk_shp,
    "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings5, "INTERSECT", "", "")
del fieldmappings5

print "43rd: Create a Update Cursor to update the fields"
# Create a cursor to iterate through the risk file
sewers2 = arcpy.UpdateCursor(Risk_shp)	

print "Create list of the risk values to identify the highest risk lines"
# Create empty list to store risk values in so that the highest risk lines 
# can be identified 
risk_list = []
	
print "44th: Update fields with weights"
for s in sewers2:

    # print "Main size is " + s.MAINSIZE
    if s.MAINSIZE is None:
        s.Con_Size = 0
    elif s.MAINSIZE == " ":
        s.Con_Size = 0
    elif float(s.MAINSIZE) > 8:        
        s.Con_Size = 10
    elif float(s.MAINSIZE) > 6 and float(s.MAINSIZE) <= 8:
        s.Con_Size = 7
    elif float(s.MAINSIZE) > 4 and float(s.MAINSIZE) <= 6:
        s.Con_Size = 4
    elif float(s.MAINSIZE) <= 4:
        s.Con_Size = 1
    else:
        s.Con_Size = 0
    #print s.Con_Size
    
	# print "Main size is " + s.MAINSIZE
    # Maybe I don't want to use this field?
    if s.MAINSIZE is None:
        s.STOP_like = 0
    elif s.MAINSIZE == " ":
        s.STOP_like = 0
    elif float(s.MAINSIZE) > 8 and float(s.MAINSIZE) <= 12:        
        s.STOP_like = 2
    elif float(s.MAINSIZE) > 6 and float(s.MAINSIZE) <= 8:
        s.STOP_like = 4
    elif float(s.MAINSIZE) > 4 and float(s.MAINSIZE) <= 6:
        s.STOP_like = 7
    elif float(s.MAINSIZE) <= 4:
        s.STOP_like = 10
    else:
        s.STOP_like = 0
    # print s.Con_Size	
    
	# print "To_Water is " + s.To_Water	
    if s.To_Water <= 100:
        s.Con_Water = 10
    elif s.To_Water > 100 and s.To_Water <= 500:
        s.Con_Water = 7
    elif s.To_Water > 500 and s.To_Water <= 1000:
        s.Con_Water = 4
    elif s.To_Water > 1000:
        s.Con_Water = 1
    else:
        s.Con_Water = 0
    #print Con_Water
	
    # Need to come up with something different 		
    if s.To_Road <= 10:
        s.Con_Road = 10
    elif s.To_Road > 10 and s.To_Road <= 40:
        s.Con_Road = 7
    elif s.To_Road > 40 and s.To_Road <= 100:
        s.Con_Road = 4
    elif s.To_Road > 100 and s.To_Road <= 200:
        s.Con_Road = 1
    else:
        s.Con_Road = 0

    # Need to Check that this is updated 8/13/15
    if s.To_High_Pu <= 50:
        s.Con_Pub = 10
    elif s.To_Mod_Pub <= 50:
        s.Con_Pub = 7
    elif s.To_Low_Pub <= 50:
        s.Con_Pub = 4
    else:
        s.Con_Pub = 1

    # Weights can be changed, maybe make them variables else where? 
    s.Consequenc = (.3 * s.Con_Size) + (.4 * s.Con_Water) + \
        (.1 * s.Con_Road) + (.2 * s.Con_Pub)
    # Use the number of days since RM occurred to set phy_con value
    if s.DaySinRM  > 1460:
        s.Phy_Con = 10
    elif s.DaySinRM > 1095:
        s.Phy_Con = 7
    elif s.DaySinRM > 730:
        s.Phy_Con = 4
    elif s.DaySinRM > 365:
        s.Phy_Con = 2
    else:
        s.Phy_Con = 1
    # Use the year the line was built to set Age_Con value
    if s.YEAR > 1981:
        s.Age_Con = 1
    elif s.YEAR > 1970 and s.YEAR < 1982:
        s.Age_Con = 2
    elif s.YEAR > 1959 and s.YEAR < 1971:
        s.Age_Con = 4
    elif s.YEAR > 1950 and s.YEAR < 1961:
        s.Age_Con = 7
    elif s.YEAR < 1951:
       s.Age_Con = 10
    else: 
       s.Phy_Con = 0
    # Use the number of STOPs or SSOs to set the Failure_ value
    if s.SSO_Count > 1:
        s.Failure_ = 10
    elif s.SSO_Count > 0 and s.SSO_Count < 2:
        s.Failure_ = 7
    elif s.STOP_Count > 1:
        s.Failure_ = 4
    elif s.STOP_Count > 0 and s.STOP_Count < 2:
        s.Failure_ = 2
    elif s.STOP_Count < 1 and s.SSO_Count < 1:
       s.Failure_ = 1
    else: 
       s.Failure_ = 0  
    # Use the Gi_Bin value from the Hot Spot analysis to set Fail_Den value
    if s.Gi_Bin > 2:
        s.Fail_Den = 10    
    elif s.Gi_Bin > 1:
        s.Fail_Den = 7
    elif s.Gi_Bin > 0:
        s.Fail_Den = 4
    elif s.Gi_Bin < 0:
        s.Fail_Den = 1	
    elif s.Gi_Bin < 1:
        s.Fail_Den = 2		
    else:
        s.Fail_Den = 0

    # Weights can be changed, maybe make them variables else where? 
    # Age Condition is Age_Con, Physical Condition is Phy_Con, 
    # WO Likelihood is Failure_ , WO Density is Fail_Den,
    # Home Values is Mark_Weigh, Potential for Stoppage is STOP_like
    s.Likelihood = (.35 * s.Phy_Con) + (.1 * s.Mark_Weigh) + \
        (.05 * s.Age_Con) + (.15 * s.Failure_) + (.2 * s.Fail_Den) + \
        (.15 * s.STOP_like)

    s.Risk = s.Consequenc * s.Likelihood
    risk_list.append (s.Risk)
	
    sewers2.updateRow(s)
del sewers2

print "Sort list of the risk values to identify the highest risk lines"
# Sort list of the risk values to identify the highest risk lines
sorted_risk = sorted(risk_list, reverse = True)
# Identify the 10th highest risk value
place_ten = sorted_risk[9]

print """Process: Make Layer where the risk is the same or
greater than the tenth highest list value"""
# Define where clause that the Risk is greater than or equal to the 10th
# risk value
where_clause = "\"Risk\" >= " + str(place_ten)
# Make layer of the SS lines that are greater than or equal to the 10th
# risk value
arcpy.MakeFeatureLayer_management(Risk_shp, "High_Risk_lyr", where_clause)
# Copy the layer to make it a feature that process may be run on
arcpy.CopyFeatures_management("High_Risk_lyr", high_risk_lines)

print """Process: Make Layer where the Manholes 
are adjacent to the high risk sewer lines"""
# Create layer version of manholes
arcpy.MakeFeatureLayer_management(MH, "MH_lyr")
# Select the manholes that intersect with the high risk sewer lines
arcpy.SelectLayerByLocation_management("MH_lyr", "INTERSECT",
    "High_Risk_lyr")
# Copy the selected Manholes as their own feature 
arcpy.CopyFeatures_management("MH_lyr", target_MH)

print "43rd: Create a Update Cursor to select the lines"
risky_lines = arcpy.SearchCursor(high_risk_lines)
date = str(datetime.date.today())
rline_FID_list =[]

for line in risky_lines:
    rline_FID_list.append(line.FID)
del risky_lines
print rline_FID_list

print """Set up map document environment to create 
exported map documents as pdfs in map folder"""

#print slyr.symbology
#print slyr.symbologyType
#print slyr
#styleItem = arcpy.mapping.ListStyleItems("USER_STYLE", "Legend Items")#[0] 
#print styleItem


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

### Delete Shapefiles that are no longer needed ### 
#arcpy.Delete_management(out_data, "")
arcpy.Delete_management(Sewer_2_shp, "")
#arcpy.Delete_management(WO_STOP_1, "")
arcpy.Delete_management(WO_SSO_1, "")
arcpy.Delete_management(Sewer_SSO_shp, "")
arcpy.Delete_management(Sewer_SSO_STOP_shp, "")
arcpy.Delete_management(parcels_select_shp, "")
arcpy.Delete_management(low_com_impact, "")
arcpy.Delete_management(mod_com_impact, "")
arcpy.Delete_management(high_com_impact, "")
arcpy.Delete_management(WO_RM_shp, "")
arcpy.Delete_management(SS_buffer_shp, "")
arcpy.Delete_management(low_com_imp_buf, "")
arcpy.Delete_management(SS_Buffer_HS_shp, "")
arcpy.Delete_management(WO_RM_HS_join_shp, "")
#
 
print "Done!"
