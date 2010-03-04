

class myTokenizer:
	
	def __init__(self, a_list):
		self.tokens = []
		self.index = 0
		self.tokenize(a_list)
	
	def tokenize(self, a_list):
		#print(a_list)
		#{},='
		#comments foul thins up with # and --, and --[[stuff new line stuff]]--
		list_length = len(a_list)
		temp_index = 0
		while temp_index < list_length:
			#if in white space skip ahead until something interesting
			while a_list[temp_index] == ' ' or a_list[temp_index] == '\t' or a_list[temp_index] == '\n' or a_list[temp_index] == '\r':
					temp_index += 1
					if temp_index == list_length:
						break

			if temp_index < list_length:
				#if in a comment ignore until new line
				if a_list[temp_index] == '#' or (a_list[temp_index] == '-' and a_list[temp_index+1] == '-'):
					while a_list[temp_index] != '\n':
						temp_index += 1
				#if a control character return
				if a_list[temp_index] == '{' or a_list[temp_index] == '}' or a_list[temp_index] == '=' or a_list[temp_index] == ',':
					self.tokens.append(a_list[temp_index])
					#print("\n["+a_list[temp_index]+"]\n")
					temp_index +=1
	
				#if in a word store word, if in comments return whole string
				if str(a_list[temp_index]).isalpha() or str(a_list[temp_index]).isdigit() or a_list[temp_index] == '.' or a_list[temp_index] == '_' or a_list[temp_index] == '-':
					temp_token = str(a_list[temp_index])
					temp_index +=1
					while a_list[temp_index] != ' ' and a_list[temp_index] != ',':
						temp_token += a_list[temp_index]
						temp_index +=1
					self.tokens.append(temp_token)
				#if in a quoted string capture the entire string including caveat for nested quotes	
				if a_list[temp_index] == '\'':
					#print("did we get here?")
					temp_token = str('\'')
					temp_index+=1;
					while a_list[temp_index] != '\'':
						temp_token += a_list[temp_index]
						temp_index += 1
						if a_list[temp_index] == '\\':
							temp_token += a_list[temp_index]
							temp_index += 1
							temp_token += a_list[temp_index]
							temp_index += 1
					#print("how about here?")
					temp_token += a_list[temp_index]
					temp_index += 1
					self.tokens.append(temp_token)
					#print("\n["+temp_token+"]\n")
				#print(a_list[temp_index] +"_" +str(temp_index))
			

				
	#fix all of these to be array safe
	def next(self):
		if self.index != len(self.tokens):
			self.index+=1
		return self.tokens[self.index-1]
	
	def peekNext(self):
		if self.index != len(self.tokens):
			return self.tokens[self.index]
		else: 
			return ''
		
	def deepPeek(self):
		return self.tokens[self.index+1]
		
	def prints(self):
		for a in range(len(self.tokens)):
			print("["+self.tokens[a]+"]\n")
