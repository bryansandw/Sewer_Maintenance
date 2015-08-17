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

# Import arcpy module
import arcpy
env.overwriteOutput = True

# Local variables:
SS_Lines = "Database Connections\\COBSDE@erentschlar.sde\\SDE.GIS_ADMIN.COB_SANITARY_SEWER_SYSTEM\\sde.GIS_ADMIN.COB_SS_LINES"
All_WO = "G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\All_WO.shp"
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
rm = "Database Connections\\COBSDE@erentschlar.sde\\SDE.GIS_ADMIN.COB_SANITARY_SEWER_SYSTEM\\SDE.GIS_ADMIN.COB_SS_ROUTINE_MAINTENANCE"  


print "1st Process: Copy Features (1)"
arcpy.CopyFeatures_management(SS_Lines, Sewer_2_shp, "", "0", "0", "0")

print "2nd Process: Select (1)"
arcpy.Select_analysis(All_WO, WO_STOP_1, "\"CATCODE\" = 'STOP'")

print "3rd Process: Snap (1)"
arcpy.Snap_edit(WO_STOP_1, "'SS Lines' EDGE '50 Feet';'SS Lines' EDGE '100 Feet';'SS Lines' EDGE '150 Feet';'SS Lines' EDGE '200 Feet';'SS Lines' EDGE '250 Feet';'SS Lines' EDGE '300 Feet';'SS Lines' EDGE '350 Feet';'SS Lines' EDGE '400 Feet'")

print "4th Process: Select (2)"
arcpy.Select_analysis(All_WO, WO_SSO_1, "\"CATCODE\" = 'SSO'")

print "5th Process: Snap (2)"
arcpy.Snap_edit(WO_SSO_1, "'SS Lines' EDGE '50 Feet';'SS Lines' EDGE '100 Feet';'SS Lines' EDGE '150 Feet';'SS Lines' EDGE '200 Feet';'SS Lines' EDGE '250 Feet';'SS Lines' EDGE '300 Feet';'SS Lines' EDGE '350 Feet';'SS Lines' EDGE '400 Feet'")

print "6th Process: Spatial Join (1) adding SSO WO"
arcpy.SpatialJoin_analysis(Sewer_2_shp, WO_SSO_1, Sewer_SSO_shp, "JOIN_ONE_TO_ONE", "KEEP_ALL", "MAINSIZE \"MAINSIZE\" true true false 10 Text 0 0 ,First,#,Sewer_2,MAINSIZE,-1,-1;PLAT_ID \"PLAT_ID\" true true false 15 Text 0 0 ,First,#,Sewer_2,PLAT_ID,-1,-1;CLASS \"CLASS\" true true false 25 Text 0 0 ,First,#,Sewer_2,CLASS,-1,-1;MAT_TYPE \"MAT_TYPE\" true true false 15 Text 0 0 ,First,#,Sewer_2,MAT_TYPE,-1,-1;Flow_Out \"Flow_Out\" true true false 17 Double 3 16 ,First,#,Sewer_2,Flow_Out,-1,-1;Flow_In \"Flow_In\" true true false 17 Double 3 16 ,First,#,Sewer_2,Flow_In,-1,-1;DROP_INVER \"DROP_INVER\" true true false 19 Double 11 18 ,First,#,Sewer_2,DROP_INVER,-1,-1;MAIN_TYPE \"MAIN_TYPE\" true true false 12 Text 0 0 ,First,#,Sewer_2,MAIN_TYPE,-1,-1;LENGTH \"LENGTH\" true true false 12 Double 2 11 ,First,#,Sewer_2,LENGTH,-1,-1;YEAR \"YEAR\" true true false 10 Double 0 10 ,First,#,Sewer_2,YEAR,-1,-1;BIN_NO \"BIN_NO\" true true false 25 Text 0 0 ,First,#,Sewer_2,BIN_NO,-1,-1;Project_NO \"Project_NO\" true true false 20 Text 0 0 ,First,#,Sewer_2,Project_NO,-1,-1;Calc_Leng \"Calc_Leng\" true true false 14 Double 2 13 ,First,#,Sewer_2,Calc_Leng,-1,-1;Maintenanc \"Maintenanc\" true true false 20 Text 0 0 ,First,#,Sewer_2,Maintenanc,-1,-1;Maint_Year \"Maint_Year\" true true false 10 Double 0 10 ,First,#,Sewer_2,Maint_Year,-1,-1;Maint_Mat \"Maint_Mat\" true true false 10 Text 0 0 ,First,#,Sewer_2,Maint_Mat,-1,-1;Maint_Type \"Maint_Type\" true true false 10 Text 0 0 ,First,#,Sewer_2,Maint_Type,-1,-1;Maint_Stat \"Maint_Stat\" true true false 20 Text 0 0 ,First,#,Sewer_2,Maint_Stat,-1,-1;Report \"Report\" true true false 175 Text 0 0 ,First,#,Sewer_2,Report,-1,-1;CCTV_File \"CCTV_File\" true true false 50 Text 0 0 ,First,#,Sewer_2,CCTV_File,-1,-1;CCTV_Date \"CCTV_Date\" true true false 8 Date 0 0 ,First,#,Sewer_2,CCTV_Date,-1,-1;CCTV_Stat \"CCTV_Stat\" true true false 50 Text 0 0 ,First,#,Sewer_2,CCTV_Stat,-1,-1;TV_Length \"TV_Length\" true true false 11 Double 2 10 ,First,#,Sewer_2,TV_Length,-1,-1;Comments \"Comments\" true true false 50 Text 0 0 ,First,#,Sewer_2,Comments,-1,-1;TECH \"TECH\" true true false 5 Text 0 0 ,First,#,Sewer_2,TECH,-1,-1;Data_Sourc \"Data_Sourc\" true true false 50 Text 0 0 ,First,#,Sewer_2,Data_Sourc,-1,-1;Entry_Date \"Entry_Date\" true true false 8 Date 0 0 ,First,#,Sewer_2,Entry_Date,-1,-1;WRNTY_DATE \"WRNTY_DATE\" true true false 8 Date 0 0 ,First,#,Sewer_2,WRNTY_DATE,-1,-1;Shape_len \"Shape_len\" true true false 19 Double 0 0 ,First,#,Sewer_2,Shape_len,-1,-1;To_Water \"To_Water\" true true false 9 Long 0 9 ,First,#,Sewer_2,To_Water,-1,-1;To_Road \"To_Road\" true true false 9 Long 0 9 ,First,#,Sewer_2,To_Road,-1,-1;To_Public \"To_Public\" true true false 9 Long 0 9 ,First,#,Sewer_2,To_Public,-1,-1;Con_Size \"Con_Size\" true true false 9 Long 0 9 ,First,#,Sewer_2,Con_Size,-1,-1;Con_Water \"Con_Water\" true true false 9 Long 0 9 ,First,#,Sewer_2,Con_Water,-1,-1;Con_Road \"Con_Road\" true true false 9 Long 0 9 ,First,#,Sewer_2,Con_Road,-1,-1;Con_Pub \"Con_Pub\" true true false 9 Long 0 9 ,First,#,Sewer_2,Con_Pub,-1,-1;Consequenc \"Consequenc\" true true false 9 Long 0 9 ,First,#,Sewer_2,Consequenc,-1,-1;SSO_Count \"SSO_Count\" true true false 10 Double 0 10 ,Count,#,WO_SSO_1,OBJECTID,-1,-1", "INTERSECT", "", "")

print "7th Process: Spatial Join (2) adding STOP WO and adding fields" 
arcpy.SpatialJoin_analysis(Sewer_SSO_shp, WO_STOP_1, Sewer_SSO_STOP_shp, "JOIN_ONE_TO_ONE", "KEEP_ALL", "Join_Count \"Join_Count\" true true false 0 Long 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Join_Count,-1,-1;TARGET_FID \"TARGET_FID\" true true false 0 Long 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,TARGET_FID,-1,-1;MAINSIZE \"MAINSIZE\" true true false 10 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,MAINSIZE,-1,-1;PLAT_ID \"PLAT_ID\" true true false 15 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,PLAT_ID,-1,-1;CLASS \"CLASS\" true true false 25 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,CLASS,-1,-1;MAT_TYPE \"MAT_TYPE\" true true false 15 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,MAT_TYPE,-1,-1;Flow_Out \"Flow_Out\" true true false 17 Double 3 16 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Flow_Out,-1,-1;Flow_In \"Flow_In\" true true false 17 Double 3 16 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Flow_In,-1,-1;DROP_INVER \"DROP_INVER\" true true false 19 Double 11 18 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,DROP_INVER,-1,-1;MAIN_TYPE \"MAIN_TYPE\" true true false 12 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,MAIN_TYPE,-1,-1;LENGTH \"LENGTH\" true true false 12 Double 2 11 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,LENGTH,-1,-1;YEAR \"YEAR\" true true false 10 Double 0 10 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,YEAR,-1,-1;BIN_NO \"BIN_NO\" true true false 25 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,BIN_NO,-1,-1;Project_NO \"Project_NO\" true true false 20 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Project_NO,-1,-1;Calc_Leng \"Calc_Leng\" true true false 14 Double 2 13 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Calc_Leng,-1,-1;Maintenanc \"Maintenanc\" true true false 20 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Maintenanc,-1,-1;Maint_Year \"Maint_Year\" true true false 10 Double 0 10 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Maint_Year,-1,-1;Maint_Mat \"Maint_Mat\" true true false 10 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Maint_Mat,-1,-1;Maint_Type \"Maint_Type\" true true false 10 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Maint_Type,-1,-1;Maint_Stat \"Maint_Stat\" true true false 20 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Maint_Stat,-1,-1;Report \"Report\" true true false 175 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Report,-1,-1;CCTV_File \"CCTV_File\" true true false 50 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,CCTV_File,-1,-1;CCTV_Date \"CCTV_Date\" true true false 8 Date 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,CCTV_Date,-1,-1;CCTV_Stat \"CCTV_Stat\" true true false 50 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,CCTV_Stat,-1,-1;TV_Length \"TV_Length\" true true false 11 Double 2 10 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,TV_Length,-1,-1;Comments \"Comments\" true true false 50 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Comments,-1,-1;TECH \"TECH\" true true false 5 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,TECH,-1,-1;Data_Sourc \"Data_Sourc\" true true false 50 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Data_Sourc,-1,-1;Entry_Date \"Entry_Date\" true true false 8 Date 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Entry_Date,-1,-1;WRNTY_DATE \"WRNTY_DATE\" true true false 8 Date 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,WRNTY_DATE,-1,-1;Shape_len \"Shape_len\" true true false 19 Double 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Shape_len,-1,-1;To_Water \"To_Water\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,To_Water,-1,-1;To_Road \"To_Road\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,To_Road,-1,-1;To_Low_Pub \"To_Low_Pub\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,To_Low_Pub,-1,-1;To_Mod_Pub \"To_Mod_Pub\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,To_Mod_Pub,-1,-1;To_High_Pub \"To_High_Pub\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,To_High_Pub,-1,-1;Con_Size \"Con_Size\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Con_Size,-1,-1;Con_Water \"Con_Water\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Con_Water,-1,-1;Con_Road \"Con_Road\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Con_Road,-1,-1;Con_Pub \"Con_Pub\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Con_Pub,-1,-1;Consequenc \"Consequenc\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Consequenc,-1,-1;SSO_Count \"SSO_Count\" true true false 10 Double 0 10 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,SSO_Count,-1,-1;STOP_Count \"STOP_Count\" true true false 10 Double 0 10 ,Count,#,WO_STOP_1,OBJECTID,-1,-1;WO_Weight \"WO_Weight\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,WO_Weight,-1,-1;Phy_Con \"Phy_Con\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Phy_Con,-1,-1;Failure_ \"Failure_\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Failure_,-1,-1;Fail_Den \"Fail_Den\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Fail_Den,-1,-1;Likelihood \"Likelihood\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Likelihood,-1,-1;Risk \"Risk\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO.shp,Risk,-1,-1;", "INTERSECT", "", "")

print "8th Process: Spatial Join"
## Field 
arcpy.SpatialJoin_analysis(Sewer_SSO_STOP_shp, rm, WO_RM_shp, "JOIN_ONE_TO_ONE", "KEEP_ALL", "MAINSIZE \"MAINSIZE\" true true false 10 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,MAINSIZE,-1,-1;PLAT_ID \"PLAT_ID\" true true false 15 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,PLAT_ID,-1,-1;CLASS \"CLASS\" true true false 25 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,CLASS,-1,-1;MAT_TYPE \"MAT_TYPE\" true true false 15 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,MAT_TYPE,-1,-1;Flow_Out \"Flow_Out\" true true false 17 Double 3 16 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Flow_Out,-1,-1;Flow_In \"Flow_In\" true true false 17 Double 3 16 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Flow_In,-1,-1;DROP_INVER \"DROP_INVER\" true true false 19 Double 11 18 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,DROP_INVER,-1,-1;MAIN_TYPE \"MAIN_TYPE\" true true false 12 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,MAIN_TYPE,-1,-1;LENGTH \"LENGTH\" true true false 12 Double 2 11 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,LENGTH,-1,-1;YEAR \"YEAR\" true true false 10 Double 0 10 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,YEAR,-1,-1;BIN_NO \"BIN_NO\" true true false 25 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,BIN_NO,-1,-1;Project_NO \"Project_NO\" true true false 20 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Project_NO,-1,-1;Calc_Leng \"Calc_Leng\" true true false 14 Double 2 13 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Calc_Leng,-1,-1;Maintenanc \"Maintenanc\" true true false 20 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Maintenanc,-1,-1;Maint_Year \"Maint_Year\" true true false 10 Double 0 10 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Maint_Year,-1,-1;Maint_Mat \"Maint_Mat\" true true false 10 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Maint_Mat,-1,-1;Maint_Type \"Maint_Type\" true true false 10 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Maint_Type,-1,-1;Maint_Stat \"Maint_Stat\" true true false 20 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Maint_Stat,-1,-1;Report \"Report\" true true false 175 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Report,-1,-1;CCTV_File \"CCTV_File\" true true false 50 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,CCTV_File,-1,-1;CCTV_Date \"CCTV_Date\" true true false 8 Date 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,CCTV_Date,-1,-1;CCTV_Stat \"CCTV_Stat\" true true false 50 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,CCTV_Stat,-1,-1;TV_Length \"TV_Length\" true true false 11 Double 2 10 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,TV_Length,-1,-1;Comments \"Comments\" true true false 50 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Comments,-1,-1;TECH \"TECH\" true true false 5 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,TECH,-1,-1;Data_Sourc \"Data_Sourc\" true true false 50 Text 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Data_Sourc,-1,-1;Entry_Date \"Entry_Date\" true true false 8 Date 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Entry_Date,-1,-1;WRNTY_DATE \"WRNTY_DATE\" true true false 8 Date 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,WRNTY_DATE,-1,-1;Shape_len \"Shape_len\" true true false 19 Double 0 0 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Shape_len,-1,-1;To_Water \"To_Water\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,To_Water,-1,-1;To_Road \"To_Road\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,To_Road,-1,-1;To_Low_Pub \"To_Low_Pub\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,To_Low_Pub,-1,-1;To_Mod_Pub \"To_Mod_Pub\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,To_Mod_Pub,-1,-1;To_High_Pu \"To_High_Pu\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,To_High_Pu,-1,-1;Con_Size \"Con_Size\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Con_Size,-1,-1;Con_Water \"Con_Water\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Con_Water,-1,-1;Con_Road \"Con_Road\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Con_Road,-1,-1;Con_Pub \"Con_Pub\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Con_Pub,-1,-1;Consequenc \"Consequenc\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Consequenc,-1,-1;SSO_Count \"SSO_Count\" true true false 10 Double 0 10 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,SSO_Count,-1,-1;STOP_Count \"STOP_Count\" true true false 10 Double 0 10 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,STOP_Count,-1,-1;WO_Weight \"WO_Weight\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,WO_Weight,-1,-1;Phy_Con \"Phy_Con\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Phy_Con,-1,-1;Age_Con \"Age_Con\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Age_Con,-1,-1;Failure_ \"Failure_\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Failure_,-1,-1;Fail_Den \"Fail_Den\" true true false 9 Long 0 9 ,First,#,G:\\GIS_PROJECTS\\WATER_SERVICES\\Tess\\Sewer\\Sewer_SSO_STOP.shp,Fail_Den,-1,-1;Comp_Date \"Comp_Date\" true true false 36 Date 0 0 ,Max,#,SDE.GIS_ADMIN.COB_SS_ROUTINE_MAINTENANCE,Comp_Date,-1,-1;RM_Count \"RM_Count\" true true false 50 Double 0 0 ,Count,#,SDE.GIS_ADMIN.COB_SS_ROUTINE_MAINTENANCE,OBJECTID,-1,-1;DaySinRM \"DaySinRM\" true true false 50 Long 0 0 ,First,#;Likelihood \"Likelihood\" true true false 50 Long 0 0 ,First,#;Risk \"Risk\" true true false 50 Long 0 0 ,First,#", "SHARE_A_LINE_SEGMENT_WITH", "", "")

print "9th Process: Near (1) how close are the sewers to streams?"
arcpy.Near_analysis(WO_RM_shp, "Streams", "", "NO_LOCATION", "NO_ANGLE", "PLANAR")

print "10th Process: Calculate Field (1)"
arcpy.CalculateField_management(WO_RM_shp, "To_Water", "!NEAR_DIST!", "PYTHON", "")

print "11th Process: Near (2) how close are the sewers to Major Roads?"
arcpy.Near_analysis(WO_RM_shp, "'MAJOR ROADS'", "", "NO_LOCATION", "NO_ANGLE", "PLANAR")

print "13th Process: Calculate Field (2)"
arcpy.CalculateField_management(WO_RM_shp, "To_Road", "!NEAR_DIST!", "PYTHON", "")

print "13th Process: Select (3) "
arcpy.Select_analysis(BCAD_PARCELS, parcels_select_shp, "state_cd = 'F1' OR state_cd = 'F2' OR state_cd LIKE 'A%' OR state_cd LIKE 'B%'")

print "14th Process: Add Field"
arcpy.AddField_management(parcels_select_shp,"Type", "TEXT", "", "", "", "","NULLABLE","NON_REQUIRED","")

print "15th Create a Update Cursor to update the fields"
parcels = arcpy.UpdateCursor(parcels_select_shp)

print "16th Classify the parcels land use type based on legal class, state_cd, and file as name."
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
 
print "17th Process: Select (4) the low community impact areas, golf and residential."
arcpy.Select_analysis(parcels_select_shp, low_com_impact, "\"Type\" = 'GOLF' OR \"Type\" = 'RESIDENTIAL'")

print "18th Process: Select (5) the moderate community impact areas, low density commercial."
arcpy.Select_analysis(parcels_select_shp, mod_com_impact, "Type = 'LOW DENSITY COMMERCIAL'")

print """19th Process: Select (6) the high community impact areas: 
Hospitals, Schools, high density commercial."""
arcpy.Select_analysis(parcels_select_shp, high_com_impact, "Type = 'HOSPITAL' OR Type = 'SCHOOL' OR Type = 'HIGH DENSITY COMMERCIAL'")

print "20th Process: Near (3) are the sewers near the low impact area?"
arcpy.Near_analysis(WO_RM_shp, low_com_impact, "", "NO_LOCATION", "NO_ANGLE", "PLANAR")

print "21st Process: Calculate Field (3) fill To_Low_Pub with distance."
arcpy.CalculateField_management(WO_RM_shp, "To_Low_Pub", "!NEAR_DIST!", "PYTHON", "")

print "22nd Process: Near (3) are the sewers near the moderate community impact area?"
arcpy.Near_analysis(WO_RM_shp, mod_com_impact, "", "NO_LOCATION", "NO_ANGLE", "PLANAR")

print "23rd Process: Calculate Field (3)"
arcpy.CalculateField_management(WO_RM_shp, "To_Mod_Pub", "!NEAR_DIST!", "PYTHON", "")

print "24th Process: Near (3) are the sewers near the high community impact area?"
arcpy.Near_analysis(WO_RM_shp, high_com_impact, "", "NO_LOCATION", "NO_ANGLE", "PLANAR")

print "25th Process: Calculate Field (3)" # Getting an error that field doesn't exist 
arcpy.CalculateField_management(WO_RM_shp, "To_High_Pu", "!NEAR_DIST!", "PYTHON", "")

print "26th Process: Delete Field"
arcpy.DeleteField_management(WO_RM_shp, "NEAR_FID;NEAR_DIST")

print "27th Process: Calculate Field (4) WO_Weight"
arcpy.CalculateField_management(WO_RM_shp, "WO_Weight", "(!SSO_Count! * 3) + !STOP_Count!", "PYTHON", "")

print "28th create Cursor find the number of days since RM took place" 
maintenance = arcpy.UpdateCursor(WO_RM_shp)

for m in maintenance:
    if m.Comp_Date is None:
        m.DaySinRM = 99999
    else:
        dif = datetime.datetime.now()- m.Comp_Date
        m.DaySinRM = dif.days
    maintenance.updateRow(m)
del maintenance

print """29th create a Update Cursor to make a List of 
the WO_Weight field values to normalize them later"""
sewers = arcpy.UpdateCursor(WO_RM_shp)

WO_Weight = []
for s in sewers:
    WO_Weight.append(s.WO_Weight)
del sewers

Fail = max(WO_Weight)
#print Fail
norm = float(10) / Fail 


#Create a Update Cursor to update the fields
sewers2 = arcpy.UpdateCursor(WO_RM_shp)	
	
# Update fields with weights	
for s in sewers2:
    if s.MAINSIZE > 14:
        s.Con_Size = 10
    elif s.MAINSIZE > 9 and s.MAINSIZE < 15:
        s.Con_Size = 7
    elif s.MAINSIZE > 6 and s.MAINSIZE < 10:
        s.Con_Size = 4
    elif s.MAINSIZE < 7:
        s.Con_Size = 1
    else:
        s.Con_Size = 0
		
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
    elif s.YEAR > 1970 and s.YEAR < 1981:
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

    if s.WO_Weight > 0:
        den = s.WO_Weight
        print den
        s.Fail_Den = (den * norm)    
        print s.Fail_Den    
    else:
        s.Fail_Den = 0

# Weights can be changed, maybe make them variables else where? 
    s.Likelihood = (.25 * s.Phy_Con) + (.25 * s.Age_Con) + (.25 * s.Failure_) + (.25 * s.Fail_Den)

    s.Risk = s.Consequenc * s.Likelihood

    sewers2.updateRow(s)
