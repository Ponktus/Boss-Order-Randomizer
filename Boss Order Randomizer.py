import random, struct, json, time
from Spoilers import spoiler_log
from Logic_Config import item_lock_config as ilc

###
#The codes is divided into seperate parts with three # if an ! is appended it means that that part of is tested and works.
###

### Picks a random boss order and returns it as a list of boss names

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
	Item_Code = Index
	Bytes[1] = int(Item_Code[:-2], 16)
	Bytes[0] = int(Item_Code[-2:], 16)
	if Visibility == 'Chozo':
		Bytes[0] += 0x54
	elif Visibility == 'Hidden':
		Bytes[0] += 0xA8
	return Bytes

###! Picks a random object from a list. Used to pick random item locations and random items from lists.

def pick_random_list_object(list_object):
	return random.choice(list_object)

print('Initializing...')
Boss_Order = boss_order()
Locked_Items = ilc(Boss_Order)

###! Opens Item_Locations.json, Items.json, Item_Set_Config.json and stores them in an array for later use.

Json = open('Item_Locations.json', 'r')
Item_Locations = json.load(Json)
Location_Codes = list(Item_Locations)

Json = open('Items.json', 'r')
Item_Properties = json.load(Json)
Json.close

Json = open('Item_Set_Config.json', 'r')
Item_Lock_Sets = json.load(Json)
Json.close

###! Setting up information and item locks based on boss order and config file.

High_Tier_Items = ["Morph", "Super", "Powerbombs", "Speed", "Varia", "Gravity", "Etank", "Spacejump"]
Unlocked_Items = []
Next_Item_List = []
Item_Distribution = []
Early_Morph = True
Item_Value = 0
Progress_Items_Not_Distributed = True

### Hauptroutine, die die Itemverteilung festlegt
while Progress_Items_Not_Distributed:
    # Make list of all Unlocked item locations and remove those locations from the locked item list.
    print('Verschlossene Items')
    print(len(Locked_Items))
    Offset = 0
    Removable_Item_Sets = []
    Newly_Unlocked_Items = []
    Progress_Items = []
    for i in range(len(Locked_Items)):
        if not Locked_Items[i-Offset]['ItemLock'] and not Locked_Items[i-Offset]['ItemSetLock']:
            Newly_Unlocked_Items.append(Locked_Items[i-Offset]['Adress'])
            Unlocked_Items.append(Locked_Items[i-Offset]['Adress'])
            del Locked_Items[i-Offset]
            Offset += 1
    print('Verschlossene Items nach dem Check')
    print(len(Locked_Items))
    #! Make List of all progress locking items. Adds items multiple times to prioritize items that lock more stuff.
    Progress_Items = []
    for i in range(len(Locked_Items)):
        if len(Locked_Items[i]['ItemLock']) != 0:
            for j in range(len(Locked_Items[i]['ItemLock'])):
                Progress_Items.append(Locked_Items[i]['ItemLock'][j])
        else:
            for j in range(len(Locked_Items[i]['ItemSetLock'])):
                Progress_Items.append(Locked_Items[i]['ItemSetLock'][j])
    # Force early Morph
    if 'Morph' in Progress_Items and Early_Morph:
        if len(Newly_Unlocked_Items) != 0: 
            Chosen_Location = pick_random_list_object(Newly_Unlocked_Items)
        else:
            Chosen_Location = pick_random_list_object(Unlocked_Items)
        Item_Distribution.append([Chosen_Location, hex(0xef23)])
        Unlocked_Items.remove(Chosen_Location)
        Offset = 0
        for i in range(len(Item_Lock_Sets)):
            for j in range(len(Item_Lock_Sets[i-Offset])-1):
                if 'Morph' in Item_Lock_Sets[i-Offset][str(j+1)]:
                    Item_Lock_Sets[i-Offset][str(j+1)].remove('Morph')
            for j in range(len(Item_Lock_Sets[i-Offset])-1):
                if [] == Item_Lock_Sets[i-Offset][str(j+1)] and not Item_Lock_Sets[i]['Name'] in Removable_Item_Sets:
                    Removable_Item_Sets.append(Item_Lock_Sets[i]['Name'])
        for i in range(len(Removable_Item_Sets)):
            Offset = 0
            for j in range(len(Item_Lock_Sets)):
                if Item_Lock_Sets[j-Offset]['Name'] == Removable_Item_Sets[i]:
                    del Item_Lock_Sets[j-Offset]
                    Offset += 1
            for j in range(len(Locked_Items)):
                if Removable_Item_Sets[i] in Locked_Items[j]['ItemSetLock']:
                    Locked_Items[j]['ItemSetLock'].remove(Removable_Item_Sets[i])
                if 'Morph' in Locked_Items[j]['ItemLock']:
                    Locked_Items[j]['ItemLock'].remove('Morph') 
        print(len(Locked_Items))
    else:
        # Pick a random one of these items and put it on a slot from the Newly_Unlocked_Items list into the Item_Distribution list if its not empty.
        if Progress_Items == []:
        	break
        Next_Item = pick_random_list_object(Progress_Items)
        Progress_Items = []
        #Checking the easier case first. Next_Item is an item and not an itemset
        if Next_Item in High_Tier_Items:
            if len(Newly_Unlocked_Items) != 0:
                Chosen_Location = pick_random_list_object(Newly_Unlocked_Items)
            else:
                Chosen_Location = pick_random_list_object(Unlocked_Items)
            Item_Value = 0
            for i in range(len(Item_Properties)):
                if Item_Properties[i]['Name'] == Next_Item:
                    Item_Value = int(Item_Properties[i]['Code'], 16)
            Item_Distribution.append([Chosen_Location, hex(Item_Value)])
            Unlocked_Items.remove(Chosen_Location)
            Removable_Item_Sets = []     
            #routine that checks if itemsets and items can be removed from the conditions
            Offset = 0
            for i in range(len(Item_Lock_Sets)):
                for j in range(len(Item_Lock_Sets[i-Offset])-1):
                    if Next_Item in Item_Lock_Sets[i-Offset][str(j+1)]:
                        Item_Lock_Sets[i-Offset][str(j+1)].remove(Next_Item)
                for j in range(len(Item_Lock_Sets[i-Offset])-1):
                    if [] == Item_Lock_Sets[i-Offset][str(j+1)] and not Item_Lock_Sets[i]['Name'] in Removable_Item_Sets:
                        Removable_Item_Sets.append(Item_Lock_Sets[i]['Name'])
            for i in range(len(Removable_Item_Sets)):
                Offset = 0
                for j in range(len(Item_Lock_Sets)):
                    if Item_Lock_Sets[j-Offset]['Name'] == Removable_Item_Sets[i]:
                        del Item_Lock_Sets[j-Offset]
                        Offset += 1
                for j in range(len(Locked_Items)):
                    if Removable_Item_Sets[i] in Locked_Items[j]['ItemSetLock']:
                        Locked_Items[j]['ItemSetLock'].remove(Removable_Item_Sets[i])
            for i in range(len(Locked_Items)):
                if Next_Item in Locked_Items[i]['ItemLock']:
                    Locked_Items[i]['ItemLock'].remove(Next_Item)             
        #If chosen progression is an itemset
        else:
            Next_Item_List = []
            for i in range(len(Item_Lock_Sets)):
                if Next_Item == Item_Lock_Sets[i]['Name']:
                    Next_Item_List = (Item_Lock_Sets[i][str(random.randint(1, len(Item_Lock_Sets[i])-1))])
            Chosen_Location_List = []
            for i in range(len(Next_Item_List)):
                if i == 0 and len(Newly_Unlocked_Items) != 0:
                    Chosen_Location = pick_random_list_object(Newly_Unlocked_Items)
                else:
                    Chosen_Location = pick_random_list_object(Unlocked_Items)
                Chosen_Location_List.append(Chosen_Location)
                Unlocked_Items.remove(Chosen_Location)
            for x in range(len(Next_Item_List)):
                Next_Item = pick_random_list_object(Next_Item_List)
                for j in range(len(Item_Properties)):
                    if Item_Properties[j]['Name'] == Next_Item:
                        Item_Value = int(Item_Properties[j]['Code'], 16)
                        Next_Item_List.remove(Next_Item)
                Next_Location = pick_random_list_object(Chosen_Location_List)
                Chosen_Location_List.remove(Next_Location)
                Item_Distribution.append([Next_Location, hex(Item_Value)])
                Offset = 0
                for i in range(len(Item_Lock_Sets)):
                    for j in range(len(Item_Lock_Sets[i-Offset])-1):
                        if Next_Item in Item_Lock_Sets[i-Offset][str(j+1)]:
                            Item_Lock_Sets[i-Offset][str(j+1)].remove(Next_Item)
                    for j in range(len(Item_Lock_Sets[i-Offset])-1):
                        if [] == Item_Lock_Sets[i-Offset][str(j+1)] and not Item_Lock_Sets[i]['Name'] in Removable_Item_Sets:
                            Removable_Item_Sets.append(Item_Lock_Sets[i]['Name'])
                for i in range(len(Removable_Item_Sets)):
                    Offset = 0
                    for j in range(len(Item_Lock_Sets)):
                        if Item_Lock_Sets[j-Offset]['Name'] == Removable_Item_Sets[i]:
                            del Item_Lock_Sets[j-Offset]
                            Offset += 1
                    for j in range(len(Locked_Items)):
	                    if Removable_Item_Sets[i] in Locked_Items[j]['ItemSetLock']:
	                        Locked_Items[j]['ItemSetLock'].remove(Removable_Item_Sets[i])
	            for i in range(len(Locked_Items)):
	                if Next_Item in Locked_Items[i]['ItemLock']:
	                    Locked_Items[i]['ItemLock'].remove(Next_Item)
    spoiler_log(Boss_Order, Item_Distribution, Item_Locations, Item_Properties)
#Items auffuellen
for i in range(15):
	Distributed = "no"
	for j in range(len(Item_Distribution)):
		if Item_Distribution[j][1] == Item_Properties[i+5]['Code']:
			Distributed = "yes"
	if Distributed == "no":
		Location = pick_random_list_object(Unlocked_Items)
		Unlocked_Items.remove(Location)
		Item_Distribution.append([Location, Item_Properties[i+5]['Code']])

Etank_Counter = 0
for i in range(len(Item_Distribution)):
	if Item_Distribution[i][1] == '0xeed7':
		Etank_Counter += 1
for i in range(14 - Etank_Counter):
	Location = pick_random_list_object(Unlocked_Items)
	Unlocked_Items.remove(Location)
	Item_Distribution.append([Location, '0xeed7'])
for i in range(4):
	Location = pick_random_list_object(Unlocked_Items)
	Unlocked_Items.remove(Location)
	Item_Distribution.append([Location, '0xef27'])

for i in range(len(Unlocked_Items)):
	x = random.randint(1,7)
	Location = pick_random_list_object(Unlocked_Items)
	Unlocked_Items.remove(Location)
	if x == 1 or x == 2 or x == 3:
		Item_Distribution.append([Location, '0xeedb'])
	if x == 4 or x == 5 or x == 6:
		Item_Distribution.append([Location, '0xeedf'])
	if x == 7:
		Item_Distribution.append([Location, '0xeee3'])
print(Item_Distribution)


Rom_File = open("SuperMetroid.sfc", "r+")

for i in range(100):
	Bytes = byte_splitter(Item_Distribution[i][1], 'Visible')
	Rom_File.seek(int(Item_Distribution[i][0], 16))
	Rom_File.write(chr(Bytes[0]))
	Rom_File.write(chr(Bytes[1]))

Door_Stuff = [[0x1C, 0x078A2B, 0x45], [0x20, 0x07C2A2, 0xB5], [0x24, 0x07C74C, 0x9B], [0x28, 0x078EB7, 0x5C]]

for i in range(3):
	Boss = Boss_Order[i+1]
	if Boss == 'Kraid':
		index1 = 0
	if Boss == 'Phantoon':
		index1 = 1
	if Boss == 'Draygon':
		index1 = 2
	if Boss == 'Ridley':
		index1 = 3
	Rom_File.seek(Door_Stuff[index1][1])
	Boss = Boss_Order[i]
	if Boss == 'Kraid':
		index2= 0
	if Boss == 'Phantoon':
		index2 = 1
	if Boss == 'Draygon':
		index2 = 2
	if Boss == 'Ridley':
		index2 = 3
	Rom_File.write(chr(Door_Stuff[index2][2]))
	Rom_File.write(chr(Door_Stuff[index1][0]))

if Boss_Order[0] == 'Kraid':
	Rom_File.seek(0x10A056)
	Rom_File.write(chr(0x01))
	Rom_File.seek(0x078A2B)
	Rom_File.write(chr(0x0C))
if Boss_Order[0] == 'Phantoon':
	Rom_File.seek(0x10B81B)
	Rom_File.write(chr(0x0B))
	Rom_File.seek(0x07C74C0)
	Rom_File.write(chr(0x0C))
if Boss_Order[0] == 'Ridley':
	Rom_File.seek(0x10C3E5)
	Rom_File.write(chr(0x02))
	Rom_File.seek(0x07C2A2)
	Rom_File.write(chr(0x0C))

print("done")
