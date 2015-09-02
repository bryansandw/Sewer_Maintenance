#############################################################################
# Name: Elizabeth Rentschlar    
# Purpose: Sewer Maintenance based on Risk Prioritization  
# Created: 8/18/15 
# Copyright: (c) City of Bryan  
# ArcGIS Version: 10.2.2 
# Python Version: 2.7 
#############################################################################

# Set the necessary product code
# import arcinfo
from arcpy import env
import arcpy
import datetime
env.overwriteOutput = True
env.autoCancelling = False
env.workspace = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer"

# Local variables:
SS_Lines = r'Database Connections\GISDATA(WS_DB1)@ERENTSCHLAR.sde\WS_DB1.SDE.COB_SANITARY_SEWER_SYSTEM\WS_DB1.SDE.COB_SS_LINES'
All_WO = "G:\\4_LAYERS\\COB_HTE_WORK_ORDERS.lyr" #"G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\All_WO.shp"
Streams = "G:\\4_LAYERS\\FEMA\\BRAZOS_FEMA_CREEK_STREAM.lyr"
MAJOR_ROADS = "G:\\4_LAYERS\\BRAZOS_CENTERLINES(MAJOR ROADS).lyr"
BCAD_PARCELS = "G:\\4_LAYERS\\BCAD\\BCAD_PARCELS.lyr"
Sewer_2_shp = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_2.shp"
WO_STOP_1 = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\WO_STOP_1.shp"
WO_SSO_1 = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\WO_SSO_1.shp"
Sewer_SSO_shp = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp"
Sewer_SSO_STOP_shp = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp"
parcels_select_shp = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\parcels_select.shp"
low_com_impact = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\low_com_impact.shp"
mod_com_impact = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\mod_com_impact.shp"
high_com_impact = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\high_com_impact.shp"
WO_RM_shp = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\WO_RM.shp"
# This guy has been causing problems
rm = r'Database Connections\GISDATA(WS_DB1)@ERENTSCHLAR.sde\WS_DB1.SDE.COB_SANITARY_SEWER_SYSTEM\WS_DB1.SDE.COB_SS_ROUTINE_MAINTENANCE'
SS_buffer_shp = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\SS_buffer.shp"
low_com_imp_buf = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\low_com_imp_buffer.shp"
SS_Buffer_HS_shp = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\SS_Buffer_HS.shp"
Density_Surface = ""
WO_RM_HS_join_shp = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\WO_RM_HS_join.shp"
Risk_shp = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Risk.shp"
#May not use
maint = 'G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Maintenance.shp'
MH = "Database Connections\\GISDATA(WS_DB1)@ERENTSCHLAR.sde\\WS_DB1.SDE.COB_SANITARY_SEWER_SYSTEM\\WS_DB1.SDE.COB_SS_MANHOLES"
target_MH = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\target_MH.shp"
map_output_folder = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Maps\\"
map = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer2.mxd"
single_MH_lyr = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\single_MH.shp"
high_risk_lines = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\high_risk_lines.shp"
risky_line = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\high_risk_line"

print "1st Process: Copy Features (1)"
arcpy.CopyFeatures_management(SS_Lines, Sewer_2_shp, "", "0", "0", "0")

print "2nd Process: Select (1)"
arcpy.Select_analysis(All_WO, WO_STOP_1, "\"CATCODE\" = 'STOP' AND \"TASKCODE\" = 'USG' OR \"CATCODE\" = 'STOP' AND \"TASKCODE\" = 'US' OR \"CATCODE\" = 'STOP' AND\"TASKCODE\" = 'USR'")

print "3rd define snapping environments"
snapEnv1 = [SS_Lines, "EDGE", '50 Feet']
snapEnv2 = [SS_Lines, "EDGE", '100 Feet']
snapEnv3 = [SS_Lines, "EDGE", '150 Feet']
snapEnv4 = [SS_Lines, "EDGE", '200 Feet']
snapEnv5 = [SS_Lines, "EDGE", '250 Feet']
snapEnv6 = [SS_Lines, "EDGE", '300 Feet']
snapEnv7 = [SS_Lines, "EDGE", '350 Feet']
snapEnv8 = [SS_Lines, "EDGE", '400 Feet']

print "4th Process: Snap (1)"
arcpy.Snap_edit(WO_STOP_1, [snapEnv1, snapEnv2, snapEnv3, snapEnv4, snapEnv5, snapEnv6, snapEnv7, snapEnv8])

print "5th Process: Select (2)"
arcpy.Select_analysis(All_WO, WO_SSO_1, "\"CATCODE\" = 'SSO' AND \"TASKCODE\" = 'CAP' OR \"CATCODE\" = 'SSO' AND \"TASKCODE\" = 'DPR' OR \"CATCODE\" = 'SSO' AND \"TASKCODE\" = 'GPU' OR \"CATCODE\" = 'SSO' AND \"TASKCODE\" = 'PFPU' OR \"CATCODE\" = 'SSO' AND \"TASKCODE\" = 'PSF' OR \"CATCODE\" = 'SSO' AND \"TASKCODE\" = 'RPU'")

print "6th Process: Snap (2)"
arcpy.Snap_edit(WO_SSO_1, [snapEnv1, snapEnv2, snapEnv3, snapEnv4, snapEnv5, snapEnv6, snapEnv7, snapEnv8])

print "7th Adding Field mappings"
# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(Sewer_2_shp)

# Create a single field map of the SSO
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
arcpy.SpatialJoin_analysis(Sewer_2_shp, WO_SSO_1, Sewer_SSO_shp, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings)
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
arcpy.SpatialJoin_analysis(Sewer_SSO_shp, WO_STOP_1, Sewer_SSO_STOP_shp, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings1)
del fieldmappings1

print "11th Adding Field mappings"
# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
fieldmappings2 = arcpy.FieldMappings()
fieldmappings2.addTable(Sewer_SSO_STOP_shp)
print "Before adding fields there are " + str(fieldmappings2.fieldCount) + " fields"

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
# There has got to be a better way to do this
# only way I could figure out...
fieldmappings3.loadFromString("DaySinRM \"DaySinRM\" true true false 9 Long 0 0 ,First,#;") #,Sewer_2,DaySinRM,-1,-1
DaySinRM = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("DaySinRM"))
#print "Field map DaySinRM"
fieldmappings3.loadFromString("To_Water \"To_Water\" true true false 9 Long 0 9 ,First,#;") #,Sewer_2,To_Water,-1,-1
To_Water = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("To_Water"))
#print "Field map To_water"
fieldmappings3.loadFromString("To_Road \"To_Road\" true true false 9 Long 0 9 ,First,#,Sewer_2,To_Road,-1,-1;")
To_Road = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("To_Road"))
#print "Field map To_Road"
fieldmappings3.loadFromString("To_Low_Pub \"To_Low_Pub\" true true false 9 Long 0 9 ,First,#,Sewer_2,To_Low_Pub,-1,-1;")
To_Low_Pub = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("To_Low_Pub"))
#print "Field map To_Low_Pub"
fieldmappings3.loadFromString("To_Mod_Pub \"To_Mod_Pub\" true true false 9 Long 0 9 ,First,#,Sewer_2,To_Mod_Pub,-1,-1;")
To_Mod_Pub = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("To_Mod_Pub"))
#print "Field map To_Mod_Pub"
fieldmappings3.loadFromString("To_High_Pub \"To_High_Pub\" true true false 9 Long 0 9 ,First,#,Sewer_2,To_High_Pub,-1,-1;")
To_High_Pub = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("To_High_Pub"))
#print "Field map To_High_Pub"
fieldmappings3.loadFromString("Con_Size \"Con_Size\" true true false 9 Long 0 9 ,First,#,Sewer_2,Con_Size,-1,-1;")
Con_Size = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("Con_Size"))
#print "Field map Con_Size"
fieldmappings3.loadFromString("Con_Water \"Con_Water\" true true false 9 Long 0 9 ,First,#,Sewer_2,Con_Water,-1,-1;")
Con_Water = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("Con_Water"))
#print "Field map Con_Water"
fieldmappings3.loadFromString("Con_Road \"Con_Road\" true true false 9 Long 0 9 ,First,#,Sewer_2,Con_Road,-1,-1;")
Con_Road = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("Con_Road"))
#print "Field map Con_Road"
fieldmappings3.loadFromString("Con_Pub \"Con_Pub\" true true false 9 Long 0 9 ,First,#,Sewer_2,Con_Pub,-1,-1;")
Con_Pub = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("Con_Pub"))
#print "Field map Con_Pub"
fieldmappings3.loadFromString("Consequenc \"Consequenc\" true true false 9 Long 0 9 ,First,#,Sewer_2,Consequenc,-1,-1;")
Consequenc = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("Consequenc"))
#print "Field map Consequenc"
fieldmappings3.loadFromString("WO_Weight \"WO_Weight\" true true false 9 Long 0 9 ,First,#,Sewer_2,WO_Weight,-1,-1;")
WO_Weight = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("WO_Weight"))

fieldmappings3.loadFromString("Age_Con \"Age_Con\" true true false 9 Long 0 9 ,First,#,Sewer_2,Age_Con,-1,-1;")
Age_Con = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("Age_Con"))

fieldmappings3.loadFromString("Phy_Con \"Phy_Con\" true true false 9 Long 0 9 ,First,#,Sewer_2,Phy_Con,-1,-1;")
Phy_Con = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("Phy_Con"))

fieldmappings3.loadFromString("Failure_ \"Failure_\" true true false 9 Long 0 9 ,First,#,Sewer_2,Failure_,-1,-1;")
Failure_  = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("Failure_"))

fieldmappings3.loadFromString("Fail_Den \"Fail_Den\" true true false 9 Long 0 9 ,First,#,Sewer_2,Fail_Den,-1,-1;")
Fail_Den = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("Fail_Den"))

fieldmappings3.loadFromString("Likelihood \"Likelihood\" true true false 9 Long 0 9 ,First,#,Sewer_2,Likelihood,-1,-1;")
Likelihood = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("Likelihood"))

fieldmappings3.loadFromString("Risk \"Risk\" true true false 9 Long 0 9 ,First,#,Sewer_2,Risk,-1,-1;")
Risk = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex ("Risk"))

# Add the field map to the field mapping object 
fieldmappings2.addFieldMap(To_Water) 
fieldmappings2.addFieldMap(To_Road) 
fieldmappings2.addFieldMap(To_Low_Pub) 
fieldmappings2.addFieldMap(To_Mod_Pub) 
fieldmappings2.addFieldMap(To_High_Pub) 
fieldmappings2.addFieldMap(Comp_Date) 
fieldmappings2.addFieldMap(DaySinRM) 
fieldmappings2.addFieldMap(RM_Count) 
fieldmappings2.addFieldMap(Con_Size) 
fieldmappings2.addFieldMap(Con_Water) 
fieldmappings2.addFieldMap(Con_Road)
fieldmappings2.addFieldMap(Con_Pub) 
fieldmappings2.addFieldMap(Consequenc)
fieldmappings2.addFieldMap(WO_Weight) 
fieldmappings2.addFieldMap(Phy_Con)
fieldmappings2.addFieldMap(Age_Con)
fieldmappings2.addFieldMap(Failure_) 
fieldmappings2.addFieldMap(Fail_Den)
fieldmappings2.addFieldMap(Likelihood) 
fieldmappings2.addFieldMap(Risk)

print "After adding fields there are " + str(fieldmappings2.fieldCount) + " fields."

print "12th Process: Spatial Join"
## Field 
arcpy.SpatialJoin_analysis(Sewer_SSO_STOP_shp, rm, WO_RM_shp, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings2, "SHARE_A_LINE_SEGMENT_WITH", "", "")
del fieldmappings2
del fieldmappings3

print "13th Process: Near (1) how close are the sewers to streams?"
arcpy.Near_analysis(WO_RM_shp, Streams, "", "NO_LOCATION", "NO_ANGLE", "PLANAR")

print "14th Process: Calculate Field (1)"
arcpy.CalculateField_management(WO_RM_shp, "To_Water", "!NEAR_DIST!", "PYTHON", "")

print "15th Process: Near (2) how close are the sewers to Major Roads?"
arcpy.Near_analysis(WO_RM_shp, MAJOR_ROADS, "", "NO_LOCATION", "NO_ANGLE", "PLANAR")

print "16th Process: Calculate Field (2)"
arcpy.CalculateField_management(WO_RM_shp, "To_Road", "!NEAR_DIST!", "PYTHON", "")

print "17th Process: Select (3) "
arcpy.Select_analysis(BCAD_PARCELS, parcels_select_shp, "state_cd = 'F1' OR state_cd = 'F2' OR state_cd LIKE 'A%' OR state_cd LIKE 'B%'")

print "18th Process: Add Field"
arcpy.AddField_management(parcels_select_shp,"Type", "TEXT", "", "", "", "","NULLABLE","NON_REQUIRED","")

print "20th Create a Update Cursor to update the fields"
parcels = arcpy.UpdateCursor(parcels_select_shp)

print "21st Classify the parcels land use type based on legal class, state_cd, and file as name."
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

         
        elif p.Acres > 1:
            p.Type = 'LOW DENSITY COMMERCIAL'
        else:
            p.Type = 'HIGH DENSITY COMMERCIAL'
    else:
        p.Type = 'RESIDENTIAL'
 
    parcels.updateRow(p)

del parcels	
 
print "22nd Process: Select (4) the low community impact areas, golf and residential."
arcpy.Select_analysis(parcels_select_shp, low_com_impact, "\"Type\" = 'GOLF' OR \"Type\" = 'RESIDENTIAL'")

print "23rd Process: Add Field"
arcpy.AddField_management(low_com_impact,"Mark_Weigh", "LONG", "", "", "", "","NULLABLE","NON_REQUIRED","")

print "24th Classify the parcels land values to weights"

low_parcels = arcpy.UpdateCursor(low_com_impact)

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

print "25th Process: Select (5) the moderate community impact areas, low density commercial."
arcpy.Select_analysis(parcels_select_shp, mod_com_impact, "Type = 'LOW DENSITY COMMERCIAL'")

print """26th Process: Select (6) the high community impact areas: 
Hospitals, Schools, high density commercial."""
arcpy.Select_analysis(parcels_select_shp, high_com_impact, "Type = 'HOSPITAL' OR Type = 'SCHOOL' OR Type = 'HIGH DENSITY COMMERCIAL'")

print "27th Process: Near (3) are the sewers near the low impact area?"
arcpy.Near_analysis(WO_RM_shp, low_com_impact, "", "NO_LOCATION", "NO_ANGLE", "PLANAR")

print "28st Process: Calculate Field (3) fill To_Low_Pub with distance."
arcpy.CalculateField_management(WO_RM_shp, "To_Low_Pub", "!NEAR_DIST!", "PYTHON", "")

print "29th Process: Near (3) are the sewers near the moderate community impact area?"
arcpy.Near_analysis(WO_RM_shp, mod_com_impact, "", "NO_LOCATION", "NO_ANGLE", "PLANAR")

print "30th Process: Calculate Field (3)"
arcpy.CalculateField_management(WO_RM_shp, "To_Mod_Pub", "!NEAR_DIST!", "PYTHON", "")

print "31st Process: Near (3) are the sewers near the high community impact area?"
arcpy.Near_analysis(WO_RM_shp, high_com_impact, "", "NO_LOCATION", "NO_ANGLE", "PLANAR")

print "32nd Process: Calculate Field (3)" # Getting an error that field doesn't exist 
arcpy.CalculateField_management(WO_RM_shp, "To_High_Pu", "!NEAR_DIST!", "PYTHON", "")

print "33rd Process: Delete Field"
arcpy.DeleteField_management(WO_RM_shp, "NEAR_FID;NEAR_DIST")

print "34th Process: Calculate Field (4) WO_Weight"
arcpy.CalculateField_management(WO_RM_shp, "WO_Weight", "(!SSO_Count! * 3) + !STOP_Count!", "PYTHON", "")

print "35th Process: Buffer"
arcpy.Buffer_analysis(WO_RM_shp, SS_buffer_shp, "50 Feet", "FULL", "ROUND", "NONE", "")

print "36th Process: Buffer"
arcpy.Buffer_analysis(low_com_impact, low_com_imp_buf, "50 Feet", "FULL", "ROUND", "NONE", "")

print """37th Process: Optimized Hot Spot Analysis
Have been getting an Error on this guy
Keeps kicking me out of the script after running Hot Spot...
"""
arcpy.OptimizedHotSpotAnalysis_stats(SS_buffer_shp, SS_Buffer_HS_shp, "WO_Weight", "COUNT_INCIDENTS_WITHIN_FISHNET_POLYGONS", "", "", Density_Surface)

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
arcpy.SpatialJoin_analysis(WO_RM_shp, SS_Buffer_HS_shp, WO_RM_HS_join_shp, "JOIN_ONE_TO_ONE", "KEEP_COMMON", fieldmappings4, "INTERSECT", "", "")
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
arcpy.SpatialJoin_analysis(WO_RM_HS_join_shp, low_com_imp_buf, Risk_shp, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings5, "INTERSECT", "", "")
del fieldmappings5

print "43rd: Create a Update Cursor to update the fields"
sewers2 = arcpy.UpdateCursor(Risk_shp)	

print """Create list of the risk values to 
identify the highest risk lines"""
risk_list = []
	
print "44th: Update fields with weights"
for s in sewers2:

    #print "Main size is " + s.MAINSIZE
    if s.MAINSIZE is None:
        s.Con_Size = 0
    elif s.MAINSIZE == " ":
        s.Con_Size = 0
    elif float(s.MAINSIZE) > 14:        
        s.Con_Size = 10
    elif float(s.MAINSIZE) > 9 and float(s.MAINSIZE) < 15:
        s.Con_Size = 7
    elif float(s.MAINSIZE) > 6 and float(s.MAINSIZE) < 10:
        s.Con_Size = 4
    elif float(s.MAINSIZE) < 7:
        s.Con_Size = 1
    else:
        s.Con_Size = 0
    #print s.Con_Size
	
    #print "To_Water is " + s.To_Water	
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
    s.Consequenc = (.3 * s.Con_Size) + (.4 * s.Con_Water) + (.1 * s.Con_Road) + (.2 * s.Con_Pub)

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
    s.Likelihood = (.05 * s.Phy_Con) + (.15 * s.Mark_Weigh) + (.4 * s.Age_Con) + (.1 * s.Failure_) + (.3 * s.Fail_Den)

    s.Risk = s.Consequenc * s.Likelihood
    risk_list.append (s.Risk)
	
    sewers2.updateRow(s)
del sewers2

print """Sort list of the risk values to identify the 
highest risk lines"""
#print risk_list
sorted_risk = sorted(risk_list, reverse=True)
#print sorted_risk
place_ten = sorted_risk[9]

print """Process: Make Layer where the risk is the same or
greater than the tenth highest list value"""
where_clause = "\"Risk\" >= " + str(place_ten)
arcpy.MakeFeatureLayer_management(Risk_shp, "High_Risk_lyr", where_clause)
arcpy.CopyFeatures_management("High_Risk_lyr", high_risk_lines)

print """Process: Make Layer where the Manholes 
are adjacent to the high risk sewer lines"""
arcpy.MakeFeatureLayer_management(MH, "MH_lyr")
arcpy.SelectLayerByLocation_management("MH_lyr", "INTERSECT", "High_Risk_lyr")
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
mapdoc = arcpy.mapping.MapDocument(map)

# need to loop through the target MH
# May need to loop through based on the FID value???
print "exporting maps"
for FID in rline_FID_list:
    where_clause2 = "\"FID\" = " + str(FID) + ""
    print where_clause2
    single_risky_line = risky_line + str(FID) + ".shp"
    arcpy.Select_analysis(high_risk_lines, single_risky_line, where_clause2)

    #Data Frame 
    data_frame = arcpy.mapping.ListDataFrames(mapdoc)[0]
    print data_frame.name
    print data_frame.scale
    scale = data_frame.scale
    
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
		
    wildcard = "high_risk_line" + str(FID) 
    print wildcard
    lyr = arcpy.mapping.ListLayers(mapdoc, wildcard)[0]
    print lyr
    data_frame.extent = lyr.getExtent(True) 
    data_frame.scale = new_scale 
    #data_frame.scale = lyr.getScale(True)
    print data_frame.extent
    arcpy.RefreshActiveView()      
    
    #arcpy.SelectLayerByAttribute_management(target_MH, "NEW_SELECTION", ' "LABEL" = mh.LABEL ')
    #zoomToSelectedFeatures(mh)

    map_output = map_output_folder + str(FID) + "_" + date + ".pdf"
    arcpy.mapping.ExportToPDF(mapdoc, map_output)

	
print "Done!"
