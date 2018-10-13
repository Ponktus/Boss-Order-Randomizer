import random, struct, json, time
import numpy as np

def boss_order():
	Bosses = ['Kraid', 'Phantoon', 'Draygon', 'Ridley']
	Bossorder = []
	for i in range(4):
		x = random.randint(0,3-i)
		Bossorder.append(Bosses[x])
		Bosses.pop(x)
	return Bossorder

def major_items_distribution():
	List_Of_Majors = ['Bombs', 'Springball', 'Varia', 'Gravity', 'Hijump', 'Speed', 'Spacejump', 'Screw', 'Charge', 'Spazer', 'Wave', 'Ice', 'Plasma', 'Grapple', 'Xray']
	Distribution = {}
	Limitations = {}
	for i in range(10):
		Distribution[str(Item_Config[i]['Name'])] = ""
		Limitations[str(Item_Config[i]['Name'])] = ""
	Item = pick_random_major(List_Of_Majors)
	List_Of_Majors.remove(Item)
	Distribution[pick_random_location(Distribution, Limitations, Item)] = Item

#def pick_random_location(Locations, Limitations, Item):

#def Location_Possible(Distribution, Item, Target):

def pick_random_major(Major_List):
	return Major_List[random.randint(0, len(Major_List))]

def ByteToHex(bytestring):
	return ''.join( [ "%02X " % ord( x ) for x in bytestring ] ).strip()

print('Initializing...')

###Opens Item_Locations.json and stores it in an array 'Item_Locations' for later use

Json = open('Item_Locations.json', 'r')
Item_Locations = json.load(Json)
Json.close

###Opens Items.json and stores it in an array 'Item_Properties' for later use

Json = open('Items.json', 'r')
Item_Properties = json.load(Json)
Json.close

toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])

Rom_File = open("SuperMetroid.sfc", "r+")
Rom_File.seek(0x786DE+2)
print(ByteToHex(Rom_File.read(2)))
Rom_File.seek(0x786DE)
Rom_File.write(chr(0x73))
Rom_File.write(chr(0xEF))
Rom_File.seek(0x786DE+2)
print(ByteToHex(Rom_File.read(2)))

for i in range(100):
	print('Check')
	Rom_File.seek(Item_Locations[i]["Adress"])

