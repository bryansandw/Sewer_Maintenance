# Implementing a risk based GIS prioritization model to optimize routine maintenance of the sanitary sewer system. 
Elizabeth Rentschlar, *GIS Analyst for Water Distribution*

City of Bryan
10/29/15

##Abstract:
As sewer systems age, it becomes increasingly important to have a routine maintenance program that cleans the system regularly.  The EPA and TCEQ recognize that cleaning is the primary method to reduce Sanitary Sewer Overflows (SSOs).  High numbers of SSOs may result in enforcement actions such as Administrative Orders and Consent Decrees that require aggressive cleaning programs and schedules.  Without an effective asset management system, enforcement action will normally consist of a requirement to clean 100% of the system in 5 to 7 years.  Mandated efforts to clean the entire pipe system treat all pipes equally, resulting in cleaning of clean pipe and cleaning of pipe that have no history of blockage or SSOs. The old program in the City of Bryan was reactionary - using customer identified problems along with the Compliance (I&I) Supervisor and the field crew’s knowledge of historical problems to determine where routine maintenance should be performed.  

Geographic information systems (GIS) and extensive data collection provide a solution to the selection of sewer system lines for routine maintenance.  A risk based prioritization model provides an objective methodology for selecting segments of the sewer network for routine maintenance.  This model is intended to augment the Compliance (I&I) Supervisor and field crew’s decision making; the model is NOT intended to provide the sole means of selecting lines that should receive maintenance or determining the frequency of cleaning.  By creating the model with ArcGIS and Python, the city was able to avoid additional investment in software and utilize the capabilities of the system already in place.  This paper will provide a methodology that other communities could use to implement risk based sewer cleaning to reduce the occurrence of blockages and SSOs.

##Introduction:
Line cleaning programs maintain sewer line flow velocity, help prevent sewage from becoming septic, and reduce the number of stoppages and sanitary sewer overflows (SSO).  Routine maintenance (RM) of the sewer system (SS) can reduce the number of emergency repairs to the system by as much as 85% (TEEX 2013).  The City of Bryan maintains 388 miles of sewer line, 306 of which are narrow enough that they require RM to prevent buildup of solids.  In fiscal year 2010, the City of Bryan intensified the number of miles that they performed RM on each year and increased the number of smoke tests in an effort to decrease the number of SSOs.  The department now cleans 75 to 90 miles of the sewer system a year.  Currently the City of Bryan uses field observations, work orders, and reports from citizens to determine where to perform RM.  This has been reasonably successful with decrease in SSOs from 116 in 2010 to 39 in 2014, but leaves room for additional reductions by targeting areas for RM that have a higher risk of becoming a problem.  
##The Problem:
The number of miles of sewer cleaned each year suggests that the entire system is cleaned every 4 to 5 years; unfortunately, this is not the case.  The RM occurs at a higher rate in the neighborhoods that are perceived to have higher rates of sewer stops and overflows and are easy for the field crews to access.  Of the sewer lines less than 12 inches, 131 miles of the SS have not been cleaned in the 7 years that we have GIS records -  this is 42 % of the cleanable SS. This failure to clean segments of the SS sets the city up for failure in the future as our infrastructure continues to age.  Setting up a schedule to clean the lines in a sequential order is not a realistic solution because it would not adequately address areas that have historically had problems.  
##Solution:
Geographic information systems (GIS) and extensive data collection provide a solution to the selection of SS lines for RM.  The water department’s GIS Analyst (or should it just be the department? Or I ) built an SSO and sewer stop risk model using the data that was created and maintained by the GIS Technician.  The risk of SSOs and sewer stoppages is defined in this paper as Consequence of an SSO x Likelihood of an SSO or sewer stop.  A python script was written using ENVI’s arcpy module to produce pdf maps of the highest risk sewer lines.  The script can be found at https://github.com/bryansandw/Sewer_Maintenance.  The pdf maps are printed and given to the Compliance (I&I) Supervisor to use in assigning areas for the jet and vacuum trucks to clean.  The pdf maps have signature lines for the field crews to sign and return to the office.
##Methodology:
Data Acquisition and Maintenance: 
The risk model uses sewer line data, sewer manhole data, RM data, work order (WO) data, stream data, road data, and parcel data.  The City of Bryan has an all pipes GIS sewer model.  The sewer feature class contains detailed information about the individual segments of sewer line, such as the year its diameter, year it was installed, material, etc.  When new lines are constructed this information is added to the GIS.  RM is a separate feature class from the sewer lines.  At one time RM was logged in a field in the sewer class, but this did not allow for frequency information to be collected or account for lines that were only partially cleaned.  The WO data is geocoded by IT from the HTE database that is updated through green screen by the admin staff.  The Stream data comes from FEMA, the road data comes from the City IT department, and the parcel data comes from the County Appraisal District (CAD), some of the contained data is the owner name, value of the property, and tax category. 
##Risk Model:
The risk model takes the existing GIS data and creates new features that provide information to create a consequence score and a likelihood score that are multiplied to create the risk score that is used to prioritize sewer line maintenance. The risk model variables and weights are based on the risk model from Flores et al. 2011, with some changes where the City of Bryan did not have the same data available, or we believed we had additional information that should be used in assessing the risk of SS problems.  
###Consequence:
The consequence score quantifies what areas a SSO would be the most detrimental to the community (Table 1).  The score is based on four categories: Potential for Large SSO, Distance to Water, Disruption to Commuters, and Impact to Community (Figure 1.).  
  1.	The **size of the SS lines** is used in the model as an indication of the amount of wastewater that could potentially be spilled by that line.  Larger spill require more time and man power to clean, so is given a 30% weight.
  2.	The **distance to the streams** is given the greatest weight for the consequence score with 40%.  If a SSO reaches the water ways   it must be reported to the state and could increase oversite of the city by the Texas Commission of Environmental Quality (TCEQ).
  3.	**Impact to commuters** is a minor consideration with a weight of only 10 % it is worth including because of its high visibility to the larger community.
  4.	**Impacts on the community** are scored 20%, their weights are based on the proximity of the SS to different land use types, for example, lines that are close to schools and hospitals are given higher weights than SS lines near golf courses.

![Figure 1. Consequence](http://c2.staticflickr.com/2/1603/23755755583_875ddfdd9e.jpg)
**Figure 1.** The Potential for Large SSO, Distance to Water, Disruption to Commuters, and Impact to Community are show on the left and the resulting consequence score is sown on the right.

Consequence	| Data Used |	Weight |	1 Values |	4 values |	7 Values |	10 Values |	Field Name
------------|-----------|--------|----------|----------|----------|-----------|-----------
Potential for Large SSO	| Size of Sewer |	30%	| MAINSIZE <= 4 in	| MAINSIZE > 4 in and MAINSIZE <= 6 in	| MAINSIZE > 6 in and MAINSIZE <= 8 in	| MAINSIZE > 8 in	 | Con_Size
Distance to Water	| FEMA Stream 	| 40%	| To_Water > 1000 ft	| To_Water > 500 ft and To_Water <= 1000 ft	| To_Water > 100 ft and To_Water <= 500 ft	| To_Water <= 100 ft	| Con_Water
Disruption to Commuters	| Major Roads	| 10%	| To_Road > 50ft and To_Road <= 100ft	| To_Road > 20 ft and To_Road <= 50 ft	| To_Road > 5 ft and To_Road <= 20 ft	| To_Road <= 5 ft	| Con_Road
Impact to Community | Parcel	| 20%	| Near Open Spaces or Parks |	Near Residential and Golf Courses |	Near Low Density Commercial	| Near Hospital, School, High Density Commercial |	Con_Pub


**Table 1.** Shows the four consequence categories and the breakdown of their weight assignments and percentages.  

###Likelihood:
The likelihood score quantifies the lines that have a greater likelihood of presenting a problem.  The model uses six categories: the age of the SS lines, the historic RM data, the historic WO information, the values of the homes around the SS lines, and the size of the SS lines.  The historic WOs are used to find the WO Likelihood and the WO density categories.  The WOs used are the public sewer stops as a result of debris, grease, and roots and the public SSOs as a result of capacity, pipe failure, pump station failure, debris, grease, and roots.  
  1.	The **ages of the SS lines** are determined by the difference between the current year and the year that the line was installed.  The majority of pipe is expected to have a 50 year useful life expectancy, for this reason the pipes that are 50 or older are given higher weights and the pipes that are younger than 50 are given lower weights.  The Compliance (I&I) Supervisor did not deem the age as a major factor in stoppages or SSOs, so it was given low percentage of the likelihood score at 5% of the total.
  2.	The **historic RM data** is used to gauge the physical condition of the pipes.  The lines that have been cleaned in the last three years are given low values and the lines that have not been cleaned more than three years are given high values.  Because one of the main objectives of this project is to decrease the time between line cleanings this is given a high weight, 35%, in determining the likelihood score.
  3.	The **WO likelihood** category is simply the location of historic WOs.  Stoppages are assigned low values and lines that have had SSOs are assigned high values.  This is simple metric that ignores relationships between segments of sewer line, so it is assigned a low weight in determining the likelihood score, 15% of the total. 
  4.	The **WO density** category is based on a Hot Spot analysis run on a count of the number of WOs that are associated with each line.  SSOs were worth three points and stops were worth a single point.  The areas where there is a 90% or better confidence that the WOs are clustered are given higher values and the not significant and the cold spots with 90% confidence and greater were assigned lower values.  This is a more complex metric that takes the sewer lines spatial relationships into account, so it is assigned a higher weight than the WO likelihood score in determining the likelihood score, 20% of the total.
  5.	The **values of the homes** are used as a proxy for the relative flow rate of the sewer lines in the area and for the amount of grease that is being washed down the drains.  Because this is not a direct measurement of either of these factors this category is given a low weight of 10% of the Likelihood score.  
  6.	The **size of the SS line** is related to the likelihood of the line becoming stopped.  Smaller lines are usually near the ends of the sewer system so have less regular flow; this increases the chance that solids will become lodged in the line creating stoppages so they are given greater weights in determining the size score.  The size score makes up 15% of the likelihood score.

![Figure 2. Likelihood](https://farm2.staticflickr.com/1720/24382560795_7214aca1d0_z.jpg)

**Figure 2.** 

Likelihood | Dada Used	| Weight	| 1 Value	| 2 Value	| 4 Value	| 7 Value	| 10 Value	| Field Name
-----------|------------|---------|---------|---------|---------|---------|-----------|-----------
Age Condition	| Age of Sewer	| 5%	| Age < 30 yr	| 30 to 39 yr	| 40 to 49 yr	| 50 to 59 yr	| Age > 60 yr	| Age_Con
Physical Condition	| RM	| 35%	| < 366 days since RM	| 366 - 731 days since RM	| 731 -1097 days since RM	| 1097 -1460 days since RM | 	1460+ days since RM	| Phy_Con
WO Likelihood	| SSO and STOP WO	| 10%	| None	| 1 STOP	| >= 2 STOPs	| 1 SSO	| >= 2 SSO	| Failure_
WO Density |	SSO and STOP WO ***	| 30%	| Gi_Bin < 0	| Gi_Bin == 0	| Gi_Bin > 0	| Gi_Bin > 1	| Gi_Bin > 2	| Fail_Den
Home Values	| Parcels	| 10%	| Market >= $230,000	| Market < $230,000	| Market < $165,000	| Market < $130,000	| Market < $75,000	| Mark_Weigh
Potential for Stoppage	| Size of Sewer	| 10%	| None	| MAINSIZE >8 in and MAINSIZE < 12 in | MAINSIZE > 6 in and MAINSIZE < =8 in	| MAINSIZE > 4 in and MAINSIZE < =6 in	| MAINSIZE <= 4 in	| STOP_like

**Table 2.** shows the breakdown of the six likelihood categories and the weight assignments and percentages.  

*** Count of WO occurring on line where STOPs are worth 1 point and SSOs are worth 3 point. Ran Hot Spot analysis on the WO_weights.  Gi_Bin is the confidence level that the line is in a statistically significant cluster.

##Map Automation:
The Risk model provides a large amount of information to GIS users with an intermediate skill level with the software, but it requires time to look at the data produced and make decisions based upon it.  To cut down on the amount of time the Compliance (I&I) Supervisor would need to spend examining the data produced by the model it was decide to output the highest risk lines as pdf maps.  There is an ArcMap mxd file that holds the layers symbology and map layout.  The script alters this mxd to create new maps that are exported to a folder.  The scale adjusts based on the size of the sewer line that is being singled out for RM.  
The output maps highlight the segment of the sewer that needs to be cleaned and show the manholes that are connected to the line segment.  This helps prevent any confusion that the user of the map might have about what sewer line on the map needs the cleaning.  The upper right hand corner of the map displays the maintenance district and quadrant and the date on which the map was produced.  The district and quadrant are only used for the sewer maintenance district and represent 10 districts separated into 4 quarters each with about 8 miles of line.  These districts and quadrants help the Compliance (I&I) Supervisor group the maps into geographic groups without requiring him to look at the manholes on the map.  
##Implementation:
The pilot began in the last month of FY 2015.  The GIS Analyst would run the python script and manually open and print each pdf map.   The original plan was to provide the Compliance (I&I) Supervisor with the pdf maps every Monday morning, but this was not enough time for the lines to be cleaned and returned to the office staff to be processed before the next set of maps was produced.  2 weeks?  




 
![Figure 3. Risk](https://farm2.staticflickr.com/1481/24382561545_727c6f4076_b.jpg)





 
##Citations:
Texas A&M Engineering Extension Service [TEEX]. "Module 6: Maintenance and Operation." Wastewater Collection. N.p.: n.p., 2013. 6-7. Print. Infrastructure Training & Safety Institute.

Flores, Michael, Joanne Siew, and Jonathan Lee. "RISK-BASED PRIORITIZATION FOR SEWER MAINTENANCE AND CAPITAL IMPROVEMENTS." 19th Annual Sharing Technologies Seminar (2011): 1-9. The Northern California Pipe User’s Group. The Northern California Pipe User’s Group, 17 Feb. 2011. Web. 16 Sept. 2015.

