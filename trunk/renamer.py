import sys
import fileinput
import os
import time 
import math
"""
This handy tool moves the unit blue prints that are combat units, as defined in unitDB.txt to a 
folder called /war_units in the same folder as the bps. The war_units folder may need to exist first
Then it renames every unit file to just the blueprintId.bp.
"""
unescapedpath = str(sys.argv[1:]).strip("[']")
fullpath = os.path.abspath(os.getcwd()+unescapedpath)
bp_files = os.listdir(fullpath)

warunits_file = open('./unitDB.txt')


line = warunits_file.readline()
while line:
	print(line)
	a_file = open(fullpath+"/"+line[:-1]+"_unit.bp")
	print(fullpath+"/"+line+"_unit.bp")
	filestring = a_file.read()
	a_file.close()
	
	output_file = open(fullpath+"/war_units/"+line[:-1]+".bp","w")
	output_file.write(filestring)
	line = warunits_file.readline()
