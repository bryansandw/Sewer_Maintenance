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
import numpy
env.overwriteOutput = True
env.autoCancelling = False

## This is important! Where all of the outputs are saved! 
env.workspace = arcpy.GetParameterAsText(0)

##### Local variables: #####
### Data from Database will only be copied and not altered ###
# Used to use my database connection, but the layers work and this way other
# people in the city should be able to run the script without having to 
# change any of the variables
# This will be used in Process 1
SS_Lines = arcpy.GetParameterAsText(1) 
# This will be used in Process 2
All_WO = arcpy.GetParameterAsText(2) 
Streams = arcpy.GetParameterAsText(3) 
MAJOR_ROADS = arcpy.GetParameterAsText(4) 
BCAD_PARCELS = arcpy.GetParameterAsText(5) 
rm = arcpy.GetParameterAsText(6) 

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
#Risk_shp = env.workspace + "\\Risk.shp"
Risk_shp = arcpy.GetParameterAsText(14)

# the %s method didn't work correctly, although it may have been a "' issue
# need to try again
# I should consider having fieldmappings3 be an input instead of static...
def addMyField(my_string):
    """
    This function creates a numeric fieldmap with the input string.
    This field map creates a field in a feature class. 
    """
    string = '"' + my_string + '\"' + my_string + '\" true true false 9 Long 0 0 ,First,#;' 
    fieldmappings3.loadFromString(string)   
    my_variable = fieldmappings3.getFieldMap(fieldmappings3.findFieldMapIndex (my_string))
    return my_variable
	
def check4default(input, default):
    '''
    This function is intended to check if the input value is empty.
    If the input is not empty the function returns the input, if it 
    is empty the function returns the second value. 
    The tool GUI in ArcMap feeds default variables in as '' 
    so I need to handle it by checking if the variable is ''
    '''
    if input == '':
        return default
    else:
        return float(input)

def drange(start, stop, step):
    '''
    This function works similarly to range, but is also has a way to 
    handle decimals, or other iterators.  The starting number, the 
    ending number in the range, and how much to add to the start number
    until you get the stop number.  The output is a list. 
    '''
    list_range = [0]
    r = start
    while r < stop:
        if round(r, 1)%int(r) == 0.0:
            list_range.append(int(r))
        else:
            list_range.append(round(r, 1))
        r += step
    return list_range

def Weigh_lines(Risk_shp):
    sewers2 = arcpy.UpdateCursor(Risk_shp)

    arcpy.SetProgressorLabel("Create list of the risk values to identify the highest risk lines")
# Will use the current year to find ages of pipes
    year = datetime.date.today().year
	
    arcpy.SetProgressorLabel("Update fields with weights")


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
    #    arcpy.GetParameterAsText(12))
	# Check if the peramiter coming in is '' and set default position
	    #Potential for Large SSO
        plsso = arcpy.GetParameterAsText(15) #.3 
        PLSSO = check4default(plsso, 30)
        #Distance to Water
        d2w = arcpy.GetParameterAsText(16) #.4
        D2W = check4default(d2w, 40)
        #Disruption to Commuters
        d2c = arcpy.GetParameterAsText(17) # .1
        D2C = check4default(d2c, 10)
        #Impact to Community 
        i2c = arcpy.GetParameterAsText(18) # .2
        I2C = check4default(i2c, 20)
		
        t = ((PLSSO * s.Con_Size) + ( D2W * s.Con_Water) + \
            (D2C * s.Con_Road) + (I2C * s.Con_Pub))
        b = (PLSSO + D2W + D2C + I2C)
		
        s.Consequenc = int(t / b)
            
			
			
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
    # The current year is used find lines that are 30 yr old
    # Age less than 30 years
        if s.YEAR > year - 30: 
            s.Age_Con = 1
    # Age between 30 and 39 years
        elif s.YEAR > year - 40 and s.YEAR <= year - 30:
            s.Age_Con = 2
    # age between 40 and 49 years
        elif s.YEAR > year - 50 and s.YEAR <= year - 40:
            s.Age_Con = 4
    # age between 50 and 59 years
        elif s.YEAR > year - 60 and s.YEAR <= year - 50:
            s.Age_Con = 7
    # age greater than 60 years
        elif s.YEAR <= year - 60:
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
	    #Age Condition
        a_ss = arcpy.GetParameterAsText(19) #.05
        A_SS = check4default(a_ss, 5)
        #Physical Condition
        phc = arcpy.GetParameterAsText(20) #.35
        PhC = check4default(phc, 35)
        #WO Likelihood
        wol = arcpy.GetParameterAsText(21) # .15
        WOL = check4default(wol, 15)
        #WO Density 
        wod = arcpy.GetParameterAsText(22) # .2	
        WOD = check4default(wod, 20)
        #Home Values
        hv = arcpy.GetParameterAsText(23) # .1
        HV = check4default(hv, 10)
        #Potential for Stoppage
        s_l = arcpy.GetParameterAsText(24) # .15
        S_L = check4default(s_l, 15)
		
        t1 = ((PhC * s.Phy_Con) + (HV * s.Mark_Weigh) + \
             (A_SS * s.Age_Con) + (WOL * s.Failure_) + (WOD * s.Fail_Den) + \
             (S_L * s.STOP_like))
        b1 = ( A_SS + PhC + WOL + WOD + HV + S_L )
		
        s.Likelihood = t1 / b1

        s.Risk = s.Consequenc * s.Likelihood
	
        sewers2.updateRow(s)
    del sewers2
    return Risk_shp

def correctFieldName(shp_to_correct, list_of_fields, user_field, newName):
    '''
    This function only creates float fields.  
    '''
    field_index = list_of_fields.index(str(user_field))
    arcpy.AddField_management(shp_to_correct, newName, "FLOAT")
    arcpy.CalculateField_management(shp_to_correct, newName, '!' + \
        str(fields[field_index].name) + '!', "PYTHON", "")
    arcpy.DeleteField_management(shp_to_correct, 
        str(fields[field_index].name))
    return Risk_shp		
	
# This creates selects the SS_Line that are < 12 
# and outputs the copy as Sewer_2_shp
MAINSIZE = arcpy.GetParameter(7)
YEAR = arcpy.GetParameter(8)
SIZE = arcpy.GetParameterAsText(9)
arcpy.SetProgressorLabel("Select Sewer lines " + SIZE + " inches or less")

if isinstance(MAINSIZE, int) == True or isinstance(MAINSIZE, float) == True or \
   isinstance(MAINSIZE, long) == True or isinstance(MAINSIZE, complex) == True:
    SQL = str(MAINSIZE) + " <= " + str(SIZE)
    arcpy.Select_analysis(SS_Lines, Sewer_2_shp, SQL) 
    #"\"MAINSIZE\" <= 12"
else:
    mainsize_value = drange(1.0, float(SIZE), 0.5)
    SQL = "\"" + str(MAINSIZE) + "\" = '" + str(SIZE) +"'"
    for ms_value in mainsize_value:
        SQL += " OR \"" + str(MAINSIZE) + "\" = '" + str(ms_value) + "'"
    arcpy.Select_analysis(SS_Lines, Sewer_2_shp, SQL)
	
# This creates a shapefile of the work orders (All_WO) that have the 
# CATCODE STOP and the TASKCODE USG ect... and out puts the points 
# As WO_STOP_1
arcpy.SetProgressorLabel("Select STOPs")
arcpy.Select_analysis(All_WO, WO_STOP_1, arcpy.GetParameterAsText(11))

# The snapping environments set the rules for how the snap 
# function will snap features together
arcpy.SetProgressorLabel("Define snapping environments")
snapEnv1 = [SS_Lines, "EDGE", '50 Feet']
snapEnv2 = [SS_Lines, "EDGE", '100 Feet']
snapEnv3 = [SS_Lines, "EDGE", '150 Feet']
snapEnv4 = [SS_Lines, "EDGE", '200 Feet']
snapEnv5 = [SS_Lines, "EDGE", '250 Feet']
snapEnv6 = [SS_Lines, "EDGE", '300 Feet']
snapEnv7 = [SS_Lines, "EDGE", '350 Feet']
snapEnv8 = [SS_Lines, "EDGE", '400 Feet']

# The copy of the sewer STOP work orders are snapped to the sewer lines, by
# starting at 50 ft and working out at 50 ft intervals, the hope is that the
# majority of the WO points will end up snapped to the line where the wo 
# occurred, but the wo's do not identify what line they occurred on and only
# identify what address the wo occurred at
arcpy.SetProgressorLabel("Snap STOPs to Sewer")
arcpy.Snap_edit(WO_STOP_1, [
    snapEnv1, snapEnv2, snapEnv3, snapEnv4, 
    snapEnv5, snapEnv6, snapEnv7, snapEnv8
    ])

# Similar to 2nd Process, but selects SSO's instead the output file is
# WO_SSO_1
arcpy.SetProgressorLabel("Select SSOs")
arcpy.Select_analysis(All_WO, WO_SSO_1, arcpy.GetParameterAsText(12))

# Same as 4th process, but on WO_SSO_1 instead
arcpy.SetProgressorLabel("Snap SSOs to sewer")
arcpy.Snap_edit(WO_SSO_1, [
    snapEnv1, snapEnv2, snapEnv3, snapEnv4, 
    snapEnv5, snapEnv6, snapEnv7, snapEnv8
    ])

# This was the last snapping so I am deleting these variables	
del snapEnv1, snapEnv2, snapEnv3, snapEnv4
del snapEnv5, snapEnv6, snapEnv7, snapEnv8

# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
arcpy.SetProgressorLabel("Adding Field mappings")
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

# The spatial join creates a new shapefile that has the fields that were 
# added in the field mappings
arcpy.SetProgressorLabel("Spatial Join adding SSO WO to Sewer")
arcpy.SpatialJoin_analysis(Sewer_2_shp, WO_SSO_1, Sewer_SSO_shp,
    "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings)
del fieldmappings

# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
arcpy.SetProgressorLabel("Adding Field mappings")
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

arcpy.SetProgressorLabel("Spatial Join adding STOP WO and adding fields")
arcpy.SpatialJoin_analysis(Sewer_SSO_shp, WO_STOP_1, Sewer_SSO_STOP_shp,
    "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings1)
del fieldmappings1

arcpy.SetProgressorLabel("Adding Field mappings")
# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
fieldmappings2 = arcpy.FieldMappings()
fieldmappings2.addTable(Sewer_SSO_STOP_shp)
arcpy.SetProgressorLabel("Before adding fields there are " +  \
    str(fieldmappings2.fieldCount) + " fields")

fieldmappings3 = arcpy.FieldMappings()

# Need to handle Comp_Date if it has another name,
# or is not in date format
# Create two field maps from RM
# Handles Date type but not sting or unicode change here or at 760?
RM_Date = arcpy.GetParameterAsText(10)
Comp_Date = arcpy.FieldMap()
Comp_Date.addInputField(rm,RM_Date) 
CD = Comp_Date.outputField
if CD.type == u'Date':
    Comp_Date.mergeRule = 'max'
else:
    Comp_Date.mergeRule = 'last'
CD.name = "Comp_Date"
CD.aliasName = "Comp_Date"
Comp_Date.outputField = CD



# Rename the field and pass the updated field object back into the field map
RM_Count = arcpy.FieldMap()
RM_Count.addInputField(rm, "OBJECTID")
RM_Count.mergeRule = "count"
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

field_names = ['To_Water', 'To_Road', 'To_Low_Pub', 'To_Mod_Pub', 'To_High_Pu', 
    'DaySinRM', 'Con_Size', 'Con_Water', 'Con_Road',
    'Con_Pub', 'Consequenc', 'WO_Weight', 'STOP_like', 'Phy_Con', 'Age_Con', 
    'Failure_', 'Fail_Den', 'Likelihood', 'Risk']

field_list = [Comp_Date, RM_Count]
	
for n in field_names:
    n = addMyField(n)
    field_list.append(n)
	
# Add the field map to the field mapping object 


for f_l in field_list: 
    fieldmappings2.addFieldMap(f_l)

arcpy.SetProgressorLabel("After adding fields there are " +  \
    str(fieldmappings2.fieldCount) + " fields.")

arcpy.SetProgressorLabel("Spatial Join")
## Field 
arcpy.SpatialJoin_analysis(
    Sewer_SSO_STOP_shp, rm, WO_RM_shp, "JOIN_ONE_TO_ONE", "KEEP_ALL",
    fieldmappings2, "SHARE_A_LINE_SEGMENT_WITH", "", "")
del fieldmappings2
del fieldmappings3

arcpy.SetProgressorLabel("Near how close are the sewers to streams?")
# Adds a field to WO_RM_shp called NEAR_DIST that displays the distance in 
# feet between WO_RM_shp and the nearest Stream feature
arcpy.Near_analysis(WO_RM_shp, Streams, "", "NO_LOCATION", "NO_ANGLE",
    "PLANAR")

arcpy.SetProgressorLabel("Calculate To_Water Field")
# Pull the numbers from the NEAR_DIST field and use them to fill the
# currently empty To_Water field
arcpy.CalculateField_management(WO_RM_shp, "To_Water", "!NEAR_DIST!",
    "PYTHON", "")

arcpy.SetProgressorLabel("Near how close are the sewers to Major Roads?")
# Replaces the NEAR_DIST with a new field of the same name, this time
# displaying the distance in feet between WO_RM_shp and the nearest major
# road
arcpy.Near_analysis(WO_RM_shp, MAJOR_ROADS, "", "NO_LOCATION", "NO_ANGLE",
    "PLANAR")

arcpy.SetProgressorLabel("Calculate To_Road Field")
# Pull the numbers from the NEAR_DIST field and use them to fill the
# currently empty To_Road field
arcpy.CalculateField_management(WO_RM_shp, "To_Road", "!NEAR_DIST!",
    "PYTHON", "")

arcpy.SetProgressorLabel("Select commercial and residential")
# I experimented with how to select just commercial and residential areas
# I ended up using the F and B values in the state cd field, I do not know
# what these mean, so this could be improved
arcpy.Select_analysis(BCAD_PARCELS, parcels_select_shp,
    arcpy.GetParameterAsText(13))
#"state_cd = 'F1' OR state_cd = 'F2' OR state_cd LIKE 'A%' OR state_cd LIKE 'B%'")

arcpy.SetProgressorLabel("Add Field Type")
# Adding a text field called Type
arcpy.AddField_management(parcels_select_shp,"Type", "TEXT", "", "", "", "",
    "NULLABLE","NON_REQUIRED","")

arcpy.SetProgressorLabel("Create a Update Cursor to update the fields")
# Create a cursor that lists the features in the parcels file, this allows 
# the user to iterate through the shapefile
parcels = arcpy.UpdateCursor(parcels_select_shp)

arcpy.SetProgressorLabel("Classify the parcels land use type based on legal class," \
    " state_cd, and file as name.")
# Iterate through parcels and update the Type field based on the values found
# in other fields, some, like the golf type, I looked at visually and made
# sure that they were correctly categorized, others, such as the commercial
# density groups are just a best guess and could be improved

# This is a problem for my soft code!
# Need to address
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
 
arcpy.SetProgressorLabel("Select the low community impact areas, golf and" \
    " residential.")
# Use the new type field and classifications select the parcels that are golf
# or residential
arcpy.Select_analysis(parcels_select_shp, low_com_impact, 
    "\"Type\" = 'GOLF' OR \"Type\" = 'RESIDENTIAL'")

arcpy.SetProgressorLabel("23rd Process: Add Field Mark_Weight")
# Add field for market value weights to the low community impact file
arcpy.AddField_management(low_com_impact,"Mark_Weigh", "LONG", "", "", "",
    "","NULLABLE","NON_REQUIRED","")

# Make list of home values and find division points of 6 catigories
home_value = []
l_parcels = arcpy.SearchCursor(low_com_impact)	
for lp in l_parcels:
    home_value.append(lp.market)
del l_parcels	
home_value_sort = sorted(home_value)
list_len = len(home_value_sort)
fifth_1 = list_len / 6
fifth_2 = fifth_1 * 2
fifth_3 = fifth_1 * 3
fifth_4 = fifth_1 * 4
fifth_5 = fifth_1 * 5

home_arr = numpy.array(home_value_sort)
lowest_home = home_arr[fifth_1]
low_home = home_arr[fifth_2]
med_home = home_arr[fifth_3]
high_home = home_arr[fifth_4]
highest_home = home_arr[fifth_5]

# Create the cursor to iterate through the low community impact file
arcpy.SetProgressorLabel("Classify the parcels land values to weights")
low_parcels = arcpy.UpdateCursor(low_com_impact)

# Fill in the Mark_Weigh field based on the value of the market field
for p in low_parcels:
    if p.market > 0:
        if p.market < lowest_home:
            p.Mark_Weigh = 10
        elif p.market < low_home:
            p.Mark_Weigh = 7
        elif p.market < med_home:
            p.Mark_Weigh = 4
        elif p.market < ((high_home + highest_home) / 2 ):
            p.Mark_Weigh = 2   
        else:
            p.Mark_Weigh = 1  
    else:
        p.Mark_Weigh = 1  
    low_parcels.updateRow(p)

del low_parcels	


# Select the low density type parcels and export them as mod_com_impact file
# These are the moderate community impact parcels
arcpy.SetProgressorLabel("Select the moderate community impact areas," \
    " low density commercial.")
arcpy.Select_analysis(parcels_select_shp, mod_com_impact,
    "Type = 'LOW DENSITY COMMERCIAL'")

# Select the high density type parcels, the hospitals, and the schools and
# export them as high_com_impact file, these are the high community impact
# parcels
arcpy.SetProgressorLabel("Select the high community impact areas: " \
    "Hospitals, Schools, high density commercial.")
arcpy.Select_analysis(parcels_select_shp, high_com_impact, 
    "Type = 'HOSPITAL' OR Type = 'SCHOOL' OR Type = 'HIGH DENSITY COMMERCIAL'")

# Replaces the NEAR_DIST with a new field of the same name, this time
# displaying the distance in feet between WO_RM_shp and the low_com_impact
# parcels
arcpy.SetProgressorLabel("Near are the sewers near the low impact area?")
arcpy.Near_analysis(WO_RM_shp, low_com_impact, "", "NO_LOCATION", "NO_ANGLE",
    "PLANAR")

# Pull the numbers from the NEAR_DIST field and use them to fill the
# currently empty To_Low_Pub field
arcpy.SetProgressorLabel("Calculate Field fill To_Low_Pub with distance.")
arcpy.CalculateField_management(WO_RM_shp, "To_Low_Pub", "!NEAR_DIST!",
    "PYTHON", "")

# Replaces the NEAR_DIST with a new field of the same name, this time
# displaying the distance in feet between WO_RM_shp and the mod_com_impact
# parcels
arcpy.SetProgressorLabel("Near are the sewers near the moderate community" \
    " impact area?")
arcpy.Near_analysis(WO_RM_shp, mod_com_impact, "", "NO_LOCATION", "NO_ANGLE",
    "PLANAR")

# Pull the numbers from the NEAR_DIST field and use them to fill the
# currently empty To_Mod_Pub field
arcpy.SetProgressorLabel("Calculate Field")
arcpy.CalculateField_management(WO_RM_shp, "To_Mod_Pub", "!NEAR_DIST!",
    "PYTHON", "")

# Replaces the NEAR_DIST with a new field of the same name, this time
# displaying the distance in feet between WO_RM_shp and the high_com_impact
# parcels
arcpy.SetProgressorLabel("Near are the sewers near the high community" \
    " impact area?")
arcpy.Near_analysis(WO_RM_shp, high_com_impact, "", "NO_LOCATION",
    "NO_ANGLE", "PLANAR")

# Pull the numbers from the NEAR_DIST field and use them to fill the
# currently empty To_High_Pu field
arcpy.SetProgressorLabel("Calculate To_High_Pu Field")
arcpy.CalculateField_management(WO_RM_shp, "To_High_Pu", "!NEAR_DIST!",
    "PYTHON", "")

# Deleting the fields that will no logger be needed 
arcpy.SetProgressorLabel("Delete Field")
arcpy.DeleteField_management(WO_RM_shp, "NEAR_FID;NEAR_DIST")

# Fill the WO_Weight field with the sum of the SSO_Count field multiplied by
# 3 and the number in the STOP_Count field.  This will be used later to find
# the WO hot spots, SSOs are more important, which is why they are weighted 
arcpy.SetProgressorLabel("Calculate Field WO_Weight")
arcpy.CalculateField_management(WO_RM_shp, "WO_Weight", 
    "(!SSO_Count! * 3) + !STOP_Count!", "PYTHON", "")


# Hot Spot analysis can not be performer on polylines, so a buffer is
# performed with a 50 ft radius and output as SS_Buffer_shp
arcpy.SetProgressorLabel("Buffer 50ft from RM")
arcpy.Buffer_analysis(WO_RM_shp, SS_buffer_shp, "50 Feet", "FULL", "ROUND",
    "NONE", "")

# The output, low_com_imp_buff, will be used later to determine the relative
# values of the residential areas that feed sewer lines, many sewer lines 
# are not in the parcels themselves, but are in the public areas near parcels
arcpy.SetProgressorLabel("Buffer 50ft from low community impact")
arcpy.Buffer_analysis(low_com_impact, low_com_imp_buf, "50 Feet", "FULL", 
    "ROUND", "NONE", "")

# If the Hot Spot Analysis is run in ArcMap or ArcCataloge the python script
# will abort after finishing running this process.  The Hot Spot analysis is
# run on the WO_Weight values. 
arcpy.SetProgressorLabel("Optimized Hot Spot Analysis")
arcpy.OptimizedHotSpotAnalysis_stats(SS_buffer_shp, SS_Buffer_HS_shp,
    "WO_Weight", "", "", Density_Surface)

# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
arcpy.SetProgressorLabel("Create field mapping for Spatial Join")
fieldmappings4 = arcpy.FieldMappings()
fieldmappings4.addTable(WO_RM_shp)
Gi_Bin = arcpy.FieldMap()
Gi_Bin.addInputField(SS_Buffer_HS_shp,"Gi_Bin") 
Gi_Bin.mergeRule = "first"
fieldmappings4.addFieldMap(Gi_Bin) 

# The results of the Hot Spot analysis are added to the WO_RM_shp file with
# the spatial join.  This is needed to return the format to a polyline 
# format instead of a polygon format. 
arcpy.SetProgressorLabel("Spatial Join")
arcpy.SpatialJoin_analysis(WO_RM_shp, SS_Buffer_HS_shp, WO_RM_HS_join_shp,
    "JOIN_ONE_TO_ONE", "KEEP_COMMON", fieldmappings4, "INTERSECT", "", "")
del fieldmappings4

arcpy.SetProgressorLabel("Create Cursor find the number of days since RM took place")
maintenance = arcpy.UpdateCursor(WO_RM_HS_join_shp)

for m in maintenance:
    if m.Comp_Date is None:
        m.DaySinRM = 99999
	# All are coming back as 0 on string data types.
    elif isinstance(m.Comp_Date, basestring):
        arcpy.SetProgressorLabel("Is instance basestring")
        if '/' in m.Comp_Date:
            rm_date = m.Comp_Date.split('/')
            dif = datetime.datetime.now()- datetime.datetime(int(rm_date[2]), int(rm_date[0]), int(rm_date[1]), 00, 00, 00)
            m.DaySinRM = dif.days
        elif '-' in m.Comp_Date:
            rm_date = m.Comp_Date.split('-')
            dif = datetime.datetime.now()- datetime.date(int(rm_date[2]), int(rm_date[0]), int(rm_date[1]), 00, 00, 00)
            m.DaySinRM = dif.days
        else:
            m.DaySinRM = 99999
    else:
        dif = datetime.datetime.now()- m.Comp_Date
        m.DaySinRM = dif.days
    maintenance.updateRow(m)
del maintenance

# Create a new fieldmappings and add the input feature classes.
# This creates field map objects for each field in the sewer file.
arcpy.SetProgressorLabel("Create field mapping for Spatial Join")
fieldmappings5 = arcpy.FieldMappings()
fieldmappings5.addTable(WO_RM_HS_join_shp)
Mark_Weigh = arcpy.FieldMap()
Mark_Weigh.addInputField(low_com_imp_buf,"Mark_Weigh") 
Mark_Weigh.mergeRule = "mean"
fieldmappings5.addFieldMap(Mark_Weigh) 

Mark_Value = arcpy.FieldMap()
Mark_Value.addInputField(low_com_imp_buf,"market") 
Mark_Value.mergeRule = "mean"
fieldmappings5.addFieldMap(Mark_Value) 

arcpy.SetProgressorLabel("Spatial Join")
arcpy.SpatialJoin_analysis(WO_RM_HS_join_shp, low_com_imp_buf, Risk_shp,
    "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings5, "INTERSECT", "", "")
del fieldmappings5

# Create a cursor to iterate through the risk file
arcpy.SetProgressorLabel("Create a Update Cursor to update the fields")
fields = arcpy.ListFields(Risk_shp)
str_field = []
for field in fields:
    str_field.append(field.baseName)
# Check if the users data fields have the same names or if 
# the field names need to be corected for the code to run
if 'MAINSIZE' in str_field and 'YEAR' in str_field:
    Weigh_lines(Risk_shp)
# YEAR field name is same, but MAINSIZE is different
elif 'YEAR' in str_field:
    correctFieldName(Risk_shp, str_field, MAINSIZE, "MAINSIZE")	
    Weigh_lines(Risk_shp)
# MAINSIZE field name is same, but YEAR is different	
elif 'MAINSIZE' in str_field:
    correctFieldName(Risk_shp, str_field, YEAR, "YEAR")	
    Weigh_lines(Risk_shp)
# YEAR and MAINSIZE field names are different	
else:
    correctFieldName(Risk_shp, str_field, MAINSIZE, "MAINSIZE")	
    correctFieldName(Risk_shp, str_field, YEAR, "YEAR")	
    Weigh_lines(Risk_shp)	

'''This should work, but it says : Invalid value type for parameter field
    
    for field1 in fields:
         if field1.name == str(fields[field_index].name):
            #print "Found"
            arcpy.AlterField_management(fc, field1, 'MyMS', 'my mainsize')
'''
dropFields = ["Join_Count", "TARGET_FID", "Join_Cou_1", "TARGET_F_1",
              "Join_Cou_2", "TARGET_F_2", "Join_Cou_3", "TARGET_F_3",
              "Join_Cou_4", "TARGET_F_4"]
arcpy.DeleteField_management(Risk_shp, dropFields)

### Delete Shapefiles that are no longer needed ### 
toDelete = [Sewer_2_shp, WO_STOP_1, WO_SSO_1, Sewer_SSO_shp,
        Sewer_SSO_STOP_shp, parcels_select_shp, low_com_impact,
        mod_com_impact, high_com_impact, WO_RM_shp, SS_buffer_shp,
        WO_RM_HS_join_shp]
 
for shp_file in toDelete:
    arcpy.Delete_management(shp_file, "")
