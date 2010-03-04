#UnitBP grammar
#<BP>::= UnitBluePrint <block>
#<block-list>::= { <block><block-list> }, | { <block> }, 
#<block>::= { <statement-list> } | {statement-list}, | { <enum>},
#<statement-list>::=<statement> | <statement><statement-list> | <block>
#<statement>::=<variable> = <value>,| <variable> = <block> | <variable> = <block-list>| <variable> = <word> <block> 
#<enum>::=<words>, | <words>,<enum>
#<variable>::=<letter>
#<letter>::=valid LUA variable names
#<word>::=words
#
#msl = mutable string List

#This function should take a string and break it up
#when it encounters !@#$%^&*()-_+=[]{}|:;",?
#it returns tokens of a-zA-Z0-9.'/\<>


def isWordnum(part):
	test_string = list(part)

	symbols = ['+','=','{','}','|',',','"','\n','\r']
	for x in test_string:
		if x in symbols:
			return False
	return True
	
	
def returnUnitBP(msl):
	#print("we got to unitBP")
	unit_data=dict()
	a_token = str(msl.next())
	if a_token == 'UnitBlueprint':
		unit_data = returnBlock(msl)
	#print("exiting unitBP ")
	return unit_data
	
def returnBlock(msl):
	#print("we got to Block")
	a_token = msl.next()
	a_dict = dict()
	if a_token == '{':
		b_token = msl.peekNext()
		c_token = msl.deepPeek()
		if isWordnum(b_token):
			if c_token == ',':
				a_dict = returnEnum(msl)
			else:
				a_dict = returnStatementList(msl)
		if msl.next() == '}':
			if msl.peekNext() == ',':
				msl.next()
	#print("exiting Block")
	return a_dict
	
def returnBlockList(msl):
	#print("we got to BlockList "+msl.peekNext()+" "+msl.deepPeek())
	a_list = list()
	a_token = msl.next()
	while a_token == '{':
		a_list.append(returnBlock(msl))
		a_token = msl.peekNext()
	msl.next()
	msl.next()
	#print("exiting BlockList ")
	return a_list

def returnStatementList(msl):
	#print("we got to StatementList")
	a_dict = dict()
	a_token = msl.peekNext()
	temp_dict = dict()
	while isWordnum(a_token):
		temp_dict = returnStatement(msl)
		if temp_dict != None:
			for keys in temp_dict.keys():
				a_dict[keys] = temp_dict.get(keys)
		a_token = msl.peekNext()
	#print("exiting StatementList ")	
	return a_dict
	
def returnStatement(msl):
	#print("we got to Statement")
	a_dict = dict()
	a_token = msl.next()
	#print("out a_token is " + a_token)
	if msl.next() == '=':
		b_token = ''.join(msl.peekNext())
		#print("our b_token is " + b_token)
		if b_token == '{':
			c_token = msl.deepPeek()
			if c_token == '{':
				#print("case 1")
				a_dict[a_token] = returnBlockList(msl)
				#print("exiting Statement ")
				return a_dict
			else:
				#print("case 2")
				a_dict[a_token] = returnBlock(msl)
				#print("exiting Statement ")
				return a_dict
		else:
			
			b_token = msl.next()
			c_token = msl.peekNext()
			if c_token == '{':
				#print("case 3")
				a_dict[a_token] = returnBlock(msl)
				#print("exiting Statement ")
				return a_dict
			else:
				#print("case 4")
				a_dict[a_token] = b_token
				if msl.next() == ',':
					#print("exiting Statement ")
					return a_dict
	
def returnEnum(msl):
	#print("we got to an enum")
	a_list = list()
	a_token = msl.peekNext()
	b_token = msl.deepPeek()
	while isWordnum(a_token) and b_token == ',':
		a_token = msl.next()
		b_token = msl.next()
		a_list.append(a_token)
		a_token = msl.peekNext()
		b_token = msl.deepPeek()
	#print("exiting enum ")
	return a_list
	
	

