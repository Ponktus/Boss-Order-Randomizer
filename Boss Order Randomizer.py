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

def pick_random_list_object(list_object):
	return random.choice(list_object)

print('Initializing...')

### Opens Item_Locations.json, Items.json, Item_Set_Config.json and stores them in an array for later use.

Json = open('Item_Locations.json', 'r')
Locked_Items = json.load(Json)
Item_Locations = list(Locked_Items)
Json.close

Json = open('Items.json', 'r')
Item_Properties = json.load(Json)
Json.close

Json = open('Item_Set_Config.json', 'r')
Item_Lock_Sets = json.load(Json)
Json.close

### Rom write test

#Rom_File = open("SuperMetroid.sfc", "r+")
#Rom_File.seek(0x786DE+2)
#Rom_File.seek(0x786DE)
#Rom_File.write(chr(0x73))
#Rom_File.write(chr(0xEF))
#Rom_File.seek(0x786DE+2)

### Setting up information and item locks based on boss order and config file.

High_Tier_Items = ["Morph", "Supers", "Powerbombs", "Speed", "Varia", "Gravity"]
Unlocked_Items = []
Item_Distribution = []
for i in range(100):
	Item_Distribution.append([Item_Locations[i]['Adress']])
Progress_Items_Distributed = False
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

while not Progress_Items_Distributed:
    for i in range(len(Item_Locations)):
        if not Item_Locations[i]['ItemLock'] and not Item_Locations[i]['ItemSetLock']:
            Unlocked_Items.append(Item_Locations[i]['Adress'])
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
	# Pick a random of these items and put it on a slot from the Unlocked_Items list into the Item_Distribution list.
    Next_Item = pick_random_list_object(Progress_Items) 						#Name as string
    Progress_Items = []
    #Checking the easier case first. Next_Item is an item and not an itemset
    if Next_Item in High_Tier_Items:
    	for i in range(len(Locked_Items)):
			if Next_Item in Locked_Items[i]['ItemLock']:
				Locked_Items[i]['ItemLock'].remove(Next_Item)





    	High_Tier_Items.remove(Next_Item)
    	Location = pick_random_list_object(Unlocked_Items)							#Adress as hex
    	Item_Distribution.append([Location, Next_Item])



	# Cross out Itemlocks on the Locked_Items list
