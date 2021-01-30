file = open("u-item.item", "r")

lines = file.readlines()
for i in lines:
	newArray = i[5:]
	print(newArray)