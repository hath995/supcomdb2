import os

def ct(title,array_string, version, qua,count=1):
	if version == 0:
		return title+"<span class='blue'>"+str(array_string)+qua+"</span>"
	elif version == 1:
		return title+"<span class='blue'>"+str(array_string)+"</span> / "+"<span class='blue'>"+array_string+qua+"</span>"
	elif version == 2:
		page_s = title+"<span class='blue'>"+str(array_string)
		dist = float(array_string)*19.5
		if dist > 1000:
			page_s += " (%(val).1fkm)"%{'val':float(dist/1000)}
		else:
			page_s += " (%(val).1fm)"%{'val':float(dist)}
		page_s += "</span>"
		return page_s
	# 1 unit = 19.55m
	elif version == 3:
		page_s = title+"<span class='blue'>"+str(array_string)
		dist = float(array_string)*19.5
		page_s += "("+str(dist)+qua+")"
		page_s += "</span>"
		return page_s
	elif version == 4:
		page_s = title+"<span class='blue'>"+str(float((10.0+count)/10)*float(array_string))+qua+" (+"+str(float(count/10.0)*float(array_string))+qua+")</span>"
		return page_s
	elif version == 5:
		return title+"<span class='green'>+"+str(array_string)+qua+"</span>"
	elif version ==  6:
		return title+"<span class='red'>-%(val).1f%(qua)s</span>"%{'val':float(array_string),'qua':qua}
	#colors text the easy way
	#case 0 generic color (blue)
	#case 1 value / value quantifier (blue)
	#case 2 distance/speed +(conversion + m/km) (blue)
	#case 3 dist + (conversion) + quantifier
	#case 4 special for printing out health of veterancy
	#case 5 green text for positive mass or energy production
	#case 5 red text for energy or mass consumption
	
def cdiv():
	return "<div>"
	
def ediv():
	return "</div>"
	
def unit_details(bp,filepath, categs):
	builtby = dict()
	for xunit in bp.keys():
		builtby[xunit] = set()
	
	for zunit in bp.keys():
		theunit = bp[zunit]
		if 'BuildableCategory' in theunit['Economy']:
			if 'BuildRate'in theunit['Economy']:
				buildables = set()
				for cats in theunit['Economy']['BuildableCategory']:
					tempcats = cats[1:-1].split(' ')
					buildtemp = set()
					
					if len(tempcats) > 1:
						tempcats[0] = "'"+tempcats[0]+"'"
						buildtemp = categs[tempcats[0]]
						for i in range(1,len(tempcats)):
							tempcats[i] = "'"+tempcats[i]+"'"
							buildtemp = buildtemp.intersection(categs[tempcats[i]])
							
						buildables = buildables.union(buildtemp)
					else:
						buildables.add(tempcats[0])
				if len(buildables) > 0:
						
					for buildee in buildables:
						if buildee != 'URL0001UPGRADE':
							builtby[buildee].add(zunit)
					
				bp[zunit]['Buildables'] = buildables
			else:
				print zunit
	#print(builtby)
		
					
	for unit in bp.keys():
		page_s = ''
		pagetempl = open('./unit_template.html')
		page_s = pagetempl.read()
		pagetempl.close()
		c_unit = bp[unit]
		#live location
		#imgsrc = '../Strategic icons/'
		#dev location
		imgsrc = '../../../Strategic icons/'
		#header
		page_s +="<div class='unit_pic_div'>"
		page_s +="<img class='unit_pic' src='"+imgsrc+c_unit['General']['Icon'][1:-1]+"_up.png' />"
		page_s +="<img class='unit_pic' src='"+imgsrc+unit+"_icon.png' />"
		page_s +=ediv()
		
		page_s += "<div class='bigfont'><div style='float: left;'>"
		page_s += "<img height='34' src='"+imgsrc+c_unit['General']['FactionName'][1:-1].lower()+"_"+c_unit["StrategicIconName"][1:-1]+".png' style='border: 0pt none ;'></div>"
		techstr = ""
		page_s += c_unit['General']['FactionName'][1:-1]+" "+techstr + c_unit["Description"][c_unit["Description"].find('>')+1:-1]
		if 'UnitName' in c_unit['General']:
			page_s += ": "+c_unit['General']["UnitName"][c_unit["General"]["UnitName"].find('>')+1:-1]
		page_s +="</div><div style='clear: both;'></div>"
		"""
		Icon = 'amph','land''sea','air'

		"""
		
		if 'Defense' in c_unit:
			page_s += cdiv()
			page_s += "<b>Health: </b>"
			page_s += ct("",c_unit['Defense']['MaxHealth'],1,"hp")
			if 'RegenRate' in c_unit['Defense']:
				page_s += " ("+ct("Regen rate: ",c_unit['Defense']['RegenRate'],0,"hp/s")+", "
			else:
				page_s += " ("+ct("Regen rate: ",0,0,"hp/s")+", "
			page_s +=ct("Armor type: ",c_unit['Defense']['ArmorType'][1:-1],0,"")+")"
			page_s += ediv()
			if 'Shield' in c_unit['Defense']:
				page_s += cdiv()
				page_s += "<b>Shield: </b>"
				page_s += ct("",c_unit['Defense']['Shield']['ShieldMaxHealth'],0,"hp") +" "
				page_s += ct("(size: ",c_unit['Defense']['Shield']['ShieldSize'],2,"") +", "
				page_s += ct("regen rate: ",c_unit['Defense']['Shield']['ShieldRegenRate'],0,"hp/s")+", "
				page_s += ct("regen start time: ",c_unit['Defense']['Shield']['ShieldRegenStartTime'],0,"s")+", "
				page_s += ct("recharge time: ",c_unit['Defense']['Shield']['ShieldRechargeTime'],0,"s")+", "
				page_s += ct("recharge rate: ",float(c_unit['Defense']['Shield']['ShieldMaxHealth'])/float(c_unit['Defense']['Shield']['ShieldRechargeTime']),0,"s")+")"
				page_s += ediv()

			
		if 'Abilities' in c_unit['Display']:
			page_s += cdiv()
			page_s += "<b>Abilities: </b>"
			for abils in c_unit['Display']['Abilities']:
				if abils == c_unit['Display']['Abilities'][0]:
					page_s += ct("",abils[1:-1],0,"")
				else:
					page_s += ", "+ct("",abils[1:-1],0,"")
			page_s += ediv()
			
		if 'Economy' in c_unit:
			page_s += cdiv()
			page_s += "<b>Economy: </b>"
			page_s += ct("mass: ",c_unit['Economy']['BuildCostMass'],0,"")
			page_s += " ("
			if 'ProductionPerSecondMass' in c_unit['Economy']:
				page_s += ct("",c_unit['Economy']['ProductionPerSecondMass'],5,"")
			else:
				page_s += ct("",0,5,"")
				
			if 'StorageMass' in c_unit['Economy']:
				page_s += ct(", storage: ",c_unit['Economy']['StorageMass'],0,"")
			page_s += ")"
			
			page_s += ct(", energy: ",c_unit['Economy']['BuildCostEnergy'],0,"")
			page_s += " ("
			if 'ProductionPerSecondEnergy' in c_unit['Economy']:
				page_s += ct("",c_unit['Economy']['ProductionPerSecondEnergy'],5,"")
			elif 'MaintenanceConsumptionPerSecondEnergy' in c_unit['Economy']:
				page_s += ct("",c_unit['Economy']['MaintenanceConsumptionPerSecondEnergy'],6,"")
			else:
				page_s += ct("",0,5,"")
				
			if 'StorageEnergy' in c_unit['Economy']:
				page_s += ct(", storage: ",c_unit['Economy']['StorageEnergy'],0,"")
			page_s += ")"
			
			page_s += ct(", build time: ",c_unit['Economy']['BuildTime'],0,"")
			
			if 'BuildRate' in c_unit['Economy']:
				page_s += ct(", build rate: ",c_unit['Economy']['BuildRate'],0,"")
			if 'MaxBuildDistance' in c_unit['Economy']:
				page_s += ct(", build radius: ",c_unit['Economy']['MaxBuildDistance'],0,"")
			page_s += ediv()
			
			"""
			BuildCostEnergy = 307500,
			BuildCostMass = 24600,
			BuildRate = 180,
			BuildTime = 18450,
			BuildableCategory = {
			    'BUILTBYTIER3FACTORY UEF MOBILE LAND',
			    'BUILTBYTIER2FACTORY UEF MOBILE LAND',
			    'BUILTBYLANDTIER2FACTORY UEF MOBILE LAND',
			},
			MaintenanceConsumptionPerSecondEnergy = 500,
			StorageEnergy = 1000,
			StorageMass = 200,
			
			ProductionPerSecondEnergy = 10,
			ProductionPerSecondMass = 1,


			"""
			
		if 'Intel' in c_unit:
			page_s += cdiv()
			page_s += "<b>Intel: </b>"
			if 'VisionRadius' in c_unit['Intel']:
				page_s += ct("vision radius: ",c_unit['Intel']['VisionRadius'],2,"")
			if 'RadarRadius' in c_unit['Intel']:
				page_s += ", "+ct("radar radius: ",c_unit['Intel']['RadarRadius'],2,"")
			if 'OmniRadius' in c_unit['Intel']:
				page_s += ", "+ct("omni radius: ",c_unit['Intel']['OmniRadius'],2,"")
			if 'SonarRadius' in c_unit['Intel']:
				page_s += ", "+ct("sonar radius: ",c_unit['Intel']['SonarRadius'],2,"")
			if 'WaterVisionRadius' in c_unit['Intel']:
				page_s += ", "+ct("water vision radius: ",c_unit['Intel']['WaterVisionRadius'],2,"")
			if 'RadarStealthFieldRadius' in c_unit['Intel']:
				page_s += ", "+ct("radar stealth field radius: ",c_unit['Intel']['RadarStealthFieldRadius'],2,"")
			if 'SonarStealthFieldRadius' in c_unit['Intel']:
				page_s += ", "+ct("sonar stealth field radius: ",c_unit['Intel']['SonarStealthFieldRadius'],2,"")
			page_s += ediv()
			
			"""
			OmniRadius = 26,
			VisionRadius = 26,
			WaterVisionRadius = 26,
			RadarRadius
			RadarStealthFieldRadius = 40,
			SonarStealthFieldRadius = 40,
			"""
			
		if 'Physics' in c_unit:
			page_s += cdiv()
			page_s += "<b>Physics: </b>"
			page_s += ct("size: ",c_unit['SizeX'],2,"")
			page_s += ct(" x ",c_unit['SizeY'],2,"")
			page_s += ct(" x ",c_unit['SizeZ'],2,"")
			adjsizes = ["place","'SIZE4'","'SIZE8'","'SIZE12'","'SIZE16'","'SIZE20'"]
			for siz in range(1,6):
				if adjsizes[siz] in c_unit['Categories']:
					page_s += ct(",  size for adjacency: ",str(int(siz*4)),0,"")
					
			if 'MaxSpeed' in c_unit['Physics']:
				page_s += ct(", max speed: ",c_unit['Physics']['MaxSpeed'],3,"m/s")
				
			if 'TurnRate' in c_unit['Physics']:
				page_s += ct(", turn rate: ",c_unit['Physics']['TurnRate'],0,"")
			page_s += ediv()
			
		if 'Air' in c_unit:
			page_s += cdiv()
			page_s += "<b>Air Physics: </b>"
			if 'MinAirspeed' in c_unit['Air']:
				page_s += ct("speed: ",c_unit['Air']['MinAirspeed'],3,"m/s")
			else:
				page_s += ct("speed: ",0,3,"m/s")
			page_s += ct(" - ",c_unit['Air']['MaxAirspeed'],3,"m/s")
			page_s += ct(", elevation:",c_unit['Physics']['Elevation'],2,"")
			if 'EngageDistance' in c_unit['Air']:
				page_s += ct(", engage distance:",c_unit['Air']['EngageDistance'],2,"")
			if 'TurnSpeed' in c_unit['Air']:
				page_s += ct(", turn speed: ",c_unit['Air']['TurnSpeed'],0,"")
			if 'CombatTurnSpeed' in c_unit['Air']:
				page_s += ct(", combat turn speed: ",c_unit['Air']['CombatTurnSpeed'],0,"")
			page_s += ediv()
			
			"""
			these are in air
			MaxAirspeed = 4,
			MinAirspeed = 3,
			CombatTurnSpeed = 1,
			TurnSpeed = 0.8,
			EngageDistance = 50,
			
			These are in ['Physics']
			Elevation = 25,
			FuelRechargeRate = 15,
			FuelUseTime = 1200,
			GroundCollisionOffset = 1.6,
			MaxSpeed = 0.5,
			"""
			
		if 'Veteran' in c_unit:
			for level in range(1,6):
				page_s += cdiv()
				page_s += "<b>Veterancy level "+str(level)+" </b>("
				page_s += ct("",c_unit['Veteran']['Level'+str(level)],0,"")+" kills): "
				page_s += ct("new health: ",c_unit['Defense']['MaxHealth'],4,"hp",level)
				if 'Buffs' in c_unit:
					page_s += ct(", new regen rate: ",str(float(c_unit['Defense']['RegenRate'])+float(c_unit['Buffs']['Regen']['Level'+str(level)])),0,"hp/s (+")
					page_s += ct("",c_unit['Buffs']['Regen']['Level'+str(level)],0,"hp/s)")
				page_s += ediv()
				
		if 'Wreckage' in c_unit:
			page_s += cdiv()
			page_s += "<b>Wreckage: </b>"
			page_s += ct("health: ",int(float(c_unit['Wreckage']['HealthMult'])*float(c_unit['Defense']['MaxHealth'])),0,"")
			page_s += ct(", mass: ",int(float(c_unit['Wreckage']['MassMult'])*float(c_unit['Economy']['BuildCostMass'])),0,"")
			page_s += ct(", energy: ",int(float(c_unit['Wreckage']['EnergyMult'])*float(c_unit['Economy']['BuildCostEnergy'])),0,"")
			page_s += ediv()
			
			
			"""
			c_unit['Defense']['MaxHealth']
			BuildCostEnergy = 307500,
			BuildCostMass = 24600,
			
			EnergyMult = 0,
			HealthMult = 0.9,
			MassMult = 0.9,
			"""
			
		if 'Weapon' in c_unit:
			page_s += cdiv()
			page_s += "<b>Weapons: </b>"
			for weap in c_unit['Weapon']:
				page_s += "<div class='indent'>"
				page_s +="<b>"+ ct("",weap['DisplayName'][1:-1],0,"")+"</b><span style='font-size:small;'>"
				page_s +=" ("+ct("",weap['WeaponCategory'][1:-1],0,"")+", "+ct("",weap['DamageType'][1:-1],0,"")+"):"
				
				if 'Damage' in weap:
					if weap['WeaponCategory'] == "'Direct Fire'":
						page_s += ct(" ",float(weap['Damage'])/(1/float(weap['RateOfFire'])),0,"") +" dps"
						
						if 'MaxRadius' in weap:
							minradius = 0;
							if 'MinRadius' in weap:
								minradius = weap['MinRadius']
								page_s += ", "+ct("range: ",minradius,2,"") + " - "+ct("range: ",weap['MaxRadius'],2,"")
						if 'DamageRadius' in weap:
							page_s += ", "+ct("area damage radius: ",weap['DamageRadius'],2,"")
						page_s += "<div class='indent'>"
						page_s += "<b>"+ct("","Projectile: ",0,"")+"</b>"+ct("",weap['Damage'],0," damage")
						page_s += ediv()
				#if 'Damage' in weap and 'RateOfFire' not in weap:
				#	print(unit)
				if weap['WeaponCategory'] == "'Death'":
					if 'Damage' in weap:
						if weap['Damage'] != '0':
							page_s += ct("<b> ",weap['Damage'],0,"</b>") + " damage"
							page_s += ct(", area damage radius:",weap['DamageRadius'],2,"")
				
				if 'TurretPitch' in weap:
					page_s += "<div class='indent'>"
					page_s += ct("turret pitch: ",weap['TurretPitch'],0,"&deg;") +" &plusmn;"+ct("",weap['TurretPitchRange'],0,"&deg;")+ ct(" (",weap['TurretPitchSpeed'],0,"&deg;/s")+"), " + ct("turret yaw: ",weap['TurretYaw'],0,"&deg;")+ct("&plusmn;",weap['TurretYawRange'],0,"&deg;")+ " ("+ct("",weap['TurretYawSpeed'],0,"&deg;/s")+")"
					page_s += ediv()
				page_s += "</span>"
				page_s += ediv()
			"""
			WeaponCategory = 'Direct Fire',
			
			RateOfFire = 1,
			ProjectilesPerOnFire = 1,
			ProjectileLifetime = 7,
			MaxRadius = 22,
			MinRadius = 1,
			MuzzleVelocity = 35,
			FiringRandomness = 0.22,

			
			Damage = 100,
			DamageType = 'Normal','Overcharge',
			DisplayName = 'Molecular Ripper Cannon',
			DamageRadius = 2
			EnergyChargeForFirstShot = false,
			EnergyDrainPerSecond = 3000,
			EnergyRequired = 3000,
			
			NukeInnerRingDamage = 3500,
			NukeInnerRingRadius = 30,
			NukeOuterRingDamage = 500,
			NukeOuterRingRadius = 40,

			
			
			TurretPitch = 0,
			TurretPitchRange = 90,
			TurretPitchSpeed = 90,
			TurretYaw = 0,
			TurretYawRange = 180,
			TurretYawSpeed = 90,
			shield gun is special!!!## absolver unit

			"""
			page_s += ediv()
			
		if 'Enhancements' in c_unit:
			page_s += cdiv()
			page_s += "<b>Enhancements: </b>"
			enhance = c_unit['Enhancements']
			for upgrade in enhance.keys():
				if upgrade != "Slots":
					if enhance[upgrade]['BuildCostMass'] != '1':
						page_s += cdiv()
						page_s += "<b>"+ct("",enhance[upgrade]['Slot'][1:-1]+" "+enhance[upgrade]['Name'][enhance[upgrade]['Name'].find('>')+1:-1],0,"")+"</b> "
						page_s += " ("
						page_s += ct("mass: ",enhance[upgrade]['BuildCostMass'],0,"")
						
						page_s += " ("
						if 'ProductionPerSecondMass' in enhance[upgrade]:
							page_s += ct("",enhance[upgrade]['ProductionPerSecondMass'],5,"")
						else:
							page_s += ct("",0,5,"")
						page_s += ")"	
						page_s += ct(", energy: ",enhance[upgrade]['BuildCostEnergy'],0,"")
						page_s += " ("
						if 'ProductionPerSecondEnergy' in enhance[upgrade]:
							page_s += ct("",enhance[upgrade]['ProductionPerSecondEnergy'],5,"")
						elif 'MaintenanceConsumptionPerSecondEnergy' in enhance[upgrade]:
							page_s += ct("",enhance[upgrade]['MaintenanceConsumptionPerSecondEnergy'],6,"")
						else:
							page_s += ct("",0,5,"")
						page_s += " )"
							
						
						
						page_s += ct(", build time: ",enhance[upgrade]['BuildTime'],0,"")
						page_s += ")"
						page_s += ediv()
			page_s += ediv()
		#builds	
		builder = False
		#for cat in buildscats:
		if 'Buildables' in c_unit:
			page_s += "<div style='float:left;'>"
			page_s += "<b>Builds: </b><table>"		
			tlevels = ["'TECH1'","'TECH2'","'TECH3'","'EXPERIMENTAL'"]
			nameandid = dict()
			idandname = dict()
			unames = list()
			for warg in tlevels:
				blarg = c_unit['Buildables'].intersection(categs[warg])
				tnames=list()
				
				for unsorted in blarg:
					techstr = ""
					if "'TECH1'" in bp[unsorted]['Categories']:
						techstr = "T1 "
					if "'TECH2'" in bp[unsorted]['Categories']:
						techstr = "T2 "
					if "'TECH3'" in bp[unsorted]['Categories']:
						techstr = "T3 "
					if "'EXPERIMENTAL'" in bp[unsorted]['Categories']:
						techstr = "EX "
					name = bp[unsorted]['General']['FactionName'][1:-1]+" "+techstr 
					name += bp[unsorted]["Description"][bp[unsorted]["Description"].find('>')+1:-1]
					if 'UnitName' in bp[unsorted]['General']:
						name += ": "+bp[unsorted]['General']["UnitName"][bp[unsorted]["General"]["UnitName"].find('>')+1:-1]
					tnames.append(name)
					nameandid[name] = unsorted
					idandname[unsorted] = name
				tnames.sort()
				
				sortedlist = list()
				for blah in tnames:
					sortedlist.append(nameandid[blah])
					unames.append(blah)
				
				tnames=[]
				#print(buildables)
				for bunit in sortedlist:
					page_s += "<tr><td style='font-size: small;'><a href='#'>"
					
					page_s += "<img src='"+imgsrc+bp[bunit]['General']['FactionName'][1:-1].lower()+"_"+bp[bunit]["StrategicIconName"][1:-1]+".png' style='border: 0pt none ;'></div>"
					page_s += idandname[bunit]
					page_s += "</a></td><td style='font-size: small;'>("	
					time = float(bp[bunit]['Economy']['BuildTime'])/float(c_unit['Economy']['BuildRate'])
					page_s += ct("mass: ",float(bp[bunit]['Economy']['BuildCostMass'])/time,6," ")
					page_s += ct("energy: ",float(bp[bunit]['Economy']['BuildCostEnergy'])/time,6," ")
					page_s += ct("time: ",str(int(time/60))+":"+str(int(time%60)),0,"")
					page_s += ")</td></tr>"
				sortedlist=[]
			
				
			page_s += "</table>"
			page_s += ediv()
			
		#Built by
		if len(builtby[unit]) > 0:	
			page_s += "<div style='float:left;'>"
			page_s += "<b>Built by: </b><table>"
			tlevels = ["'TECH1'","'TECH2'","'TECH3'","'EXPERIMENTAL'"]
			nameandids = dict()
			idandnames = dict()
			uname = list()
			for wargs in tlevels:
				blargs = builtby[unit].intersection(categs[wargs])
				if wargs == "'TECH1'":
					blargs = builtby[unit].difference(categs["'TECH2'"]).difference(categs["'TECH3'"]).difference(categs["'EXPERIMENTAL'"])
				tname=list()
				
				for unsorteds in blargs:
					techstr = ""
					if "'TECH1'" in bp[unsorteds]['Categories']:
						techstr = "T1 "
					if "'TECH2'" in bp[unsorteds]['Categories']:
						techstr = "T2 "
					if "'TECH3'" in bp[unsorteds]['Categories']:
						techstr = "T3 "
					if "'EXPERIMENTAL'" in bp[unsorteds]['Categories']:
						techstr = "EX "
					names = bp[unsorteds]['General']['FactionName'][1:-1]+" "+techstr 
					names += bp[unsorteds]["Description"][bp[unsorteds]["Description"].find('>')+1:-1]
					if 'UnitName' in bp[unsorteds]['General']:
						names += ": "+bp[unsorteds]['General']["UnitName"][bp[unsorteds]["General"]["UnitName"].find('>')+1:-1]
					tname.append(names)
					nameandids[names] = unsorteds
					idandnames[unsorteds] = names
				tname.sort()
				
				sortedlists = list()
				for blah in tname:
					sortedlists.append(nameandids[blah])
					uname.append(blah)
				
				tname=[]
				for bunits in sortedlists:
					page_s += "<tr><td style='font-size: small;'><a href='#'>"
					
					page_s += "<img src='"+imgsrc+bp[bunits]['General']['FactionName'][1:-1].lower()+"_"+bp[bunits]["StrategicIconName"][1:-1]+".png' style='border: 0pt none ;'></div>"
					page_s += idandnames[bunits]
					page_s += "</a></td><td style='font-size: small;'>("	
					time = float(c_unit['Economy']['BuildTime'])/float(bp[bunits]['Economy']['BuildRate'])
					page_s += ct("mass: ",float(c_unit['Economy']['BuildCostMass'])/time,6," ")
					page_s += ct("energy: ",float(c_unit['Economy']['BuildCostEnergy'])/time,6," ")
					page_s += ct("time: ",str(int(time/60))+":"+str(int(time%60)),0,"")
					page_s += ")</td></tr>"
				sortedlist=[]
	
		
	

		page_s +="</body></html>"	
		unit_file = open(filepath+str(unit)+".html",'w')
		unit_file.write(page_s)
		unit_file.close()
	#health
	#abilities
	#economy
	#intel
	#physics
	#air physics
	#veterancy
	
	#wreckage
	#weapons
	#builds
	#built by
