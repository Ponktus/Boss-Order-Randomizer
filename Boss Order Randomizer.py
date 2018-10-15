import random, struct, json, time

### Picks a random boss order and returns it as a list.

def boss_order():
	Bosses = ['Kraid', 'Phantoon', 'Draygon', 'Ridley']
	Bossorder = []
	for i in range(4):
		x = random.randint(0,3-i)
		Bossorder.append(Bosses[x])
		Bosses.pop(x)
	return Bossorder

### Takes the index of the item from the Items.json aswell as the visibility of the target location
### and outputs the first and second bite that needs to be written over the target adress as a list.

def byte_splitter(Index, Visibility):
	Bytes = [0x00, 0x00]
	Item_Code = Item_Properties[Index]['Code']
	Bytes[1] = int(Item_Code[:-2], 16)
	Bytes[0] = int(Item_Code[2:] + Item_Code[:2], 16)
	if Visibility == 'Chozo':
		Bytes[0] += 0x54
	elif Visibility == 'Hidden':
		Bytes[0] += 0xA8
	return Bytes

### Picks a random object from a list. Used to pick random item locations and random items from lists.

def pick_random_list_object(list):
	return list[random.randint(0, len(list))]

print('Initializing...')

### Opens Item_Locations.json and stores it in an array 'Item_Locations' for later use.

Json = open('Item_Locations.json', 'r')
Item_Locations = json.load(Json)
Json.close

### Opens Items.json and stores it in an array 'Item_Properties' for later use.

Json = open('Items.json', 'r')
Item_Properties = json.load(Json)
Json.close

Rom_File = open("SuperMetroid.sfc", "r+")
Rom_File.seek(0x786DE+2)
print(ByteToHex(Rom_File.read(2)))
Rom_File.seek(0x786DE)
Rom_File.write(chr(0x73))
Rom_File.write(chr(0xEF))
Rom_File.seek(0x786DE+2)
print(ByteToHex(Rom_File.read(2)))

### Setting up information and item locks based on boss order and config file.

Locked_Items = Item_Locations.copy()
Unlocked_Items = []

Boss_Order = boss_order()
Ridley_Position = Boss_Order.index('Ridley')
Draygon_Position = Boss_Order.index('Draygon')
Phantoon_Position = Boss_Order.index('Phantoon')
Kraid_Position = Boss_Order.index('Kraid')

#for i in range(4):
#	for j in range(4-(i+1)):
#		for k in range(100):
#			if Locked_Items[k]['BossLock'] == Boss_Order[j]:
				#Need to add Boss_Requirements.json for comparison and to add prerequisites

for x in range(16):
    for i in range(len(Locked_Items)):
        if not Item_Locations[i]['ItemLock'] and not Item_Locations[i]['ItemSetLock']:
            Unlocked_Items.append(Item_Locations[i])
            del Locked_Items[i]
    # Make List of all progress locking items
    Progress_Items = []
    for i in range(len(Locked_Items)):
        if len(Locked_Items[i]['ItemLock']) != 0:
            for j in range(len(Locked_Items[i]['ItemLock'])):
                if not Locked_Items[i]['ItemLock'][j] in Progress_Items:
                    Progress_Items.append(Locked_Items[i]['ItemLock'][j])
        else:
            for j in range(len(Locked_Items[i]['ItemSetLock'])):
                if not Locked_Items[i]['ItemSetLock'][j] in Progress_Items:
                    Progress_Items.append(Locked_Items[i]['ItemSetLock'][j])
        
	# Pick a random of these items and put it on a slot from the Unlocked_Items list.
	# Cross out Itemlocks on the Locked_Items list


#for i in range(100):
#	Rom_File.seek(int(Item_Locations[i]["Adress"], 16))
#	Index = 0
#	for j in range(21):
#		if Item_Distribution[i][1] = Item_Properties[j]['Name']:
#			Index = j
#	Bytes = byte_splitter(Index, Visibility)


