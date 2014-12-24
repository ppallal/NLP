import commands

def ip():
	full = commands.getoutput("/sbin/ifconfig")
	#print full	
	trash,full=full.split("eth",1)
	trash,full=full.split("inet addr:",1)
	ip,trash=full.split(" ",1)
	return ip
