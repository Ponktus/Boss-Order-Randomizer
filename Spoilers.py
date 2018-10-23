def spoiler_log(Boss_Order, Item_Distribution, Item_Locations, Item_Properties):
    Layout_Correction = ['Morph', 'Bombs', 'Super', 'Speed', 'Etank', 'Ice', 'Varia']
    Log = open('Spoilers.txt', 'w')
    Log.write('Boss-Order-Randomizer Version 0.2 created by Ponk.\n')
    Log.write('For more infos check out https://www.twitch.tv/ponktus or https://github.com/Ponktus/Boss-Order-Randomizer\n\n')
    Log.write('Boss Order:\n')
    Log.write(str(Boss_Order[0]) + ', ' + str(Boss_Order[1]) + ', ' + str(Boss_Order[2]) + ', ' + str(Boss_Order[3]) + '\n\n')
    Log.write('Items:\n')
    for i in range(len(Item_Distribution)):
        for j in range(100):
            if Item_Distribution[i][0] == Item_Locations[j]['Adress']:
                Location = Item_Locations[j]['Name']
        for j in range(20):
            if Item_Distribution[i][1] == Item_Properties[j]['Code']:
                Item = Item_Properties[j]['Name']
        if Item in Layout_Correction:
            Log.write(Item + ': \t\t' + Location + '\n')
        else:
            Log.write(Item + ': \t' + Location + '\n')
