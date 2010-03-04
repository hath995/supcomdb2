import sys
import fileinput
import os
import time 
import math
from datetime import date
from myParser import *
from myTokenizer import *

from myDataprep import *

unescapedpath = str(sys.argv[1:]).strip("[']")
if sys.argv[1] != "-r":

	fullpath = os.path.abspath(os.getcwd()+unescapedpath)
	bp_files = os.listdir(fullpath)
	bp_full_files = os.listdir(fullpath)
	for i in range(len(bp_files)):
		bp_full_files[i] = fullpath+"/"+bp_files[i]
		
	print(bp_files)
	
	bp = {}
	for i in range(len(bp_full_files)):
		filestring = ""
		a_file = None
		filestring = None
		blah = {}
		if os.path.splitext(bp_full_files[i])[1] == '.bp':
			a_file = open(bp_full_files[i])
			
			filestring = a_file.read()
			a_file.close()
			#print(a_file.name +"=  " + filestring)
			
			tz = list(filestring)
		
			
			bptokens = myTokenizer(tz)
			#bptokens.prints()
			output_file = open("output.py",'w')
			print("["+bp_files[i][0:bp_files[i].find('.')]+"]")
			bp[bp_files[i][0:bp_files[i].find('.')]] = returnUnitBP(bptokens)
	output_file.write("all_the_units = "+str(bp))
	output_file.close()
	data_prep(bp)

else:
	import output
	data_prep(output.all_the_units)
		#isUnitBP(bptokens,output_file)
		#output_file.close()
		
	
	#print("i="+str(bptokens.index))
	#print("len="+str(len(bptokens.tokens)))
	#print(bptokens.next())
	#print(bptokens.peekNext())
	#for tks in bptokens:
	#	if len(tks) == 1 and tks[0] != '\n':
	#		print str(tks[0])
	#	else:
	#		print str(tks)

	#bp_temp = returnUnitBP(bptokens)
	#print(a_file.name[0,a_file.name.find('.')])
	#print(a_file.name.find('.'))
	#bp[] = bp_temp
