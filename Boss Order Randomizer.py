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

High_Tier_Items = ["Morph", "Super", "Powerbombs", "Speed", "Varia", "Gravity", "Etank", "Spacejump"]
Unlocked_Items = []
Next_Item_List = []
Item_Distribution = []
Early_Morph = True
Item_Value = 0
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

### Hauptroutine, die die Itemverteilung festlegt

while not Progress_Items_Distributed:
    
    #Make list of all Unlocked item locations and remove those locations from the locked item list.
    Offset = 0
    Removable_Item_Sets = []
    Newly_Unlocked_Items = []
    for i in range(len(Locked_Items)):
        if not Locked_Items[i-Offset]['ItemLock'] and not Locked_Items[i-Offset]['ItemSetLock']:
            Newly_Unlocked_Items.append(Locked_Items[i-Offset]['Adress'])
            Unlocked_Items.append(Locked_Items[i-Offset]['Adress'])
            del Locked_Items[i-Offset]
            Offset += 1
    if Locked_Items == []:
        Progress_Items_Distributed = True
            
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
    
    # Force early Morph
    if 'Morph' in Progress_Items and Early_Morph:
        if len(Newly_Unlocked_Items) != 0: 
            Chosen_Location = pick_random_list_object(Newly_Unlocked_Items)
        else:
            Chosen_Location = pick_random_list_object(Unlocked_Items)
        Item_Distribution.append([Chosen_Location, 0xef23])
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
        
    else:
        # Pick a random one of these items and put it on a slot from the Newly_Unlocked_Items list into the Item_Distribution list if its not empty.
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
            Item_Distribution.append([Chosen_Location, Item_Value])
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
                    if Next_Item in Locked_Items[j]['ItemLock']:
                        Locked_Items[j]['ItemLock'].remove(Next_Item)
                        
        #If chosen progression is an itemset
        else:
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
                Item_Distribution.append([Next_Location, Item_Value])
                #checks if itemsets and items can be removed from the conditions
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
                        if Next_Item in Locked_Items[j]['ItemLock']:
                            Locked_Items[j]['ItemLock'].remove(Next_Item)
                            
        
    print("Item Verteilung:")
    print(Item_Distribution)
    print()
