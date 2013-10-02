def Calc_CFT(count,length,width,height):# calculate cubic feet using inches as inputs
	return ((1.0 * count) * length * width * height)/17280 

def Calc_M3(count,length,width,height): # calculates cubic meters usd
	return Calc_CFT(count,length,width,height)/35.315
def WhichContainer(size):# returns the containers that can contain the cubic meter
	CNTS = []
	for a in ListOfCnt:
		if size <= ListOfCnt[a]['Capacity']:
			CNTS.append(ListOfCnt[a]['Name'])

	if CNTS == []:
		return None
	else:
		return CNTS
def isTooLong(length,Container):#if the length won't fit into container, returns FALSE

	if length > Container['Length']:
		return False
	else:
		return True

def isTooHigh(Height,Container):#if the Height won't fit into container, returns FALSE

	if Height > Container['Height']:
		return False
	else:
		return True
		

FortyFootGP = {'Name':"40' Standard" ,'Length':473, 'Width':92, 'Height':94,'DoorWidth':92,'DoorHeight':90,'Capacity':76.28} #inside and outside dimension in inches for 40' cnt
FortyFootHC = {'Name':"40' High Cube",'Length':473, 'Width':92, 'Height':107,'DoorWidth':92,'DoorHeight':101,'Capacity':76.28} #inside and outside dimension in inches for 40' high cube
TwentyFootGP = {'Name':"20' Standard",'Length':232, 'Width':92, 'Height':94,'DoorWidth':92,'DoorHeight':90,'Capacity':33.18} #inside and outside dimension in inches for 20'
 
ListOfCnt =  {'TwentyFootGP':TwentyFootGP, 'FortyFootGP':FortyFootGP, 'FortyFootHC':FortyFootHC } 	 


