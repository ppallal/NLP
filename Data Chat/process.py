f = open("salesData")
context = "None"
data = []
for i in f:
	x = i.split(":")
	if(len(x) >1):
		context = x[0][1:]
		#context.strip()
		ch = x[1]
	else:
		ch = x[0]
	data.append("<"+context+">"+ch+"</"+context+">")

for i in data:
	print i
