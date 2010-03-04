import os
import time 
import math
from datetime import date
from myUnitDetails import *
def data_prep(bp):
	#This portion reads the categories which all units are assigned to and builds sets based on them
	categories = dict()
	for unit in bp.keys():
		temp_unit = bp.get(unit,99)
		if temp_unit != 99:
			temp_cats = temp_unit.get('Categories',99)
			if temp_cats != 99:
				for cat in temp_cats:
					if categories.get(cat,99) != 99:
						categories.get(cat).add(unit)
					else:
						categories[cat] = set()
						categories[cat].add(unit)
			else:
				print("bad unit: " + unit)
		else:
			print("bad temp unit")
	#Create the file structure needed for printing out the unitdb pages			
	#print(categories)
	direxist = False
	for dirs in os.listdir("."):
		if dirs == "Web_pages":
			direxist = True
	if direxist == False:
		os.mkdir("Web_pages")
	current_filepath=str(date.today())+"-"+str(int(time.time()))
	os.mkdir("./Web_pages/units"+current_filepath)
	os.mkdir("./Web_pages/units"+current_filepath+"/units")
	
	#begin index.html creation
	template = open("./index_template.html")
	page_string = template.read()
	template.close()
	
	races = ["'AEON'","'CYBRAN'","'UEF'","'SERAPHIM'"]
	tech_level = ["'TECH1'","'TECH2'","'TECH3'","'EXPERIMENTAL'"]
	cssnames = {"'AEON'":'aeon',"'CYBRAN'":'cybran',"'UEF'":'uef',"'SERAPHIM'":'seraphim'}
	#dev location
	imagesrc= "../../Strategic icons/"
	#live location
	#imagesrc= "./Strategic icons/"
	
	displayorder = ["Engineer","Building-factory","Building-economy","Building-weapon","Building-defense","Building-sensor","Aircraft","Vehicle","Ship","Support"]
	unitsets = {"Engineer": categories["'ENGINEER'"].difference(categories["'SUBCOMMANDER'"]).difference(categories["'AIR'"]), "Building-factory": categories["'STRUCTURE'"].intersection(categories["'FACTORY'"]), "Building-economy": categories["'ECONOMIC'"], "Building-weapon": categories["'STRUCTURE'"].intersection(categories["'DEFENSE'"]).difference(categories["'SHIELD'"]).difference(categories["'WALL'"]).difference(categories["'COUNTERINTELLIGENCE'"]).difference(categories["'ANTIMISSILE'"]).union(categories["'STRATEGIC'"]).difference(categories["'AIRSTAGINGPLATFORM'"]), "Building-defense":categories["'STRUCTURE'"].intersection(categories["'SHIELD'"]).union(categories["'COUNTERINTELLIGENCE'"]).union(categories["'ANTIMISSILE'"]).difference(categories["'MOBILE'"]), "Building-sensor": categories["'STRUCTURE'"].intersection(categories["'INTELLIGENCE'"]).difference(categories["'COUNTERINTELLIGENCE'"]).union(categories["'MOBILESONAR'"]), "Aircraft": categories["'AIR'"].difference(categories["'STRUCTURE'"]), "Vehicle": categories["'LAND'"].intersection(categories["'MOBILE'"]).difference(categories["'ENGINEER'"]), "Ship": categories["'NAVAL'"].difference(categories["'STRUCTURE'"]), "Support": categories["'WALL'"].union(categories["'AIRSTAGINGPLATFORM'"]).difference(categories["'MOBILE'"]).union(categories["'ORBITALSYSTEM'"])}
	
	#command
	page_string+="<tr><td class='black_table' colspan='4'>Command</td></tr><tr>"
	for race in races:
		page_string+="<td class="+race+">"
		for unit in categories["'COMMAND'"].intersection(categories[race]):
			if bp[unit].get("Interface",99) != 99:
				image_string = ""
				if bp[unit].get("StrategicIconName",99) != 99:
					image_string += "<img src='"+imagesrc+cssnames[race]+"_"+bp[unit]["StrategicIconName"][1:-1]+".png' style='border: 0pt none ;'>"
				
				page_string+="<a href='./units/"+unit+".html'><div>"+image_string+bp[unit]["Description"][bp[unit]["Description"].find('>')+1:-1]
				if bp[unit].get("General",99) != 99:
					if bp[unit]["General"].get("UnitName",99) != 99:
						page_string+=": "+bp[unit]["General"]["UnitName"][bp[unit]["General"]["UnitName"].find('>')+1:-1]
				
				page_string+="</div></a>"
		page_string+="</td>"
	page_string+="</tr><tr>"
	for race in races:
		page_string+="<td class="+race+">"	
		for unit in categories["'SUBCOMMANDER'"].intersection(categories[race]):
			if bp[unit].get("Interface",99) != 99:
				image_string = ""
				if bp[unit].get("StrategicIconName",99) != 99:
					image_string += "<img src='"+imagesrc+cssnames[race]+"_"+bp[unit]["StrategicIconName"][1:-1]+".png' style='border: 0pt none ;'>"
				
				page_string+="<a href='./units/"+unit+".html'><div>"+image_string+bp[unit]["Description"][bp[unit]["Description"].find('>')+1:-1]
				if bp[unit].get("General",99) != 99:
					if bp[unit]["General"].get("UnitName",99) != 99:
						page_string+=": "+bp[unit]["General"]["UnitName"][bp[unit]["General"]["UnitName"].find('>')+1:-1]
				
				page_string+="</div></a>"
		page_string+="</td>"
	page_string+="</tr>"

	#engineer
	#building-factory	
	#building-economy
	#building-weapon
	#building-defense
	#building-sensor
	#Aircraft
	#vehicle
	#Ship
	#Support
	#prints the unit groups in order defined by the list display order
	for group in displayorder:
		page_string+="<tr><td class='black_table' colspan='4'>"+group+"</td></tr>"
		for tier in tech_level:
			query = categories[tier].intersection(unitsets[group])
			if len(query) > 0: 
				page_string+="<tr>"
				for race in races:
					page_string+="<td class="+race+">"
					
					units = query.intersection(categories[race])
					sortedunits = list()
					sortedunits_bpids = dict()
					
					for unit in units:
						sortedunits.append(bp[unit]["Description"][bp[unit]["Description"].find('>')+1:-1])
						sortedunits_bpids[bp[unit]["Description"][bp[unit]["Description"].find('>')+1:-1]] = unit
					
					sortedunits.sort()
					for unit in sortedunits:
						if bp[sortedunits_bpids[unit]].get("Interface",99) != 99:
							image_string = ""
							if bp[sortedunits_bpids[unit]].get("StrategicIconName",99) != 99:
								image_string += "<img src='"+imagesrc+cssnames[race]+"_"+bp[sortedunits_bpids[unit]]["StrategicIconName"][1:-1]+".png' style='border: 0pt none ;'>"
							
							tier_string = ""
							if tech_level.index(tier)+1 < 4:
								tier_string = "T"+str(tech_level.index(tier)+1)+" "
							else:
								tier_string = "EX "
								
							page_string+="<a href='./units/"+sortedunits_bpids[unit]+".html'><div>"+image_string+tier_string+bp[sortedunits_bpids[unit]]["Description"][bp[sortedunits_bpids[unit]]["Description"].find('>')+1:-1]
							if bp[sortedunits_bpids[unit]].get("General",99) != 99:
								if bp[sortedunits_bpids[unit]]["General"].get("UnitName",99) != 99:
									page_string+=": "+bp[sortedunits_bpids[unit]]["General"]["UnitName"][bp[sortedunits_bpids[unit]]["General"]["UnitName"].find('>')+1:-1]
							
							page_string+="</div></a>"
					page_string+="</td>"
				page_string+="</tr>"

		#for units in categories[race].intersection("TECH1").intersection("LAND").intersection("MOBILE"):
		#	page_string+="<a href=#>"+units+"</a>"
	

	
	#begin creation of 
	page_string+="</table></body></html>"
	index = open("./Web_pages/units"+current_filepath+"/index.html",'w')
	index.write(page_string)
	index.close()
	
	unit_details(bp, "./Web_pages/units"+current_filepath+"/units/",categories)

	
	"""
["'ECONOMIC'", 
"'BENIGN'", 
"'TRANSPORTBUILTBYTIER2FACTORY'", 
"'TACTICALMISSILEPLATFORM'", 
"'COMMAND'", 
"'SORTDEFENSE'", 
"'BUILTBYTIER2ENGINEER'", 
"'WALL'", 
"'OMNI'", 
"'UEF'", 
"'ABILITYBUTTON'", 
"'NAVALCARRIER'", 
"'CAPTURE'", 
"'TRANSPORTFOCUS'", 
"'TRANSPORTATION'", 
"'CONSTRUCTIONSORTDOWN'", 
"'HOVER'", 
"'OVERLAYANTIAIR'", 
"'PODSTAGINGPLATFORM'", 
"'HIGHPRIAIR'", 
"'NAVAL'", 
"'T1SUBMARINE'", 
"'TRANSPORTBUILTBYTIER1FACTORY'", 
"'TECH3'", 
"'SCOUT'", 
"'REPAIR'", 
"'PRODUCTDL'", 
"'SORTINTEL'", 
"'BUILTBYTIER3FACTORY'", 
"'BOMBER'", 
"'MASSSTORAGE'", 
"'MASSEXTRACTION'", 
"'DRAGBUILD'", 
"'PRODUCTSC1'", 
"'SIZE16'", 
"'AIRSTAGINGPLATFORM'", 
"'OVERLAYANTINAVY'", 
"'STATIONASSISTPOD'", 
"'AIR'", 
"'TANK'", 
"'OVERLAYMISC'", 
"'FRIGATE'", 
"'OVERLAYDIRECTFIRE'", 
"'TECH2'", 
"'GATE'", 
"'TRANSPORTBUILTBYTIER3FACTORY'", 
"'SHIELD'", 
"'VISIBLETORECON'", 
"'STRUCTURE'", 
"'NUKESUB'", 
"'SIZE4'", 
"'RADAR'", 
"'BUILTBYTIER2FACTORY'", 
"'STRATEGIC'", 
"'BUILTBYLANDTIER2FACTORY'", 
"'ENERGYSTORAGE'", 
"'INSIGNIFICANTUNIT'", 
"'FACTORY'", "'HYDROCARBON'", 
"'HIGHALTAIR'", 
"'ORBITALSYSTEM'", 
"'SONAR'", 
"'BUILTBYCOMMANDER'", 
"'MASSFABRICATION'", 
"'PRODUCTFA'", 
"'RECLAIM'", 
"'RALLYPOINT'", 
"'OVERLAYCOUNTERINTEL'", 
"'OVERLAYINDIRECTFIRE'", 
"'BUILTBYTIER1FACTORY'", 
"'UNTARGETABLE'", 
"'SORTSTRATEGIC'", 
"'ENGINEERSTATION'", 
"'SHOWATTACKRETICLE'", 
"'ENERGYPRODUCTION'", 
"'MOBILESONAR'", 
"'ANTIMISSILE'", 
"'ENGINEER'", 
"'AEON'", 
"'BUILTBYEXPERIMENTALSUB'", 
"'FIELDENGINEER'", 
"'DIRECTFIRE'", 
"'ANTINAVY'", 
"'CONSTRUCTION'", 
"'EXPERIMENTAL'", 
"'RECLAIMABLE'", 
"'MASSPRODUCTION'", 
"'SATELLITE'", 
"'PATROLHELPER'", 
"'INDIRECTFIRE'", 
"'SIZE12'", 
"'SORTCONSTRUCTION'", 
"'SIZE20'", 
"'NEEDMOBILEBUILD'", 
"'CANTRANSPORTCOMMANDER'", 
"'VERIFYMISSILEUI'", 
"'COUNTERINTELLIGENCE'", 
"'BUILTBYTIER3ENGINEER'", 
"'BUILTBYTIER2COMMANDER'", 
"'OPTICS'", 
"'BUILTBYTIER1ENGINEER'", 
"'SUBCOMMANDER'", 
"'ARTILLERY'", 
"'BUILTBYQUANTUMGATE'", 
"'TARGETCHASER'", 
"'OVERLAYOMNI'", 
"'CARRIER'", 
"'BUILTBYTIER3COMMANDER'",
"'BOT'", 
"'LAND'", 
"'SUBMERSIBLE'", 
"'UNSELECTABLE'", 
"'ANTISUB'", 
"'CYBRAN'", 
"'DEFENSE'", 
"'CANNOTUSEAIRSTAGING'", 
"'NUKE'", 
"'GROUNDATTACK'", 
"'OVERLAYSONAR'", 
"'DESTROYER'", 
"'CRUISER'", 
"'TECH1'", 
"'FAVORSWATER'", 
"'SERAPHIM'", 
"'SELECTABLE'", 
"'SILO'", 
"'INTELLIGENCE'", 
"'POD'", 
"'ANTIAIR'", 
"'DEFENSIVEBOAT'", 
"'OVERLAYRADAR'", 
"'LIGHTBOAT'", 
"'BATTLESHIP'", 
"'BUILTBYLANDTIER3FACTORY'",
"'OVERLAYDEFENSE'", 
"'SHOWQUEUE'", 
"'T2SUBMARINE'", 
"'MOBILE'", 
"'SORTECONOMY'", 
"'REBUILDER'", 
"'SIZE8'"]"""
