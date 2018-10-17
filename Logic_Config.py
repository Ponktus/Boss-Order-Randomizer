import json, random

def item_lock_config(Boss_Order): #Will later require the difficulty settings as parameter for customization in a later release.
    
    Json = open('Item_Locations.json', 'r')
    Locked_Items = json.load(Json)
    Json.close

    Ridley_Position = Boss_Order.index('Ridley')
    Draygon_Position = Boss_Order.index('Draygon')
    Phantoon_Position = Boss_Order.index('Phantoon')
    Kraid_Position = Boss_Order.index('Kraid')

    for i in range(100):
        if Draygon_Position > Ridley_Position:
            if Locked_Items[i]['BossLock'] == "Draygon":
                Locked_Items[i]['ItemLock'].append('Varia')
                Locked_Items[i]['ItemSetLock'].append('CanTraverseWRITG')
        if Phantoon_Position > Ridley_Position:
            if Locked_Items[i]['BossLock'] == "Phantoon":
                Locked_Items[i]['ItemLock'].append('Varia')
                Locked_Items[i]['ItemSetLock'].append('CanTraverseWRITG')
        if Kraid_Position > Ridley_Position:
            if Locked_Items[i]['BossLock'] == "Kraid":
                Locked_Items[i]['ItemLock'].append('Varia')
                Locked_Items[i]['ItemLock'].append('Powerbombs')
                Locked_Items[i]['ItemSetLock'].append('CanTraverseWRITG')
        if Ridley_Position > Draygon_Position:
            if Locked_Items[i]['BossLock'] == "Ridley":
                Locked_Items[i]['ItemLock'].append('Gravity')
                Locked_Items[i]['ItemSetLock'].append('CanTraverseBotwoonHallway')
        if Phantoon_Position > Draygon_Position:
            if Locked_Items[i]['BossLock'] == "Phantoon":
                Locked_Items[i]['ItemLock'].append('Gravity')
                Locked_Items[i]['ItemSetLock'].append('CanTraverseBotwoonHallway')
        if Kraid_Position > Draygon_Position:
            if Locked_Items[i]['BossLock'] == "Kraid":
                Locked_Items[i]['ItemLock'].append('Gravity')
                Locked_Items[i]['ItemLock'].append('Powerbombs')
                Locked_Items[i]['ItemSetLock'].append('CanTraverseBotwoonHallway')
        if Kraid_Position > Phantoon_Position:
            if Locked_Items[i]['BossLock'] == "Kraid":
                Locked_Items[i]['ItemLock'].append('Powerbombs')
                Locked_Items[i]['ItemSetLock'].append('CanTraverseBotwoonHallway')
    
    for i in range(100):
        del Locked_Items[i]['Name']
        del Locked_Items[i]['Area']
        del Locked_Items[i]['Visibility']
        del Locked_Items[i]['Class']
    
    return(Locked_Items)
