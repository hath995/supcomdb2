import output

print(output.all_the_units['urb3202']['Categories'])
c_unit = output.all_the_units['urb3202']
buildscats = ["'CONSTRUCTION'","'FACTORY'","'ENGINEER'"]
builder = False
for cat in buildscats:
	if cat in c_unit['Categories']:
		builder = True
		print("True")
