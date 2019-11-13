#
# Map Module For Discord Bot
################################
import pickle, sys, datetime, os, discord, math, re, socket, time, random, asyncio
np, plt, ticker, mcd = None,None,None,None
n = 75

TILES = {
    'LAND': [45, 84, 55, 255],
    'WATER': [49, 108, 237, 255],
    'MEAT': [200, 110, 110, 255],
    'MOONDUST': [127, 127, 127, 255],
    'STARSEA': [64, 64, 64, 255],
}

UNIT_BASE = {
    'Costs': [],
    'DailyCosts': [],
    'NeedAdminApproval': False,
    'UpgradeUnit': "",
    'Marker': "",
    'isMobile': False,
    'MobileCost': [],
    'MoveLimitPerDay': 0,
    'DailyReturn': [],
    'LandOnly': False,
    'WaterOnly': False,
    'BeachOnly': False
}

TECH_TREE = {
    'granary': {
        'InitCost':None,
        'MaxLevel': 10,
        'BaseCost': '5 Technology',
        'AddResource': 'granary'
    },
    'mine': {
        'InitCost':None,
        'MaxLevel': 10,
        'BaseCost': '5 Technology',
        'AddResource': 'mines'
    },
    'oil': {
        'InitCost':None,
        'MaxLevel': 10,
        'BaseCost': '5 Technology',
        'AddResource': 'oil'
    },
    'powerplant': {
        'InitCost':None,
        'MaxLevel': 10,
        'BaseCost': '5 Technology',
        'AddResource': 'powerplant'
    },
    'university': {
        'InitCost':None,
        'MaxLevel': 10,
        'BaseCost': '5 Technology',
        'AddResource': 'university'
    },
    'sailing': {
        'InitCost': '15 Technology',
        'MaxLevel': 10,
        'BaseCost': '15 Technology',
        'AddResource': 'None'
    },
}

TIERLIST = [
    {'Harvest': {
        'type': 'Perpetual'
    }},
    {'Harvest':{
        'type':'Non Perpetual'
    }},
    {'Unit':{
        'Name':'town'
    }},
    {'Unit':{
        'Name':'village'
    }},
    {'Unit':{
        'Name':'granary'
    }},
    {'Unit':{
        'Name':'mines'
    }},
    {'Unit': {
        'Name': 'mill'
    }},
    {'Unit':{
        'Name':'oil'
    }},
    {'Unit':{
        'Name':'sailboat'
    }},
    {'Unit':{
        'Name':'powerplant'
    }},
    {'Unit':{
        'Name':'university'
    }},
    {'Unit':{
        'Name':'diplomats'
    }},
    {'Unit':{
        'Name':'digsite'
    }},
]

playerOrder = [
        'Alekosen#8467',
        'Paum#7183',
        'Boolacha#4539',
        'Krozr#0878',
        'Crorem#6962',
        'Jaekon#4155',
        'Fenris Wolf#6136',
        'Rabz12#9343',
        'Steam:HaphStealth Bnet#1191#5187',
        "Doby's Peri#6151",
        'Janwich#4842',
        'gfigs#6656',
        'iann39#8298',
    ]

botName = "Nomitron#3034"
oldData = {}
msgQueue = []
channels = {}
logChannel = ""
Data = {}
AllData = {}
savefile = str(__name__)  # + '_Data.pickle'
print(savefile)
Admins = ['Fenris Wolf#6136', 'Crorem#6962', 'iann39#8298']

itemList = ['BF', 'Cheese', 'Silica','Starfish','Aether', 'Corn', 'Food', 'Steel', 'Oil', 'Wood', 'Technology', 'Energy', 'C-Fish', 'Artifact', 'Curse']
rawMaterialsList = ['BF','Corn', 'Food', 'Steel', 'Oil', 'Wood', 'Technology', 'Energy']
resourceList = ['Corn', 'Cheese', 'Silica','Starfish','Aether','Steel', 'Oil']
FedMaterialList = list(rawMaterialsList)
FedMaterialList.remove('BF')

import itertools

letters = 'abcdefghijklmnopqrstuvwxyz'.upper()
labels = []
plotLables = []
for l1, l2 in list(itertools.product(letters, letters))[:75]:
    plotLables.append(l1 + '\n' + l2)
    labels.append(l1 + l2)

labels.append("TheDarkColdVoidBetweenWorldAndSky")

plotmoonLables = []
for l1, l2 in list(itertools.product('MNO', letters))[:30]:
    plotmoonLables.append(l1 + '\n' + l2)
    labels.append(l1 + l2)

"""
Initiate New Player
"""


async def addMember(inData, member):
    global Data
    loadData(inData)
    # Do Stuff Here

    return saveData()


"""
Function Called on Reaction
"""
async def reaction(inData, action, user, messageid, emoji):
    global Data
    loadData(inData)
    # Do Stuff Here
    message = messageid
    reactorName = user.name + '#' + user.discriminator
    playerName = message.author.name + "#" + str(message.author.discriminator)
    guild = message.guild.id
    splitContent = messageid.content.split(' ')


    if splitContent[0] == '!unit' and len(splitContent) == 3 and reactorName in Admins:
        coords, name = splitContent[1:]
        addMsgQueue(message.channel, "Mod Must Add Unit Manually.")
        """
        if coords in Data[guild]['Units'].keys(): coords, name = name, coords

        coords = extractCoords(coords, message.channel)
        if coords is not None and name in Data[guild]['Units'].keys():
            x, xa, y = coords
            unit = dict(Data[guild]['Units'][name])
            indexTile = None

            try:
                indexTile = Data[guild]['Players'][playerName]['Markers']['Location'].index([x, y])
            except:
                addMsgQueue(message.channel, "You Do Not Own Ths Location")

            if indexTile is not None:
                canAfford = True
                for cost in unit['Costs']:
                    amount, item = cost.split(' ')
                    canAfford = canAfford and addItem(guild, playerName, item, -float(amount), testOnly=True)

                if Data[guild]['Players'][playerName]['Markers']['Shape'][indexTile] == "":
                    addMsgQueue(message.channel, "Units Must Be Upgraded Adjacent To A Claimed Tile")
                elif unit['UpgradeUnit'] != "" and unit['UpgradeUnit'] != \
                        Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]['Unit']['Name']:
                    addMsgQueue(message.channel, "This location cannot be Upgraded To " + name)
                elif unit['UpgradeUnit'] == "" and 'Unit' in \
                        Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]:
                    addMsgQueue(message.channel, "This location Already Has Unit")
                elif canAfford:
                    for cost in unit['Costs']:
                        amount, item = cost.split(' ')
                        addItem(guild, playerName, item, -float(amount))

                    Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]['Unit'] = {'Name': name}
                    addMsgQueue(message.channel, name + "Unit Added On " + str(xa) + str(y + 1) + " For " + playerName)
                else:
                    addMsgQueue(message.channel, "Insufficent Funds")
        else:
            addMsgQueue(message.channel, "Unit Not Found")
        """

    elif splitContent[0] == '!claim' and len(splitContent) == 2 and reactorName == playerName and action == 'add':
        bot = None
        canContinute = True
        for r in message.reactions:
            isBot = False
            for u in await r.users().flatten():
                isBot = u.bot or isBot
                if u.bot:  bot = u
            canContinute = canContinute and isBot

        if canContinute:
            for r in message.reactions:
                if r.emoji not in ['💵', '🌮']:
                    addMsgQueue(message.channel, "Invalid Payment Method You Fool.")
                    canContinute = False
                    break
            if canContinute:
                xcord, xcordAlpha, ycord = extractCoords(splitContent[1], message.channel)
                cost = ""
                amount = 0
                if str(emoji) == '💵':
                    cost = "BF"
                    amount = 2 + Data[guild]['Players'][playerName]['BF Claimed Today']
                elif str(emoji) == '🌮':
                    cost = "Food"
                    index = Data[guild]['Players'][playerName]['Markers']['Shape'].index("Capital")
                    capx, capy = Data[guild]['Players'][playerName]['Markers']['Location'][index]
                    amount = abs(capx - xcord) + abs(capy - ycord)
                else:
                    cost = 'BF'
                    amount = '10000'

                await message.remove_reaction('💵', bot)
                await message.remove_reaction('🌮', bot)
                claimsLeft = 1 + (hasUnit(guild, playerName, 'explorerguild') * 5) \
                - Data[guild]['Players'][playerName]['Claimed Today']
                if claimsLeft <= 0 and cost == "Food":
                    addMsgQueue(message.channel,
                                "You have reached your limit of Non-BF claims. Please wait until tomorrow to claim again. Have a nice day. :v:")
                elif not isTileType(Data[guild]['Image'], xcord, ycord, 'LAND') and cost == "Food":
                    addMsgQueue(message.channel,"There is no capital found on the moon. Please use BF.")

                elif addItem(guild, playerName, cost, -1 * amount):
                    if reactorName in ["Doby's Peri#6151", ]:
                        addMsgQueue(message.channel,
                                    "Bad Kid " + reactorName + " has Claimed with " + str(amount) + ' ' + cost)

                    properties = {}
                    #for player in Data[guild]['Players'].keys():
                    player = botName
                    if [xcord, ycord] in Data[guild]['Players'][player]['Markers']['Location']:
                        index = Data[guild]['Players'][player]['Markers']['Location'].index([xcord,ycord])
                        properties = dict(Data[guild]['Players'][player]['Markers']['Properties'][index])
                        Data[guild]['Players'][player]['Markers']['Location'].pop(index)
                        Data[guild]['Players'][player]['Markers']['Properties'].pop(index)
                        Data[guild]['Players'][player]['Markers']['Shape'].pop(index)

                    Data[guild]['Players'][playerName]['Markers']['Location'].append([xcord, ycord])
                    Data[guild]['Players'][playerName]['Markers']['Properties'].append(properties)
                    Data[guild]['Players'][playerName]['Markers']['Shape'].append('Claim')
                    if cost != 'BF': Data[guild]['Players'][playerName]['Claimed Today'] += 1
                    if cost == 'BF': Data[guild]['Players'][playerName]['BF Claimed Today'] += 1
                    addMsgQueue(message.channel, "You have claimed the location. ")
                else:
                    addMsgQueue(message.channel, "You Do Not Have " + str(amount) + ' ' + cost + " To Claim The Tile")

    elif splitContent[0] == '!trade' and len(splitContent) == 4:
        bot = None
        canContinute = False
        for r in message.reactions:
            isBot = False
            for u in await r.users().flatten():
                isBot = u.bot or isBot
                if u.bot:  bot = u
            canContinute = canContinute or isBot

        if canContinute:
            canContinute = False

            targetName = getPlayer(message.guild, splitContent[1], message.channel)
            if targetName is not None:
                for r in message.reactions:
                    if not r.emoji in ['👍', '👎']:
                        continue
                    for u in await r.users().flatten():
                        if u.name + '#' + u.discriminator == targetName:
                            canContinute = True
                            emoji = r.emoji

                if not canContinute:
                    pass
                elif str(emoji) == '👍':
                    amount = None
                    item = splitContent[-1]
                    try:
                        amount = float(splitContent[-2])
                    except:
                        addMsgQueue(message.channel, splitContent[-2] + ' cannot be quantified into an amount.')

                    if amount is not None \
                            and addItem(guild, playerName, item, -amount, testOnly=True) \
                            and addItem(guild, targetName, item,  amount, testOnly=True):
                        await message.remove_reaction('👍', bot)
                        await message.remove_reaction('👎', bot)

                        addItem(guild, playerName, item, -amount)
                        addItem(guild, targetName, item, amount)

                        addMsgQueue(message.channel, 'Transaction Completed For ' + playerName + ' to ' + targetName)
                    else:
                        addMsgQueue(message.channel, "Resources Unavailable For Trade")
                elif str(emoji) == '👎':
                    await message.remove_reaction('👍', bot)
                    await message.remove_reaction('👎', bot)
                    addMsgQueue(message.channel, 'Transaction Rejected')

    elif splitContent[0] == '!trade' and len(splitContent) == 6:
        bot = None
        canContinute = False
        for r in message.reactions:
            isBot = False
            for u in await r.users().flatten():
                isBot = u.bot or isBot
                if u.bot:  bot = u
            canContinute = canContinute or isBot

        if canContinute:
            canContinute = False

            targetName = getPlayer(message.guild, splitContent[1], message.channel)
            if targetName is not None:
                for r in message.reactions:
                    if not r.emoji in ['👍', '👎']:
                        continue
                    for u in await r.users().flatten():
                        if u.name + '#' + u.discriminator == targetName:
                            canContinute = True
                            emoji = r.emoji

                if not canContinute:
                    pass
                elif str(emoji) == '👍':
                    buyamount = None
                    buyitem = splitContent[-1]
                    sellamount = None
                    sellitem = splitContent[-3]
                    try:
                        buyamount = float(splitContent[-2])
                        sellamount = float(splitContent[-4])
                    except:
                        addMsgQueue(message.channel, 'Item Count cannot be quantified into an amount.')


                    if buyamount is not None \
                        and sellamount is not None \
                        and addItem(guild, playerName, sellitem, -sellamount, testOnly=True) \
                        and addItem(guild, targetName, sellitem, sellamount, testOnly=True) \
                        and addItem(guild, playerName, buyitem, buyamount, testOnly=True) \
                        and addItem(guild, targetName, buyitem, -buyamount, testOnly=True):

                        await message.remove_reaction('👍', bot)
                        await message.remove_reaction('👎', bot)

                        addItem(guild, playerName, buyitem, buyamount)
                        addItem(guild, targetName, sellitem, sellamount)

                        addItem(guild, playerName, sellitem, -sellamount)
                        addItem(guild, targetName, buyitem, -buyamount)

                        addMsgQueue(message.channel, 'Transaction Completed For ' + playerName + ' to ' + targetName)
                    else:
                        addMsgQueue(message.channel, "Resources Unavailable For Trade")
                elif str(emoji) == '👎':
                    await message.remove_reaction('👍', bot)
                    await message.remove_reaction('👎', bot)
                    addMsgQueue(message.channel, 'Transaction Rejected')

    elif splitContent[0].lower() == '!asset':
        bot = None
        canContinute = False
        for r in message.reactions:
            isBot = False
            for u in await r.users().flatten():
                isBot = u.bot or isBot
                if u.bot:  bot = u
            canContinute = canContinute or isBot

        if canContinute:
            canContinute = False
            approvedPlayers = set()
            for r in message.reactions:
                if not r.emoji in ['👍', '👎']: continue
                for u in await r.users().flatten():
                    if r.emoji == '👍':
                        approvedPlayers.add( u.name + '#' + u.discriminator)
            if 1:
                msg =  messageid.content.split('\n')
                giver, reciptient = None, None
                region = set()
                assets = []
                badassets = []
                failed = False
                toSet = []
                players = set()
                for linenum in range(len(msg)):
                    line = str(msg[linenum])
                    print(linenum, line)
                    if 'gives to' not in line and giver is not None and reciptient is not None and len(line) >= 3:
                        asset = line.strip()
                        coord = extractCoords(asset, message.channel)
                        if coord == None:
                            failed = True
                            addMsgQueue(message.channel, 'Failed with bad coord')
                            break
                        else:
                            assets.append((coord[0],coord[2],asset))
                            badassets.append(asset)
                            print('asset added',(coord[0],coord[2]) )
                    if 'gives to' in line or linenum == len(msg)-1:
                        if giver is not None and reciptient is not None:
                            #generate map to ensure all tiles are connected by adjacency
                            assetsToMap = list(assets)
                            region = set()
                            for x,y,a in list(assets):
                                if [x,y] in Data[guild]['Players'][giver]['Markers']['Location'] and (\
                                    [x+1, y+1] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x+1, y  ] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x+1, y-1] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x  , y+1] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x   ,  y] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x  , y-1] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x-1, y+1] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x-1, y  ] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x-1, y-1] in Data[guild]['Players'][reciptient]['Markers']['Location']):
                                    region.add((x+1,y+1))
                                    region.add((x  ,y+1))
                                    region.add((x-1,y+1))
                                    region.add((x+1,y  ))
                                    region.add((x  ,y  ))
                                    region.add((x-1,y  ))
                                    region.add((x+1,y-1))
                                    region.add((x  ,y-1))
                                    region.add((x-1,y-1))

                                    assetsToMap.remove((x, y, a))
                                    badassets.remove(a)

                                    print('Region Seed',x,y)
                            print('Start ATM', assetsToMap)
                            regionExpanded = True
                            while regionExpanded:
                                regionExpanded = False
                                print(assetsToMap)
                                for x,y,a in set(assetsToMap):
                                    if (x,y) in region:
                                        assetsToMap.remove((x,y,a))
                                        badassets.remove(a)
                                        regionExpanded = True
                                        region.add((x+1,y+1))
                                        region.add((x  ,y+1))
                                        region.add((x-1,y+1))
                                        region.add((x+1,y  ))
                                        region.add((x-1,y  ))
                                        region.add((x+1,y-1))
                                        region.add((x  ,y-1))
                                        region.add((x-1,y-1))
                                        region.add((x  ,y  ))
                            print('End ATM', assetsToMap)
                            if len(assetsToMap) != 0:
                                addMsgQueue(message.channel, "Error Trading Tiles:\n "+str('\n\t'.join(badassets)))
                                failed = True
                            else:
                                for x,y,a in set(assets):
                                    tile = [x,y,giver,reciptient]
                                    toSet.append(tile)
                                region = set()
                                assets = []
                                badassets = []
                                print('Done')
                        if linenum != len(msg)-1:
                            giver, reciptient = line.split('gives to')
                            giver      = getPlayer(message.guild, giver.strip()     )
                            reciptient = getPlayer(message.guild, reciptient.strip())
                            players.add(giver)
                            players.add(reciptient)
                    else:
                        print('Else:', line)
                print(players, approvedPlayers)
                if not failed and players.issubset(approvedPlayers):
                    await message.remove_reaction('👍', bot)
                    await message.remove_reaction('👎', bot)
                    for x,y,g,r in toSet:
                        index = Data[guild]['Players'][g]['Markers']['Location'].index([x,y])
                        Data[guild]['Players'][r]['Markers']['Location'].append(Data[guild]['Players'][g]['Markers']['Location'][index])
                        Data[guild]['Players'][r]['Markers']['Shape'].append(Data[guild]['Players'][g]['Markers']['Shape'][index])
                        Data[guild]['Players'][r]['Markers']['Properties'].append(Data[guild]['Players'][g]['Markers']['Properties'][index])
                    for x,y,g,r in toSet:
                        index = Data[guild]['Players'][g]['Markers']['Location'].index([x,y])
                        Data[guild]['Players'][g]['Markers']['Location'].pop(index)
                        Data[guild]['Players'][g]['Markers']['Shape'].pop(index)
                        Data[guild]['Players'][g]['Markers']['Properties'].pop(index)

    elif message.channel.name == 'changelog-live' and action == 'add':
        print('reloading')
        for r in message.reactions:
            for u in await r.users().flatten():
                await message.remove_reaction('🔄', u)

        await updateInAnnouncements(message.guild)
        await message.add_reaction('🔄')


    await sendMessages()
    #task1 = asyncio.ensure_future(
    #    updateInAnnouncements(message.guild))
    return saveData()


"""
Main Run Function On Messages
"""
async def run(inData, payload, message):
    global Data
    loadData(inData)

    start = time.time()
    # Do Stuff Here

    print(message.content)

    guild = message.guild.id
    splitContent = payload['Content'].split(' ')
    update = [0,0,0,]
    #  IF A SERVER CHANNEL
    if payload['Channel Type'] == 'Text':


        if Data[guild]['Pause'] and payload['Content'][0] == '!':
            addMsgQueue(message.channel, "Warning: The Bot Has Been Paused.\n Admins May Ignore This Message")

        if '!rule ' in payload['Content']:return saveData()
        if '!f ' in payload['Content']:return saveData()

        if payload['Content'] == '!map':
            await plotMap(message.channel)
            saveData()

        if payload['Channel'].lower() in ['bot-spam','bot-lounge', 'pizza-party','anti-league-league'] and len(splitContent) != 0:

            if payload['Content'].lower() in ['!units', '!unit']:
                for unit in Data[guild]['Units'].keys():
                    msg = unit + ':\n'
                    for k in Data[guild]['Units'][unit]:
                        msg += '\t' + k + ': ' + str(Data[guild]['Units'][unit][k]) + '\n'
                    addMsgQueue(message.channel, '```' + msg + '```')

            if payload['Content'].lower() in ['!tech', '!techs']:
                msgt = ""
                for technode in TECH_TREE.keys():
                    amount, item = TECH_TREE[technode]['BaseCost'].split(' ')
                    amount = int(amount)

                    msg = '\n\n'+technode.title()
                    msg += '\n  Max Level   : ' + str(TECH_TREE[technode]['MaxLevel'])
                    msg += '\n  Base Cost   : ' + str(TECH_TREE[technode]['BaseCost'])

                    if Data[guild]['Players'][payload['Author']]['TechTree'].get(technode) == TECH_TREE[technode]['MaxLevel']:
                        msg += '\n  Upgrade Cost: At Max Level'
                    else:
                        if TECH_TREE[technode]['InitCost'] is not None:
                            if Data[guild]['Players'][payload['Author']]['TechTree'].get(technode) == 0:
                                amount, item = TECH_TREE[technode]['InitCost'].split(' ')
                            else:
                                amount, item = TECH_TREE[technode]['BaseCost'].split(' ')
                                amount = int(amount) * (
                                        2 ** (Data[guild]['Players'][payload['Author']]['TechTree'].get(technode)-1))
                            print(amount, item)
                        else:
                            amount, item = TECH_TREE[technode]['BaseCost'].split(' ')
                            amount = int(amount) * (
                                        2 ** Data[guild]['Players'][payload['Author']]['TechTree'].get(technode))
                            print(amount, item)

                        msg += '\n  Upgrade Cost: ' + str(amount) +' '+ str(item)
                    msgt += msg
                addMsgQueue(message.channel, '```' + msgt + '```')

            elif splitContent[0] == '!tile' and len(splitContent) == 2:
                coords = extractCoords(splitContent[1], message.channel)
                if coords is not None:
                    xcord, xcordAlpha, ycord = coords
                    msg = "Tile Data:\n"
                    for player in Data[guild]['Players'].keys():
                        try:
                            index = Data[guild]['Players'][player]['Markers']['Location'].index([xcord, ycord])
                            msg += '-' + player + ": " + str(Data[guild]['Players'][player]['Markers']['Shape'][index])
                            msg += '\n EXTRA INFO: ' + str(Data[guild]['Players'][player]['Markers']['Properties'][index])
                        except ValueError:
                            pass
                    addMsgQueue(message.channel, msg)

            elif splitContent[0].lower() == '!asset':
                msg = payload['Content'].split('\n')
                giver, reciptient = None, None
                region = set()
                assets = []
                badassets = []
                failed = False
                toSet = []
                players = set()
                for linenum in range(len(msg)):
                    line = str(msg[linenum])
                    print(linenum, line)
                    if 'gives to' not in line and giver is not None and reciptient is not None and len(line) >= 3:
                        asset = line.strip()
                        coord = extractCoords(asset, message.channel)
                        if coord == None:
                            failed = True
                            addMsgQueue(message.channel, 'Failed with bad coord')
                            break
                        else:
                            assets.append((coord[0], coord[2], asset))
                            badassets.append(asset)
                            print('asset added', (coord[0], coord[2]))
                    if 'gives to' in line or linenum == len(msg) - 1:
                        if giver is not None and reciptient is not None:
                            # generate map to ensure all tiles are connected by adjacency
                            regionExpanded = True
                            for x, y, a in assets:
                                if [x, y] in Data[guild]['Players'][giver]['Markers']['Location'] and ( \
                                                [x + 1, y + 1] in Data[guild]['Players'][reciptient]['Markers'][
                                            'Location'] or \
                                                [x + 1, y] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x + 1, y - 1] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x, y + 1] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x, y - 1] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x - 1, y + 1] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x - 1, y] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x - 1, y - 1] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location']):
                                    region.add((x + 1, y + 1))
                                    region.add((x, y + 1))
                                    region.add((x - 1, y + 1))
                                    region.add((x + 1, y))
                                    region.add((x, y))
                                    region.add((x - 1, y))
                                    region.add((x + 1, y - 1))
                                    region.add((x, y - 1))
                                    region.add((x - 1, y - 1))
                                    print('Region Seed', x, y)
                            assetsToMap = list(assets)
                            print('Start ATM', assetsToMap)
                            while regionExpanded:
                                regionExpanded = False
                                print(assetsToMap)
                                for x, y, a in set(assetsToMap):
                                    if (x, y) in region:
                                        assetsToMap.remove((x, y, a))
                                        badassets.remove(a)
                                        regionExpranded = True
                                        region.add((x + 1, y + 1))
                                        region.add((x, y + 1))
                                        region.add((x - 1, y + 1))
                                        region.add((x + 1, y))
                                        region.add((x - 1, y))
                                        region.add((x + 1, y - 1))
                                        region.add((x, y - 1))
                                        region.add((x - 1, y - 1))
                            print('End ATM', assetsToMap)
                            if len(assetsToMap) != 0:
                                addMsgQueue(message.channel, "Error Trading Tiles:\n " + str('\n\t'.join(badassets)))
                                failed = True
                            else:
                                for x, y, a in set(assets):
                                    tile = [x, y, giver, reciptient]
                                    toSet.append(tile)
                                print('Done')
                        if linenum != len(msg) - 1:
                            giver, reciptient = line.split('gives to')
                            giver = getPlayer(message.guild, giver.strip())
                            reciptient = getPlayer(message.guild, reciptient.strip())
                            players.add(giver)
                            players.add(reciptient)
                    else:
                        print('Else:', line)
                if not failed:
                    addMsgQueue(message.channel, "Asset Trade Requires Approval of: \n" + str(' '.join(players)))
                    await message.add_reaction('👍')
                    await message.add_reaction('👎')

        if payload['Channel'].lower() in ['actions-map',] and len(splitContent) != 0:
            update[0] = 1

            if splitContent[0] == '!start' and len(splitContent) == 3:

                if payload['Author'] in Data[guild]['Players'].keys():
                    addMsgQueue(message.channel, "Silly Rabbit. You already established a Capital.")
                else:
                    coords = extractCoords(splitContent[1], message.channel)
                    if coords is not None:
                        xcord, xcordAlpha, ycord = coords
                        if not isTileType(Data[guild]['Image'], xcord, ycord, 'LAND'):
                            addMsgQueue(message.channel, "Please seek more advanced technology to claim Water Tiles.")
                        elif splitContent[2].lower() in mcd.CSS4_COLORS:
                            Data[guild]['Players'][payload['Author']] = {}
                            Data[guild]['Players'][payload['Author']]['Claimed Today'] = False
                            Data[guild]['Players'][payload['Author']]['Color'] = splitContent[2].lower()
                            Data[guild]['Players'][payload['Author']]['Markers'] = {}
                            Data[guild]['Players'][payload['Author']]['Markers']['Location'] = [[xcord, ycord]]
                            Data[guild]['Players'][payload['Author']]['Markers']['Shape'] = ['Capital']
                            Data[guild]['Players'][payload['Author']]['Markers']['Properties'] = [{}]
                            Data[guild]['Players'][payload['Author']]['Inventory'] = {'BF': 0, }
                            Data[guild]['Fed']['MemberHistory'][payload['Author']] = 0
                        else:
                            addMsgQueue(message.channel, 'Color ' + splitContent[2] + ' is unavailable. Sorry.')

            elif splitContent[0] == '!claim' and len(splitContent) == 2:
                if payload['Author'] not in Data[guild]['Players'].keys():
                    addMsgQueue(message.channel, "You havent established a capital yet.")
                else:
                    coords = extractCoords(splitContent[1], message.channel)
                    if coords is not None:
                        xcord, xcordAlpha, ycord = coords

                        if isTileType(Data[guild]['Image'], xcord, ycord, 'WATER'):
                            addMsgQueue(message.channel, "Please seek more advanced technology to claim Water Tiles.")

                        elif (isTileType(Data[guild]['Image'], xcord, ycord, 'LAND') or isTileType(Data[guild]['Image'], xcord, ycord, 'MEAT'))\
                                and isAdjacent(guild, payload['Author'], [xcord, ycord], False):
                            isClaimed = False
                            for player in Data[guild]['Players'].keys():
                                if botName == player: continue
                                if [xcord, ycord] not in Data[guild]['Players'][player]['Markers']['Location']: continue

                                inde = Data[guild]['Players'][player]['Markers']['Location'].index([xcord, ycord])
                                isClaimed = isClaimed or \
                                            Data[guild]['Players'][player]['Markers']['Shape'][inde] in ['Claim', 'Capital']

                            if isClaimed:
                                addMsgQueue(message.channel, "You cannot claim this location. It is already claimed.")
                            elif hasUnit(guild, payload['Author'], 'explorerguild') != 0:
                                await message.add_reaction('💵')
                                await message.add_reaction('🌮')
                            elif addItem(guild, payload['Author'], 'BF', -2 - Data[guild]['Players'][payload['Author']]['BF Claimed Today']):
                                properties = {}
                                #for player in Data[guild]['Players'].keys():
                                player = botName
                                if [xcord, ycord] in Data[guild]['Players'][player]['Markers']['Location']:
                                    index = Data[guild]['Players'][player]['Markers']['Location'].index([xcord,ycord])
                                    properties = dict(Data[guild]['Players'][player]['Markers']['Properties'][index])
                                    Data[guild]['Players'][player]['Markers']['Location'].pop(index)
                                    Data[guild]['Players'][player]['Markers']['Properties'].pop(index)
                                    Data[guild]['Players'][player ]['Markers']['Shape'].pop(index)


                                Data[guild]['Players'][payload['Author']]['Markers']['Location'].append([xcord, ycord])
                                Data[guild]['Players'][payload['Author']]['Markers']['Properties'].append(properties)
                                Data[guild]['Players'][payload['Author']]['Markers']['Shape'].append('Claim')

                                Data[guild]['Players'][payload['Author']]['BF Claimed Today'] += 1
                                addMsgQueue(message.channel, "You have claimed the location. ")
                            else:
                                addMsgQueue(message.channel,
                                            "You Need " + str(Data[guild]['Players'][payload['Author']][
                                                                  'BF Claimed Today'] + 2) + " Blemflarcks To Complete This Actions.")

                        elif (not isTileType(Data[guild]['Image'], xcord, ycord, 'LAND')) \
                                and isAdjacent(guild, payload['Author'], [xcord, ycord], False):
                            isClaimed = False
                            for player in Data[guild]['Players'].keys():
                                if botName == player: continue
                                if [xcord, ycord] not in Data[guild]['Players'][player]['Markers']['Location']: continue

                                inde = Data[guild]['Players'][player]['Markers']['Location'].index([xcord, ycord])
                                isClaimed = isClaimed or \
                                            Data[guild]['Players'][player]['Markers']['Shape'][inde] in ['Claim',
                                                                                                         'Colony']

                            if isClaimed:
                                addMsgQueue(message.channel, "You cannot claim this location. It is already claimed.")
                                '''elif hasUnit(guild, payload['Author'], 'explorerguild') != 0:
                                await message.add_reaction('💵')
                                await message.add_reaction('🌮')
                                '''

                            elif addItem(guild, payload['Author'], 'BF', -2 - Data[guild]['Players'][payload['Author']]['BF Claimed Today']):
                                properties = {}
                                # for player in Data[guild]['Players'].keys():
                                player = botName
                                if [xcord, ycord] in Data[guild]['Players'][player]['Markers']['Location']:
                                    index = Data[guild]['Players'][player]['Markers']['Location'].index([xcord, ycord])
                                    properties = dict(Data[guild]['Players'][player]['Markers']['Properties'][index])
                                    Data[guild]['Players'][player]['Markers']['Location'].pop(index)
                                    Data[guild]['Players'][player]['Markers']['Properties'].pop(index)
                                    Data[guild]['Players'][player]['Markers']['Shape'].pop(index)

                                Data[guild]['Players'][payload['Author']]['Markers']['Location'].append([xcord, ycord])
                                Data[guild]['Players'][payload['Author']]['Markers']['Properties'].append(properties)
                                Data[guild]['Players'][payload['Author']]['Markers']['Shape'].append('Claim')

                                Data[guild]['Players'][payload['Author']]['BF Claimed Today'] += 1
                                addMsgQueue(message.channel, "You have claimed the location. ")
                            else:
                                addMsgQueue(message.channel,
                                            "You Need "+str(Data[guild]['Players'][payload['Author']]['Claimed Today']+2)+" Blemflarcks To Complete This Actions.")

                        else:
                            addMsgQueue(message.channel,
                                        "You cannot claim this location as you have no adjacent markers.")

            elif splitContent[0] == '!harvest' and len(splitContent) == 3:
                if payload['Author'] not in Data[guild]['Players'].keys():
                    addMsgQueue(message.channel, "You havent established a capital yet.")
                elif splitContent[2].lower() not in ['perpetual', 'non-perpetual', 'p', 'n'] and \
                        splitContent[1].lower() not in ['perpetual', 'non-perpetual', 'p', 'n']:
                    addMsgQueue(message.channel, "That is not a valid harvesting method. \n"
                                                 "If like me you cant spell, just use n (non perpetual) or p (perpetual) in your command.")
                else:
                    if splitContent[1].lower() in ['perpetual', 'non-perpetual', 'p', 'n']:
                        splitContent[1], splitContent[2] = splitContent[2], splitContent[1]

                    coords = extractCoords(splitContent[1], message.channel)
                    if coords is not None:
                        xcord, xcordAlpha, ycord = coords

                        if isTileType(Data[guild]['Image'], xcord, ycord, 'MEAT'):
                            addMsgQueue(message.channel, "You Cannot Harvest A Meat Tile.")
                        elif [xcord, ycord] in Data[guild]['Players'][payload['Author']]['Markers']['Location']:
                            index = Data[guild]['Players'][payload['Author']]['Markers']['Location'].index(
                                [xcord, ycord])

                            if Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index].get('Harvest'):
                                typeHarv = None

                                # Changing Harvest Type
                                if Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Harvest'][
                                    'type'] == 'Perpetual' \
                                        and splitContent[2].lower() in ['non-perpetual', 'n']:
                                    typeHarv = 'Non Perpetual'
                                elif \
                                Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Harvest'][
                                    'type'] == 'Non Perpetual' \
                                        and splitContent[2].lower() in ['perpetual', 'p']:
                                    typeHarv = 'Perpetual'
                                else:
                                    addMsgQueue(message.channel,
                                                "This locations is already being harvested in that method.")

                                if 'Unit' in Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]:
                                    addMsgQueue(message.channel,
                                                "This locations contains a Unit, It cannot be Harvested.")
                                    typeHarv = None

                                cost = {'Perpetual': -4, 'Non Perpetual': -7}
                                if typeHarv is None:
                                    pass
                                elif not addItem(guild, payload['Author'], 'BF', cost[typeHarv]):
                                    addMsgQueue(message.channel,
                                                "You Have Insufficient Blemflarcks To Complete This Actions.")
                                else:
                                    Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index][
                                        'Harvest'] = {
                                        'age': 0,
                                        'type': typeHarv
                                    }
                                    addMsgQueue(message.channel,
                                                "Location Harvest Changed. Resources Will Be Given At The Start Of The Next Turn")
                            else:
                                typeHarv = 'Perpetual'
                                if splitContent[2].lower() in ['non-perpetual', 'n']:
                                    typeHarv = 'Non Perpetual'

                                cost = {'Perpetual': -4, 'Non Perpetual': -7}
                                if 'Unit' in Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]:
                                    addMsgQueue(message.channel,
                                                "This locations contains a Unit, It cannot be Harvested.")

                                elif not addItem(guild, payload['Author'], 'BF', cost[typeHarv]):
                                    addMsgQueue(message.channel,
                                                "You Have Insufficient Blemflarcks To Complete This Actions.")

                                else:
                                    Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index][
                                        'Harvest'] = {
                                        'age': 0,
                                        'type': typeHarv
                                    }
                                    addMsgQueue(message.channel,
                                                "Location set to Harvest. Resources Will Be Given At The Start Of The Next Turn")
                        else:
                            addMsgQueue(message.channel, "You cannot harvest this location until you have claimed it.")

            elif splitContent[0] in ['!unit', '!units'] and len(splitContent) == 3:
                coords, name = splitContent[1:]
                playerName = payload['Author']
                if coords in Data[guild]['Units'].keys(): coords, name = name, coords
                name = name.lower()

                coords = extractCoords(coords, message.channel)
                if coords is not None and name in Data[guild]['Units'].keys():
                    x, xa, y = coords
                    unit = dict(Data[guild]['Units'][name])
                    indexTile = None

                    canAfford = True
                    missingItems = ""
                    for cost in unit['Costs']:
                        amount, item = cost.split(' ')
                        if not addItem(guild, playerName, item, -float(amount), testOnly=True):
                            canAfford = False
                            missingItems += '   ' + str(amount) + ' ' + item + "\n"


                    try: indexTile = Data[guild]['Players'][playerName]['Markers']['Location'].index([x, y])
                    except:  pass

                    if not isAdjacent(guild,playerName, [x,y] ):
                        addMsgQueue(message.channel, "You Do Not Own An Ajacent Location")
                    elif unit['LandOnly'] and not isTileType(Data[guild]['Image'], x, y, 'LAND'):
                        addMsgQueue(message.channel, "This Can Only Be Placed On Land")
                    elif unit['WaterOnly'] and not isTileType(Data[guild]['Image'], x, y, 'WATER'):
                        addMsgQueue(message.channel, "This Can Only Be Placed On Water")
                    elif name in ['town', 'village', 'digsite', 'mill', 'oil', 'mine', 'wall']\
                            and isTileType(Data[guild]['Image'], x, y, 'MEAT'):
                        addMsgQueue(message.channel, "This Unit Cannot Be Placed On A Meat Tile")
                    elif unit['BeachOnly'] and not (
                            isTileType(Data[guild]['Image'], x, y, 'LAND')
                            and (
                                    isTileType(Data[guild]['Image'], x + 1, y, 'WATER') or
                                    isTileType(Data[guild]['Image'], x - 1, y, 'WATER') or
                                    isTileType(Data[guild]['Image'], x, y + 1, 'WATER') or
                                    isTileType(Data[guild]['Image'], x, y - 1, 'WATER')
                            )
                    ): addMsgQueue(message.channel, "This Can Only Be Placed On A Beach")

                    elif name == 'diplomats' and hasUnit(guild,playerName,'diplomats') >= 3*hasUnit(guild,playerName,'embassy'):
                        addMsgQueue(message.channel, "You need more Embassies to make more Diplomats.")

                    elif name == 'sailboat' and not Data[guild]['Players'][playerName]['TechTree']['sailing'] == 1:
                        addMsgQueue(message.channel, "You dont have the Sailing Technology")

                    elif indexTile is not None:
                        if Data[guild]['Players'][playerName]['Markers']['Shape'][indexTile] == "":
                            addMsgQueue(message.channel, "Units Must Be Upgraded On Your Claimed Tile")

                        elif unit['UpgradeUnit'] != "" and unit['UpgradeUnit'] != \
                                Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]['Unit']['Name']:
                            addMsgQueue(message.channel, "This location cannot be Upgraded To " + name)
                        elif unit['UpgradeUnit'] == "" and 'Unit' in \
                                Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]:
                            addMsgQueue(message.channel, "This location Already Has Unit")
                        elif unit['NeedAdminApproval']:
                            addMsgQueue(message.channel, "Awaiting Admin/Mod React on Request For Approval")
                        elif canAfford:
                            for cost in unit['Costs']:
                                amount, item = cost.split(' ')
                                addItem(guild, playerName, item, -float(amount))
                            Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]['Unit']={'Name': name}
                            if name == 'diplomats':
                                Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]['Unit']['Originator'] = playerName
                            addMsgQueue(message.channel, name + "Unit Added On " + str(xa) + str(y + 1) + " ")
                        else:
                            addMsgQueue(message.channel, "Insufficent Funds You Need:" + missingItems)

                    elif indexTile is None:
                        if unit['UpgradeUnit'] != "" :
                            addMsgQueue(message.channel, "This location cannot be Upgraded To " + name)
                        elif unit['NeedAdminApproval']:
                            addMsgQueue(message.channel, "Awaiting Admin/Mod React on Request For Approval")
                        elif canAfford:
                            for cost in unit['Costs']:
                                amount, item = cost.split(' ')
                                addItem(guild, playerName, item, -float(amount))

                            Data[guild]['Players'][playerName]['Markers']['Location'].append([x,y])
                            Data[guild]['Players'][playerName]['Markers']['Shape'].append("")
                            Data[guild]['Players'][playerName]['Markers']['Properties'].append({'Unit':{'Name':name}})
                            addMsgQueue(message.channel, name + "Unit Added On " + str(xa) + str(y + 1) + " ")
                        else:
                            addMsgQueue(message.channel, "Insufficent Funds You Need:" + missingItems)

                elif coords is not None:
                    addMsgQueue(message.channel, "Unit Not Found")

            elif splitContent[0] == '!move' and len(splitContent) == 3:
                coord1 = extractCoords(splitContent[1], message.channel)
                coord2 = extractCoords(splitContent[2], message.channel)
                player = payload['Author']
                if coord1 is not None and coord2 is not None:
                    x1, x1a, y1 = coord1
                    x2, x2a, y2 = coord2
                    index1 = None
                    try: index1 = Data[guild]['Players'][player]['Markers']['Location'].index([x1, y1])
                    except ValueError: pass

                    index2 = None
                    try: index2 = Data[guild]['Players'][player]['Markers']['Location'].index([x2, y2])
                    except ValueError: pass

                    targetOccupied = False
                    unitOccupied = False
                    toMove = None
                    harvOccupied = False
                    for playerTest in Data[guild]['Players']:
                        try:
                            ind = Data[guild]['Players'][playerTest]['Markers']['Location'].index([x2, y2])
                            if 'Unit' in Data[guild]['Players'][playerTest]['Markers']['Properties'][ind]:
                                unitOccupied = True
                            if 'Harvest' in Data[guild]['Players'][playerTest]['Markers']['Properties'][ind]:
                                harvOccupied = True
                        except ValueError:
                            pass
                    name = None
                    unit = None
                    if index1 is None: addMsgQueue(message.channel, "Nothing There To Move")
                    elif 'Harvest' in Data[guild]['Players'][player]['Markers']['Properties'][index1]: toMove = 'Harvest'

                    elif 'Unit' in Data[guild]['Players'][player]['Markers']['Properties'][index1]:
                        toMove = 'Unit'
                        name = Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']['Name']
                        unit = Data[guild]['Units'][name]

                    else: addMsgQueue(message.channel, "Nothing There To Move")

                    if unitOccupied and toMove == 'Unit': addMsgQueue(message.channel, "2 Units cant exist in the same location")

                    elif harvOccupied and toMove == 'Harvest': addMsgQueue(message.channel, "2 Harvests cant exist in the same location")


                    elif toMove == 'Unit' and Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']['Name']\
                            in ['town', 'village', 'digsite', 'mill', 'oil', 'mine', 'wall'] \
                            and isTileType(Data[guild]['Image'], x2, y2, 'MEAT'):
                        addMsgQueue(message.channel, "This Unit Cannot Be Placed On A Meat Tile")

                    elif toMove == 'Harvest' and isTileType(Data[guild]['Image'], x2, y2, 'MEAT'):
                        addMsgQueue(message.channel, "This Harvest Cannot Be Placed On A Meat Tile")

                    elif toMove == 'Harvest' and (index2 is None or Data[guild]['Players'][player]['Markers']['Shape'][index2] != 'Claim'):
                        addMsgQueue(message.channel, "This Harvest Must be placed on a Claim")

                    elif toMove == 'Unit' and (
                            (unit['LandOnly'] and not isTileType(Data[guild]['Image'], x2, y2, 'LAND')) or \
                            (unit['WaterOnly'] and not isTileType(Data[guild]['Image'], x2, y2, 'WATER')) or \
                            (name in ['town', 'village', 'digsite', 'mill', 'oil', 'mine', 'wall'] \
                                and isTileType(Data[guild]['Image'], x2, y2, 'MEAT')) or \
                            (unit['BeachOnly'] and not ( isTileType(Data[guild]['Image'], x2, y2, 'LAND') \
                                and (
                                    isTileType(Data[guild]['Image'], x2 + 1, y2, 'WATER') or
                                    isTileType(Data[guild]['Image'], x2 - 1, y2, 'WATER') or
                                    isTileType(Data[guild]['Image'], x2, y2 + 1, 'WATER') or
                                    isTileType(Data[guild]['Image'], x2, y2 - 1, 'WATER')
                                )
                            ))
                    ):
                        addMsgQueue(message.channel, "This Cant Be Placed On This Type Of Tile")


                    elif toMove == 'Unit' and Data[guild]['Units'][
                            Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']['Name']
                        ]['isMobile']:

                        def landInRange(x,y,r):
                            dirs = [(-1, 0), (1, 0), (0, 1), (0, -1), (1,1), (-1,-1), (1,-1), (-1,1)]
                            if r != 0:
                                res = [ landInRange(x+d[0], y+d[1], r-1) for d in dirs ]
                                res.append(isTileType(Data[guild]['Image'], x, y, 'LAND'))
                                return max(res)
                            if r == 0:
                                return isTileType(Data[guild]['Image'], x, y, 'LAND')


                        name = Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']['Name']
                        dist = min(abs(x1 - x2), abs(y1 - y2)) +  abs(abs(x1 - x2) - abs(y1 - y2))

                        print('Dist: ',dist)
                        print( landInRange(x2,y2,1 + Data[guild]['Players'][player]['TechTree']['sailing']) )

                        if Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit'].get(
                                    'MobileMoveCount') is None:
                            Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit'][
                                'MobileMoveCount'] = 0
                        if dist > Data[guild]['Players'][player]['TechTree']['sailing'] and name == 'sailboat':
                            addMsgQueue(message.channel, "Movement Must Be Within Movement Dist")

                        elif not landInRange(x2,y2,1 + Data[guild]['Players'][player]['TechTree']['sailing']) and name == 'sailboat':
                            addMsgQueue(message.channel, "Movement Must Be Within Range Of Land")

                        elif 'DisabledAndPermanent' in Data[guild]['Players'][player]['Markers']['Properties'][index1]:
                            addMsgQueue(message.channel, "Unit Is Disabled")

                        elif name =='sailboat' and \
                                Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit'][
                                    'MobileMoveCount'] >= Data[guild]['Units'][name]['MoveLimitPerDay']:
                            addMsgQueue(message.channel, "You can only move this unit once per day")

                        else:
                            unit = Data[guild]['Units'][
                                Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']['Name']
                            ]
                            canAfford = True
                            for cost in unit['MobileCost']:
                                amount, item = cost.split(' ')
                                canAfford = canAfford and addItem(guild, payload['Author'], item, -float(amount),
                                                                  testOnly=True)
                            if not canAfford:
                                addMsgQueue(message.channel, "Insufficient Funds To Move")
                            else:
                                for cost in unit['MobileCost']:
                                    amount, item = cost.split(' ')
                                    addItem(guild, payload['Author'], item, -float(amount))
                                Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit'][
                                    'MobileMoveCount'] += 1
                                if index2 is None:
                                    Data[guild]['Players'][player]['Markers']['Properties'].append({
                                        'Unit': Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']
                                    })
                                    Data[guild]['Players'][player]['Markers']['Shape'].append("")
                                    Data[guild]['Players'][player]['Markers']['Location'].append([x2, y2])
                                    del Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']
                                else:
                                    Data[guild]['Players'][player]['Markers']['Properties'][index2]['Unit'] \
                                        = dict(Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit'])
                                    del Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']

                                if Data[guild]['Players'][player]['Markers']['Shape'][index1] == "":
                                    del Data[guild]['Players'][player]['Markers']['Location'][index1]
                                    del Data[guild]['Players'][player]['Markers']['Shape'][index1]
                                    del Data[guild]['Players'][player]['Markers']['Properties'][index1]

                                addMsgQueue(message.channel,
                                            "Moving Unit From " + x1a + str(y1 + 1) + " to " + x2a + str(y2 + 1))

                    elif toMove is not None:
                        hist =  Data[guild]['Players'][player]['Markers']['Properties'][index1][toMove].get('MoveCount')
                        if hist is None:
                            Data[guild]['Players'][player]['Markers']['Properties'][index1][toMove]['MoveCount'] = 0
                            hist = 0
                        amount = 3**hist
                        item = 'Energy'
                        canAfford = addItem(guild, payload['Author'], item, -float(amount),
                                                              testOnly=True)
                        if not isAdjacent(guild, payload['Author'], [x2, y2]):
                            addMsgQueue(message.channel, "Target is not adjacent to a claim")

                        elif canAfford:
                            addItem(guild, payload['Author'], item, -float(amount))
                            Data[guild]['Players'][player]['Markers']['Properties'][index1][toMove]['MoveCount'] += 1
                            if index2 is None:
                                Data[guild]['Players'][player]['Markers']['Properties'].append({
                                    toMove: dict(
                                        Data[guild]['Players'][player]['Markers']['Properties'][index1][toMove])
                                })
                                Data[guild]['Players'][player]['Markers']['Shape'].append("")
                                Data[guild]['Players'][player]['Markers']['Location'].append([x2, y2])
                                del Data[guild]['Players'][player]['Markers']['Properties'][index1][toMove]
                            else:
                                Data[guild]['Players'][player]['Markers']['Properties'][index2][toMove] \
                                    = dict(Data[guild]['Players'][player]['Markers']['Properties'][index1][toMove])
                                del Data[guild]['Players'][player]['Markers']['Properties'][index1][toMove]

                            if Data[guild]['Players'][player]['Markers']['Shape'][index1] == "":
                                del Data[guild]['Players'][player]['Markers']['Location'][index1]
                                del Data[guild]['Players'][player]['Markers']['Shape'][index1]
                                del Data[guild]['Players'][player]['Markers']['Properties'][index1]

                            addMsgQueue(message.channel,
                                        "Moving From " + x1a + str(y1 + 1) + " to " + x2a + str(y2 + 1))

            elif splitContent[0] == '!toggle' and len(splitContent) == 2:
                coords = extractCoords(splitContent[1], message.channel)
                if coords is not None:
                    xcord, xcordAlpha, ycord = coords
                    index = Data[guild]['Players'][payload['Author']]['Markers']['Location'].index([xcord, ycord])
                    if 'Unit' not in Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]:
                        addMsgQueue(message.channel, "No Unit At That Location.")

                    elif 'DisabledAndPermanent' in Data[guild]['Players'][payload['Author']]['Markers']['Properties'][
                        index]['Unit'] and \
                            Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Unit'][
                                'DisabledAndPermanent']:
                        del Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Unit'][
                            'DisabledAndPermanent']
                        addMsgQueue(message.channel, "Location Enabled.")
                    else:
                        Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Unit'][
                            'DisabledAndPermanent'] = True
                        addMsgQueue(message.channel, "Location Disabled.")
                else:
                    addMsgQueue(message.channel, "You cannot disable this location.")

            elif splitContent[0] == '!raze' and len(splitContent) == 3:
                if splitContent[1] in ['claim', 'harvest', 'unit']:
                    coords = extractCoords(splitContent[2],message.channel)
                    if coords is not None:
                        x,xa,y = coords

                        if [x,y] not in Data[guild]['Players'][payload['Author']]['Markers']['Location']:
                            addMsgQueue(message.channel, "You do not own the Tile")
                        else:
                            index = Data[guild]['Players'][payload['Author']]['Markers']['Location'].index([x,y])
                            prop = dict( Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index] )
                            print(prop)
                            if splitContent[1] == 'claim':
                                if len(prop) != 0:
                                    Data[guild]['Players'][botName]['Markers']['Location'].append([x,y])
                                    Data[guild]['Players'][botName]['Markers']['Shape'].append('Claim')
                                    Data[guild]['Players'][botName]['Markers']['Properties'].append(prop)

                                Data[guild]['Players'][payload['Author']]['Markers']['Location'].pop(index)
                                Data[guild]['Players'][payload['Author']]['Markers']['Shape'].pop(index)
                                Data[guild]['Players'][payload['Author']]['Markers']['Properties'].pop(index)
                                addMsgQueue(message.channel, "Claim Razed")

                            elif splitContent[1] == 'harvest':
                                if prop.get('Harvest') is None:
                                    addMsgQueue(message.channel, "Harvest Not Found On Tile")
                                elif addItem(guild, payload['Author'], 'BF', -1):
                                    if prop['Harvest']['type'] == 'Non Perpetual':
                                        addItem(guild, payload['Author'], 'Steel', 1)
                                    if prop['Harvest']['type'] == 'Perpetual':
                                        addItem(guild, payload['Author'], 'Corn', 1)
                                    del Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Harvest']
                                    addMsgQueue(message.channel, "Harvest Razed")
                                else:
                                    addMsgQueue(message.channel, "You Need 1 BF to raze a harvest")

                            elif splitContent[1] == 'unit':
                                if prop.get('Unit') is None:
                                    addMsgQueue(message.channel, "Unit Not Found On Tile")
                                elif addItem(guild, payload['Author'], 'BF', -2):
                                    name = prop['Unit']['Name']
                                    unit = dict(Data[guild]['Units'][name])

                                    for cost in unit['Costs']:
                                        if ' ' in cost:
                                            amount, item = cost.split(' ')
                                            print('amount',math.ceil(0.2*float(amount)))
                                            addItem(guild, payload['Author'], item, math.ceil(0.2*float(amount)))
                                    for cost in unit['DailyCosts']:
                                        if ' ' in cost:
                                            amount, item = cost.split(' ')
                                            addItem(guild, payload['Author'], item, 1)
                                    for cost in unit['DailyReturn']:
                                        if ' ' in cost:
                                            amount, item = cost.split(' ')
                                            addItem(guild, payload['Author'], item, 1)

                                    del Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Unit']

                                    if Data[guild]['Players'][payload['Author']]['Markers']['Shape'][index] in ["", "None"]:
                                        del Data[guild]['Players'][payload['Author']]['Markers']['Shape'][index]
                                        del Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]
                                        del Data[guild]['Players'][payload['Author']]['Markers']['Location'][index]

                                    addMsgQueue(message.channel, "Unit Razed")
                                else:
                                    addMsgQueue(message.channel, "You Need 2 BF to raze a unit")



                else:
                    addMsgQueue(message.channel, "Can only raze a claim, harvest, or unit")

            elif splitContent[0] == '!dig' and len(splitContent) == 2:
                coords = extractCoords(splitContent[1], message.channel)
                if coords is not None:
                    xcord, xcordAlpha, ycord = coords
                    index = Data[guild]['Players'][payload['Author']]['Markers']['Location'].index([xcord, ycord])
                    if 'Unit' not in Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]\
                            or 'digsite' != Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Unit']['Name']:
                        addMsgQueue(message.channel, "No Dig Site At That Location.")

                    elif Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Unit']['Artifact']:
                        Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Unit']['Artifact'] = False
                        addItem(guild,payload['Author'],'Artifact',1)
                        addMsgQueue(message.channel, "You Collected 1 Artifact.")

            elif splitContent[0] == '!tech' and len(splitContent) >=2:
                technode = ' '.join(splitContent[1:]).lower()
                amount, item = 0, None
                if technode in TECH_TREE:
                    if TECH_TREE[technode]['InitCost'] is not None:
                        if Data[guild]['Players'][payload['Author']]['TechTree'].get(technode) == 0:
                            amount, item = TECH_TREE[technode]['InitCost'].split(' ')
                        else:
                            amount, item = TECH_TREE[technode]['BaseCost'].split(' ')
                            amount = int(amount) * (
                                        2 ** (Data[guild]['Players'][payload['Author']]['TechTree'].get(technode)-1))
                        print(amount, item)
                    else:
                        amount, item = TECH_TREE[technode]['BaseCost'].split(' ')
                        amount = int(amount) * (2 ** Data[guild]['Players'][payload['Author']]['TechTree'].get(technode))
                        print(amount, item)

                    if addItem(guild, payload['Author'], item, -float(amount), testOnly=True):
                        addItem(guild, payload['Author'], item, -float(amount))
                        Data[guild]['Players'][payload['Author']]['TechTree'][technode] += 1

                        addMsgQueue(message.channel, "Tech Node Updated ")
                    else:
                        addMsgQueue(message.channel, "You do not have "+str(amount) + ' '+item)


                else:
                    addMsgQueue(message.channel, "Tech Node not Found.")

            else: update[0] = False

        if payload['Channel'].lower() in ['actions',] and len(splitContent) != 0:
            update[1] = 1

            if splitContent[0] == '!trade' and len(splitContent) == 4:
                for playerid in splitContent[1:-2]:
                    playerName = getPlayer(message.guild, playerid, message.channel)

                    if playerName is not None:
                        amount = None
                        item = splitContent[-1]
                        try:
                            amount = float(splitContent[-2])
                        except:
                            addMsgQueue(message.channel, splitContent[-2] + ' cannot be quantified into an amount.')


                        if amount is not None \
                                and addItem(guild, payload['Author'], item, -amount, testOnly=True) \
                                and addItem(guild, playerName, item, amount, testOnly=True):

                            await message.add_reaction('👍')
                            await message.add_reaction('👎')
                        else:
                            addMsgQueue(message.channel, "You Do Not Have The Resources")

            elif splitContent[0] == '!trade' and len(splitContent) == 6:
                for playerid in splitContent[1:-4]:
                    playerName = getPlayer(message.guild, playerid, message.channel)

                    if playerName is not None:
                        buyamount = None
                        buyitem = splitContent[-1]
                        sellamount = None
                        sellitem = splitContent[-3]
                        try:
                            buyamount = float(splitContent[-2])
                            sellamount = float(splitContent[-4])
                        except:
                            addMsgQueue(message.channel, 'Item Count cannot be quantified into an amount.')

                        if buyamount is not None \
                                and sellamount is not None \
                                and addItem(guild, payload['Author'],   sellitem, -sellamount, testOnly=True) \
                                and addItem(guild, playerName,          sellitem, sellamount, testOnly=True) \
                                and addItem(guild, payload['Author'],   buyitem, buyamount, testOnly=True) \
                                and addItem(guild, playerName,          buyitem, -buyamount, testOnly=True):

                            await message.add_reaction('👍')
                            await message.add_reaction('👎')
                        else:
                            addMsgQueue(message.channel, "Resources Unavailable")

            elif splitContent[0].lower() == '!asset':
                msg = payload['Content'].split('\n')
                giver, reciptient = None, None
                region = set()
                assets = []
                badassets = []
                failed = False
                toSet = []
                players = set()
                for linenum in range(len(msg)):
                    line = str(msg[linenum])
                    print(linenum, line)
                    if 'gives to' not in line and giver is not None and reciptient is not None and len(line) >= 3:
                        asset = line.strip()
                        coord = extractCoords(asset, message.channel)
                        if coord == None:
                            failed = True
                            addMsgQueue(message.channel, 'Failed with bad coord')
                            break
                        else:
                            assets.append((coord[0], coord[2], asset))
                            badassets.append(asset)
                            print('asset added', (coord[0], coord[2]))
                    if 'gives to' in line or linenum == len(msg) - 1:
                        if giver is not None and reciptient is not None:
                            # generate map to ensure all tiles are connected by adjacency
                            regionExpanded = True
                            assetsToMap = list(assets)
                            region = set()
                            for x, y, a in assets:
                                if [x, y] in Data[guild]['Players'][giver]['Markers']['Location'] and ( \
                                                [x + 1, y + 1] in Data[guild]['Players'][reciptient]['Markers'][
                                            'Location'] or \
                                                [x + 1, y] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x + 1, y - 1] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x, y + 1] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x, y - 1] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x - 1, y + 1] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x - 1, y] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location'] or \
                                                [x - 1, y - 1] in Data[guild]['Players'][reciptient]['Markers'][
                                                    'Location']):
                                    region.add((x + 1, y + 1))
                                    region.add((x, y + 1))
                                    region.add((x - 1, y + 1))
                                    region.add((x + 1, y))
                                    region.add((x, y))
                                    region.add((x - 1, y))
                                    region.add((x + 1, y - 1))
                                    region.add((x, y - 1))
                                    region.add((x - 1, y - 1))

                                    badassets.remove(a)
                                    assetsToMap.remove((x, y, a))
                                    print('Region Seed', x, y)
                            print('Start ATM', len(assetsToMap))
                            while regionExpanded:
                                regionExpanded = False
                                print('Step:',len(assetsToMap))
                                for x, y, a in set(assetsToMap):
                                    if (x, y) in region:
                                        print('Mapped:',[x,y])
                                        assetsToMap.remove((x, y, a))
                                        badassets.remove(a)
                                        regionExpanded = True
                                        region.add((x + 1, y + 1))
                                        region.add((x, y + 1))
                                        region.add((x - 1, y + 1))
                                        region.add((x + 1, y))
                                        region.add((x - 1, y))
                                        region.add((x + 1, y - 1))
                                        region.add((x, y - 1))
                                        region.add((x - 1, y - 1))
                                print('Step:',len(assetsToMap))
                            print('End ATM', assetsToMap)
                            if len(assetsToMap) != 0:
                                addMsgQueue(message.channel, "Error Trading Tiles:\n " + str('\n\t'.join(badassets)))
                                failed = True
                            else:
                                for x, y, a in set(assets):
                                    tile = [x, y, giver, reciptient]
                                    toSet.append(tile)
                                print('Done')
                                region = set()
                                assets = []
                                badassets = []
                        if linenum != len(msg) - 1:
                            giver, reciptient = line.split('gives to')
                            giver = getPlayer(message.guild, giver.strip())
                            reciptient = getPlayer(message.guild, reciptient.strip())
                            players.add(giver)
                            players.add(reciptient)
                    else:
                        print('Else:', line)
                if not failed:
                    addMsgQueue(message.channel, "Asset Trade Requires Approval of: \n" + str(' '.join(players)))
                    await message.add_reaction('👍')
                    await message.add_reaction('👎')

            elif splitContent[0] == '!sell' and len(splitContent) == 3:
                print('selling')
                amount = None
                item = splitContent[-1]
                try:
                    amount = float(splitContent[-2])
                except:
                    addMsgQueue(message.channel, splitContent[-2] + ' cannot be quantified into an amount.')
                if amount < 0:
                    addMsgQueue(message.channel, 'You cannot sell negative stuff.')
                elif Data[guild]['Fed']['Rates'].get(item) is None:
                    addMsgQueue(message.channel, 'I dont buy that item. Sorry.')
                elif amount is not None \
                        and addItem(guild, payload['Author'], item, -amount, testOnly=True):
                    addItem(guild, payload['Author'], item, -amount)
                    amount = math.floor(amount / Data[guild]['Fed']['Rates'][item])
                    addItem(guild, payload['Author'], 'BF', amount)
                    addMsgQueue(message.channel, "Here is "+str(amount)+' BF. Enjoy.')
                else:
                    addMsgQueue(message.channel, 'Insufficient Items to Sell')

            else: update[1] = False

    if payload['Author'] in Admins and payload['Channel'].lower() in ['actions', 'actions-map', 'mod-lounge',
                                                                          'bot-lounge']:
        update[2] = 1
        if payload['Content'] == '!csv':
            print ('csv')
            import csv
            csv_columns = ['BF', 'Corn', 'Compensation Fish', 'Food', 'Steel', 'Oil', 'Wood', 'Technology', 'Energy','Gloop','Wine','Cracker','Cute_Dog', 'Cake','food']
            csv_columns = ['Name',]+csv_columns
            dict_data = []
            for player in Data[guild]['Players'].keys():
                s =  dict(Data[guild]['Players'][player]['Inventory'])
                s['Name'] = player
                dict_data.append( s )
            csv_file = "Inventories.csv"
            try:
                with open(csv_file, 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    writer.writeheader()
                    for data in dict_data:
                        writer.writerow(data)
                await message.channel.send(
                   'CSV Inventory:', file=discord.File(open(csv_file, 'br')))
            except IOError:
                print("I/O error")

        elif payload['Content'] == '!newTurn':
            await onTurnChange(message.guild)
            addMsgQueue(message.channel, "New Turn Initiated")
            print('New Turn')

        elif splitContent[0] == '!newDay':
            onDayChange(message.guild)
            #task1 = asyncio.ensure_future(
            #    updateInAnnouncements(message.guild, postToSpam=True))

        elif payload['Content'] == '!getData':
            await sendMapData(guild=message.guild.id, channel=message.channel)
            print("sending Map_Data File")

        elif splitContent[0] == '!remove' and len(splitContent) == 2:
            if len(splitContent[1]) <= 4:
                coords = extractCoords(splitContent[1], message.channel)
                if coords is not None:
                    xcord, xcordAlpha, ycord = coords
                    for player in Data[guild]['Players'].keys():
                        try:
                            index = Data[guild]['Players'][player]['Markers']['Location'].index([xcord, ycord])
                            del Data[guild]['Players'][player]['Markers']['Location'][index]
                            del Data[guild]['Players'][player]['Markers']['Shape'][index]
                            del Data[guild]['Players'][player]['Markers']['Properties'][index]
                        except ValueError:
                            pass
                    addMsgQueue(message.channel, "Tile Removed")

            else:
                player = getPlayer(message.guild, splitContent[1], message.channel)
                if player is not None:
                    del Data[guild]['Players'][player]
                    addMsgQueue(message.channel, 'Player ' + player + ' is removed from the Map.')

        elif splitContent[0] == '!setPlayer' and len(splitContent) == 3:

            player1 = splitContent[1]
            player2 = splitContent[2]

            if player1 not in Data[guild]['Players']:
                addMsgQueue(message.channel, 'Player cannot be found. Sorry.')
            elif player1 is not None and player2 is not None:
                Data[guild]['Players'][player2] = dict(Data[guild]['Players'][player1])
                del Data[guild]['Players'][player1]
                addMsgQueue(message.channel, 'Player ' + player1 + ' is now ' +player2)

        elif splitContent[0] == '!setColor' and len(splitContent) == 3:
            if splitContent[1].lower() in mcd.CSS4_COLORS:
                splitContent[1], splitContent[2] = splitContent[2], splitContent[1]

            player = getPlayer(message.guild, splitContent[1], message.channel)
            if splitContent[2].lower() not in mcd.CSS4_COLORS:
                addMsgQueue(message.channel, 'Color ' + splitContent[2] + ' is unavailable. Sorry.')
            elif player is not None:
                Data[guild]['Players'][player]['Color'] = splitContent[2].lower()
                addMsgQueue(message.channel, 'Player ' + player + ' is now ' + splitContent[2].lower())

        elif splitContent[0] == '!getTile' and len(splitContent) == 2:
            coords = extractCoords(splitContent[1], message.channel)
            if coords is not None:
                xcord, xcordAlpha, ycord = coords
                msg = "Tile Data:\n"

                msg += str(Data[guild]["Image"][xcord,ycord]) + "\n"

                for player in Data[guild]['Players'].keys():
                    try:
                        index = Data[guild]['Players'][player]['Markers']['Location'].index([xcord, ycord])
                        msg += '-' + player + ": " + str(Data[guild]['Players'][player]['Markers']['Shape'][index])
                        msg += '\n' + str(Data[guild]['Players'][player]['Markers']['Properties'][index])
                    except ValueError:
                        pass
                addMsgQueue(message.channel, msg)

        elif splitContent[0] == '!setTile' and len(splitContent) >= 5:
            coords = extractCoords(splitContent[1], message.channel)
            playerName = getPlayer(message.guild, splitContent[2], message.channel)
            shape = splitContent[3]
            properties = eval(' '.join(splitContent[4:]))

            if not isinstance(properties, (dict,)):
                addMsgQueue(message.channel, 'Properties Is Not Dict.')
            elif shape not in ['Claim', 'Capital', 'None', 'Colony']:
                addMsgQueue(message.channel, 'Shape is Not Claim or Capital')
            elif coords is not None and playerName is not None:
                if shape == 'None':shape = ""
                x, xa, y = coords
                '''
                for player2 in Data[guild]['Players'].keys():
                    try:
                        index = Data[guild]['Players'][player2]['Markers']['Location'].index([x, y])
                        del Data[guild]['Players'][player2]['Markers']['Location'][index]
                        del Data[guild]['Players'][player2]['Markers']['Shape'][index]
                        del Data[guild]['Players'][player2]['Markers']['Properties'][index]
                    except ValueError:
                        pass
                '''
                try:
                    index = Data[guild]['Players'][playerName]['Markers']['Location'].index([x, y])
                    del Data[guild]['Players'][playerName]['Markers']['Location'][index]
                    del Data[guild]['Players'][playerName]['Markers']['Shape'][index]
                    del Data[guild]['Players'][playerName]['Markers']['Properties'][index]
                except ValueError:
                    pass
                Data[guild]['Players'][playerName]['Markers']['Location'].append([x, y])
                Data[guild]['Players'][playerName]['Markers']['Shape'].append(shape)
                Data[guild]['Players'][playerName]['Markers']['Properties'].append(properties)

                addMsgQueue(message.channel, 'Marker Changes Set.')

        elif splitContent[0] in ['!resetTimer', '!resetTimers']:
            playerid = None
            if len(splitContent) == 2:
                playerid = splitContent[1]
            resetTimers(message.guild, playerid=playerid, channel=message.channel)

        elif splitContent[0] == ['!setTimer', '!setTimers']:
            playerid = None
            if len(splitContent) == 2:
                playerid = splitContent[1]
            resetTimers(message.guild, playerid=playerid, channel=message.channel, mode=True)

        elif splitContent[0] == '!give':
            for playerid in splitContent[1:-2]:
                playerName = getPlayer(message.guild, playerid, message.channel)

                if playerName is not None:
                    amount = None
                    item = splitContent[-1]
                    try:
                        amount = float(splitContent[-2])
                    except:
                        addMsgQueue(message.channel, splitContent[-2] + ' cannot be quantified into an amount.')
                    if amount is not None:
                        addItem(guild, playerName, item, amount)
                        addMsgQueue(message.channel, 'Transaction Completed For ' + playerName)

        elif payload['Content'] == '!pause':
            Data[guild]['Pause'] = not Data[guild]['Pause']
            addMsgQueue(message.channel, "You Have Paused/Unpaused The Bot. Pause is " + str(Data[guild]['Pause']))

        elif payload['Content'] == '!subtractTurn':
            for player in Data[guild]['Players'].keys():
                for i in range(len(Data[guild]['Players'][player]['Markers']['Shape'])):
                    for prop in Data[guild]['Players'][player]['Markers']['Properties'][i].keys():
                        if prop == 'Harvest':
                            Data[guild]['Players'][player]['Markers']['Properties'][i][prop]['age'] -= 1
            addMsgQueue(message.channel, "Every Player Had one Turn Removed Form Harvest Count")

        elif payload['Content'] == '!ping':
            addMsgQueue(message.channel, "pong")

        elif splitContent[0] == '!mark' and len(splitContent) == 4:
            location, marker, player = splitContent[1:]
            if len(marker) > len(player): marker, player = player, marker
            if marker[0] == '"' and marker[-1] == '"':
                marker = '${0}$'.format(marker[1:-1])

            coords = extractCoords(location, message.channel)
            player = getPlayer(message.guild, player, message.channel)
            if player is not None and coords is not None:
                x, xa, y = coords
                for player2 in Data[guild]['Players'].keys():
                    try:
                        index = Data[guild]['Players'][player2]['Markers']['Location'].index([x, y])
                        del Data[guild]['Players'][player2]['Markers']['Location'][index]
                        del Data[guild]['Players'][player2]['Markers']['Shape'][index]
                        del Data[guild]['Players'][player2]['Markers']['Properties'][index]
                    except ValueError:
                        pass
                Data[guild]['Players'][player]['Markers']['Location'].append([x, y])
                Data[guild]['Players'][player]['Markers']['Shape'].append(marker)
                Data[guild]['Players'][player]['Markers']['Properties'].append({'Unit': {}})
                addMsgQueue(message.channel, "Location Marked")

        elif splitContent[0] == '!newUnit' and len(splitContent) == 1:
            addMsgQueue(message.channel, str(UNIT_BASE))

        elif splitContent[0] == '!newUnit' and len(splitContent) > 1:
            name = splitContent[1].lower()
            data = dict(eval(' '.join(splitContent[2:])))

            if name in Data[guild]['Units']:
                addMsgQueue(message.channel, "Replacing Existing Unit...")

            requirements = dict(UNIT_BASE)
            for key in data.keys():
                if requirements.get(key) is not None:
                    requirements[key] = data[key]
            Data[guild]['Units'][name] = requirements

            addMsgQueue(message.channel, "Unit Saved")

        elif splitContent[0] == '!removeUnit' and len(splitContent) == 2:
            name = splitContent[1]

            if name in Data[guild]['Units']:
                del Data[guild]['Units'][name]
                addMsgQueue(message.channel, "Removeing Existing Unit...")
            else:
                addMsgQueue(message.channel, "Unit Not Found")

        elif splitContent[0] == '!setTerm' and len(splitContent) == 2:
            try:
                term = int(splitContent[1])
                Data[guild]['Fed']['Term']=term
            except:
                addMsgQueue(message.channel, splitContent[-2] + ' cannot be quantified into a term 0-5')

        elif splitContent[0] == '!adjust':
            import re
            if splitContent[-1].lower() in ['increasing', 'static', 'decreasing']:
                for item in splitContent[1:-2]:
                    if item not in Data[guild]['Fed']['Velocity']:
                        addMsgQueue(message.channel, item+" Not Found..Skipped")
                    elif splitContent[-1].lower() == 'increasing':
                        Data[guild]['Fed']['Velocity'][item] = 10.0
                    elif splitContent[-1].lower() == 'decreasing':
                        Data[guild]['Fed']['Velocity'][item] = -10.0
                    elif splitContent[-1].lower()  == 'static':
                        Data[guild]['Fed']['Velocity'][item] = 0
            elif re.match("^\d+?\.\d+?$", splitContent[-1]) is not None:
                for item in splitContent[1:-2]:
                   Data[guild]['Fed']['Rates'][item] = 1.0/float(splitContent[-1])
            else:
                addMsgQueue(message.channel, "Not a valid velocity")
            addMsgQueue(message.channel,'Fed Market Updated')

        elif splitContent[0] == '!specialCommand':

            array = np.random.rand(75,75)*175
            array[2,13] = 0.5

            coords = np.where(array<=1)
            for x,y in zip(coords[0], coords[1]):
                if isTileType(Data[guild]['Image'],x,y,'LAND'):
                    print(x, y)
                    isOnPlayer = False
                    for player in Data[guild]['Players'].keys():
                        if [x,y] in Data[guild]['Players'][player]['Markers']['Location']:
                            print(1,player)
                            index = Data[guild]['Players'][player]['Markers']['Location'].index([x,y])

                            if 'Unit' not in Data[guild]['Players'][player]['Markers']['Properties'][index]:
                                Data[guild]['Players'][player]['Markers']['Properties'][index][
                                    'Unit'] = 'town'
                                Data[guild]['Players'][player]['Markers']['Properties'][index][
                                    'TownItem'] = random.choice(rawMaterialsList)

                            isOnPlayer = True
                    if not isOnPlayer:
                        Data[guild]['Players'][botName]['Markers']['Shape'].append("")
                        Data[guild]['Players'][botName]['Markers']['Location'].append([x,y])
                        Data[guild]['Players'][botName]['Markers']['Properties'].append({
                            'Unit': {
                                'Name':'town',
                                'TownItem': random.choice(rawMaterialsList)
                            }
                        })

        elif splitContent[0] == '!setVinny' and len(splitContent) == 2:
            coords = extractCoords(splitContent[1], message.channel)
            if coords is not None:
                Data[guild]['Vinny']['Position'] = [coords[0],coords[2]]

        elif splitContent[0] == '!setTech' and len(splitContent) > 3:
            playerName = getPlayer(message.guild, splitContent[1], message.channel)
            technode = ' '.join(splitContent[2:-1]).lower()
            try: level = int(splitContent[-1])
            except: addMsgQueue(message.channel, splitContent[-1] + ' cannot be quantified into a level 0-10')

            print([playerName,technode,level])
            if technode in TECH_TREE:
                Data[guild]['Players'][playerName]['TechTree'][technode] = level
                addMsgQueue(message.channel, 'Level Changed')
            else:
                addMsgQueue(message.channel, 'Node Not Found')

        elif splitContent[0] == '!postUpdate':
            post = await channels[guild]['changelog-live'].send('Update Button')
            await post.add_reaction('🔄')

        else: update[2] = False

    #  IF A DM CHANNEL
    if payload['Channel Type'] == 'DM':
        pass

    await sendMessages()
    #if '!' in payload['Content'] and 1 in update:
    #    print("Run- " + payload['Content'] + ': ', time.time() - start)
    #    asyncio.ensure_future(
    #        updateInAnnouncements(message.guild))


    return saveData()


"""
Update Function Called Every 10 Seconds
"""
async def update(inData, server):
    global Data
    loadData(inData)
    # Do Stuff Here

    guild = server.id
    if (datetime.datetime.now()+ datetime.timedelta(hours=1)).strftime("%Y-%m-%d")!= Data[guild]['Date']:
        Data[guild]['Date'] = (datetime.datetime.now()+ datetime.timedelta(hours=1)).strftime("%Y-%m-%d")

        await sendMapData(guild, channels[guild][logChannel])
        onDayChange(server)
        await updateInAnnouncements(server,postToSpam=True)
    await sendMessages()
    return saveData()


"""
Reset All Claim Timers
"""
def onDayChange(server):
    start = time.time()
    guild = server.id
    print('Day Changing...')

    resetTimers(server)

    for chan in ['action', 'actions']:
        if chan in channels[guild].keys():
            addMsgQueue(channels[guild][chan],
                        "New Day Actions Completed: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    log(guild, "Day " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    for player in Data[guild]['Players']:

        cursed = not Data[guild]['Players'][player]['Inventory'].get('Curse') in [0, None]

        if Data[guild]['Players'][player]['Inventory'].get('Curse') not in [0,None]:
            del Data[guild]['Players'][player]['Inventory']['Curse']
        for markerTier in TIERLIST:

            def checktier(prop,tier):
                subtiers = True
                for name, subtier in tier.items():
                    subtiers = subtiers and (name in prop)
                    if isinstance(subtier,dict) and subtiers:
                        subtiers = subtiers and checktier(prop[name],subtier)
                    elif isinstance(subtier,str) and subtiers:
                        subtiers = subtiers and subtier == prop[name]

                return subtiers

            numFound = 0
            for tileIndex in range(len(Data[guild]['Players'][player]['Markers']['Shape'])):
                if not checktier(Data[guild]['Players'][player]['Markers']['Properties'][tileIndex],markerTier): continue
                numFound += 1
                # IF HARVEST
                if 'Harvest' in markerTier and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].get('Harvest') is not None \
                        and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].get('Unit') is None:
                    xcord, ycord = Data[guild]['Players'][player]['Markers']['Location'][tileIndex]
                    double = 'Boost' in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']
                    modifier = (1 - cursed * 0.5) * (double + 1)

                    if double:
                        del Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['Boost']

                    if isTileType(Data[guild]['Image'], xcord, ycord, 'LAND') and \
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                                'type'] == 'Perpetual':                    addItem(guild, player, 'Corn', 3 * modifier)

                    if isTileType(Data[guild]['Image'], xcord, ycord, 'LAND') and \
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                                'type'] == 'Non Perpetual':                    addItem(guild, player, 'Steel', 1 * modifier)


                    if isTileType(Data[guild]['Image'], xcord, ycord, 'MOONDUST') and \
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                                'type'] == 'Perpetual':                    addItem(guild, player, 'Cheese', 3 * modifier)

                    if isTileType(Data[guild]['Image'], xcord, ycord, 'MOONDUST') and \
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                                'type'] == 'Non Perpetual':                    addItem(guild, player, 'Silica',
                                                                                       1 * modifier)
                    if isTileType(Data[guild]['Image'], xcord, ycord, 'STARSEA') and \
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                                'type'] == 'Perpetual':                    addItem(guild, player, 'Starfish', 3 * modifier)

                    if isTileType(Data[guild]['Image'], xcord, ycord, 'STARSEA') and \
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                                'type'] == 'Non Perpetual':                    addItem(guild, player, 'Aether',
                                                                                       1 * modifier)



                    if isTileType(Data[guild]['Image'], xcord, ycord, 'WATER') and \
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                                'type'] == 'Non Perpetual':                    addItem(guild, player, 'Oil', 1 * modifier)

                    Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['age'] += 1
                    if Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                        'type'] == 'Non Perpetual' and \
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['age'] >= 5:
                        del Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']

                # IF UNIT
                if 'Unit' in markerTier and 'Unit' in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex] \
                        and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'].get('DisabledAndPermanent') is not True:
                    name = Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']['Name']
                    unit = dict(Data[guild]['Units'][name])

                    double = 'Boost' in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']
                    modifier = (1 - cursed * 0.5) * (double + 1)
                    if double: del \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']['Boost']

                    if Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'].get(
                                    'MobileMoveCount') is not None:
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']['MobileMoveCount'] = 0


                    canAfford = True
                    for cost in unit['DailyCosts']:
                        if ' ' in cost:
                            amount, item = cost.split(' ')
                            canAfford = canAfford and addItem(guild, player, item, -float(amount), testOnly=True)

                    if not canAfford:
                        addMsgQueue(channels[guild]['actions'],
                                    '@' + player + ' You Have Insufficient Funds For Your ' + name + '.\n Unit is disabled, will retry in 1 Day.')
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']['DisabledAndPermanent'] = False
                    else:
                        if 'DisabledAndPermanent' in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'] and \
                                not Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'][
                                    'DisabledAndPermanent']:
                            del Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']['DisabledAndPermanent']

                        if name == 'town':
                            gift = Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'].get('TownItem')
                            if gift == None:
                                gift = random.choice(rawMaterialsList)
                                Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'][
                                    'TownItem'] = gift
                            addItem(guild, player, gift, float(2) * modifier)

                        if name == 'village':
                            gift = Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'].get(
                                'VillageItem')
                            if gift == None:
                                gift = random.choice(rawMaterialsList)
                                Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'][
                                    'VillageItem'] = gift
                            addItem(guild, player, gift, float(1) * modifier)

                        if name == 'digsite':
                            if random.randint(0,100) < 5:
                                Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'][
                                    'Artifact'] = True

                        if name == 'sailboat' and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]\
                            ['Unit'].get('MobileMoveCount') in [0,None]:
                            addItem(guild, player, 'Oil', 2.0)
                        elif name == 'sailboat' :
                           Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']['MobileMoveCount'] = 0

                        for cost in unit['DailyCosts']:
                            if ' ' in cost:
                                amount, item = cost.split(' ')
                                addItem(guild, player, item, -float(amount) )

                        for cost in unit['DailyReturn']:
                            if ' ' in cost:
                                amount, item = cost.split(' ')
                                amount = int(amount)
                                for technode in TECH_TREE:
                                    if TECH_TREE[technode]['AddResource'] == name:
                                        amount += Data[guild]['Players'][player]['TechTree'][technode]

                                addItem(guild, player, item, float(amount) * modifier)

    for item in Data[guild]['Fed']['Rates'].keys():
        vel = Data[guild]['Fed']['Velocity'][item]+100
        if vel != 0:
            Data[guild]['Fed']['Rates'][item] = 100.0/vel * Data[guild]['Fed']['Rates'][item]

    dir = random.randint(0,3)
    stepsize = random.randint(2,4)
    atlantean = 'ATLANTEAN' in Data[guild]['Vinny']
    if atlantean: Data[guild]['Vinny']['ATLANTEAN'] -= 1
    if atlantean and Data[guild]['Vinny']['ATLANTEAN'] <=0 : del Data[guild]['Vinny']['ATLANTEAN']

    acts = [(-1,0),(1,0),(0,1),(0,-1)]
    event = random.randint(0, 100)

    for i in range(4):
        dir = (dir + 1) % 4
        action = acts[dir]
        ncoords = [
            Data[guild]['Vinny']['Position'][0] + action[0]*stepsize,
            Data[guild]['Vinny']['Position'][1] + action[1]*stepsize,
        ]
        if ncoords[0] < 0 or ncoords[1] < 0 or ncoords[0] >= 75 or ncoords[1] >= 75: continue
        elif ncoords in Data[guild]['Vinny']['History'] and random.randint(0,1) and i != 3:
            print("Skipping Past Place")
            continue
        else:
            Data[guild]['Vinny']['Position'] = ncoords
            addMsgQueue(channels[guild]['actions'], 'Vinny has moved to '+ labels[ncoords[0]]+str( ncoords[1]+1) + ' Rolled: ' +str(event) )
            break

    vx, vy = Data[guild]['Vinny']['Position']
    Data[guild]['Vinny']['History'].append([vx,vy])
    if atlantean and isTileType(Data[guild]['Image'], vx, vy, 'WATER'):
        for i in range(4):
            dir = (dir + 1) % 4
            stepsize = random.randint(2, 4)
            action = acts[dir]
            ncoords = [
                Data[guild]['Vinny']['Position'][0] + action[0]*stepsize,
                Data[guild]['Vinny']['Position'][1] + action[1]*stepsize,
            ]
            if ncoords[0] < 0 or ncoords[1] < 0 or ncoords[0] >= 75 or ncoords[1] >= 75:
                continue
            elif ncoords in Data[guild]['Vinny']['History'] and random.randint(0, 1) and i != 3:
                print("Skipping Past Place")
                continue
            else:
                Data[guild]['Vinny']['Position'] = ncoords
                addMsgQueue(channels[guild]['actions'],
                            'Vinny has moved to ' + labels[ncoords[0]] + str(ncoords[1] + 1) + ' Rolled: ' +str(event) )
                break


    vx, vy = Data[guild]['Vinny']['Position'] # Process Vinny Events Here
    Data[guild]['Vinny']['History'].append([vx,vy])
    if event < 10 and not isTileType(Data[guild]['Image'], vx, vy, 'MEAT'):
        for i in range(6):
            event = (event + 1) % 6
            if event == 1:
                addMsgQueue(channels[guild]['actions'], "Vinny has triggered an event: ARCHAEOLOGICAL DISCOVERY")
                isOnPlayer = False
                isOnUnit = False
                for player in Data[guild]['Players'].keys():
                    if [vx, vy] in Data[guild]['Players'][player]['Markers']['Location']:
                        print(1, player)
                        index = Data[guild]['Players'][player]['Markers']['Location'].index([vx, vy])

                        if 'Unit' not in Data[guild]['Players'][player]['Markers']['Properties'][index]:
                            Data[guild]['Players'][player]['Markers']['Properties'][index][
                                'Unit']['Name'] = {
                                    'Name': 'digsite',
                                    'Artifact': False
                            }
                            isOnPlayer = True
                        else: isOnUnit = True
                if not isOnPlayer and not isOnUnit:
                    Data[guild]['Players'][botName]['Markers']['Shape'].append("")
                    Data[guild]['Players'][botName]['Markers']['Location'].append([vx, vy])
                    Data[guild]['Players'][botName]['Markers']['Properties'].append({
                        'Unit': {
                            'Name': 'digsite',
                            'Artifact': False
                        }
                    })

            elif event == 2 and isTileType(Data[guild]['Image'], vx, vy, 'LAND'):
                addMsgQueue(channels[guild]['actions'], "Vinny has triggered an event: FIRST CONTACT")
                isOnPlayer = False
                isOnUnit = False
                for player in Data[guild]['Players'].keys():
                    if [vx, vy] in Data[guild]['Players'][player]['Markers']['Location']:
                        print(1, player)
                        index = Data[guild]['Players'][player]['Markers']['Location'].index([vx, vy])

                        if 'Unit' not in Data[guild]['Players'][player]['Markers']['Properties'][index]:
                            Data[guild]['Players'][player]['Markers']['Properties'][index][
                                'Unit'] ={'Name': 'village',
                                          'VillageItem': random.choice(rawMaterialsList)}
                            isOnPlayer = True
                        else: isOnUnit = True
                if not isOnPlayer and not isOnUnit:
                    Data[guild]['Players'][botName]['Markers']['Shape'].append("")
                    Data[guild]['Players'][botName]['Markers']['Location'].append([vx, vy])
                    Data[guild]['Players'][botName]['Markers']['Properties'].append({
                        'Unit': {
                            'Name': 'village',
                            'VillageItem': random.choice(rawMaterialsList)
                        }
                    })

            elif event == 3 and isTileType(Data[guild]['Image'], vx, vy, 'WATER'):
                addMsgQueue(channels[guild]['actions'], "Vinny has triggered an event: ATLANTEAN ENVOY")
                Data[guild]['Vinny']['ATLANTEAN'] = 5

            elif event == 4 and isTileType(Data[guild]['Image'], vx, vy, 'WATER'):
                Data[guild]['Image'][vx, vy] = TILES['MEAT']
                addMsgQueue(channels[guild]['actions'], "Vinny has triggered an event: RELEASE THE KRAKEN")

            elif event == 5: # LEGENDARY EXPLORER
                addMsgQueue(channels[guild]['actions'], "Vinny has triggered an event: LEGENDARY EXPLORER")
                radius = [
                    (0, 0),

                    (0,1),(0,-1),(1,0),(-1,0),
                    (-1, -1),(1,-1),(-1,1),(1,1),

                    (0, 2),(2,0),(0,-2),(-2,0),
                    (1, 2),(2,1),(1,-2),(-2,1),
                    (-1, 2), (2, -1), (-1, -2), (-2, -1),
                    (-2, 2), (2, -2), (-2, -2), (2, 2),

                    (0, 3),(3,0),(0,-3),(-3,0),
                ]
                addMsgQueue(channels[guild]['actions'], "Nearby Production Has Been Doubled")
                for player in Data[guild]['Players'].keys():
                    for offsetx, offsety in radius:
                        coor = [vx + offsetx, vy + offsety]
                        if coor in Data[guild]['Players'][player]['Markers']['Location']:
                            index = Data[guild]['Players'][player]['Markers']['Location'].index(coor)
                            if 'Unit' in Data[guild]['Players'][player]['Markers']['Properties'][index]:
                                Data[guild]['Players'][player]['Markers']['Properties'][index]['Unit']['Boost'] = True
                            if 'Harvest' in Data[guild]['Players'][player]['Markers']['Properties'][index]:
                                Data[guild]['Players'][player]['Markers']['Properties'][index]['Harvest']['Boost'] = True

            elif event == 0: #explosive Adventure
                addMsgQueue(channels[guild]['actions'], "Vinny has triggered an event: EXPLOSIVE ADVENTURE")
                dir = random.randint(0, 3)
                action = acts[dir]
                ncoords = [
                    Data[guild]['Vinny']['Position'][0] + 12*action[0],
                    Data[guild]['Vinny']['Position'][1] + 12*action[1],
                ]
                if ncoords[0] < 0: ncoords[0] = 0
                if ncoords[1] < 0: ncoords[1] = 0
                if ncoords[0] > 74: ncoords[0] = 74
                if ncoords[1] > 74: ncoords[1] = 74

                Data[guild]['Vinny']['Position'] = ncoords
                addMsgQueue(channels[guild]['actions'], "Vinny is sent flying to "+labels[ncoords[0]]+str( ncoords[1]+1))

            else: continue
            break
    print("OnDayChange: ", time.time() - start)


"""
Is tile Adjacent
"""
def isAdjacent(guild, player, coord, claimAdjacencyOnly = True):
    global Data
    xcord, ycord = coord
    loc = []
    for index in range(len(Data[guild]['Players'][player]['Markers']['Location'])):
        if Data[guild]['Players'][player]['Markers']['Shape'][index] in ['Claim','Capital'] or not claimAdjacencyOnly:
            loc.append(Data[guild]['Players'][player]['Markers']['Location'][index])

    isadj = [xcord + 1, ycord + 1] in loc or \
            [xcord + 1, ycord    ] in loc or \
            [xcord + 1, ycord - 1] in loc or \
            [xcord    , ycord + 1] in loc or \
            [xcord    , ycord - 1] in loc or \
            [xcord - 1, ycord + 1] in loc or \
            [xcord - 1, ycord    ] in loc or \
            [xcord - 1, ycord - 1] in loc
    return  isadj


"""
Called On Turn Change
"""
async def onTurnChange(server):
    global Data

    start = time.time()
    guild = server.id
    Data[guild]['Fed']['Term'] += 1
    if Data[guild]['Fed']['Term'] >= 5:
        Data[guild]['Fed']['Term'] = 0
        FedMembers = getRoleList(server,'Fed Member')
        Inactives = getRoleList(server, 'Inactive')
        role = getRole(server,name='Fed Member')
        for member in FedMembers.keys():
            Data[guild]['Fed']['MemberHistory'][member] +=1
            await FedMembers[member].remove_roles(role)

        newMembers = []
        newMembersNames = []
        for i in [1,2,3]:
            minList = []
            minVal = 10000
            for member in Data[guild]['Fed']['MemberHistory'].keys():
                id = server.get_member_named(member)
                if member in Inactives or member in newMembers: continue
                if Data[guild]['Fed']['MemberHistory'][member] < minVal:
                    minVal = Data[guild]['Fed']['MemberHistory'][member]
                    minList = [member]
                elif Data[guild]['Fed']['MemberHistory'][member] == minVal:
                    minList.append(member)
            print('MinList',minList)
            newMember = random.choice(minList)
            print(newMember)
            newMembers.append(newMember)
            newMembersNames.append(server.get_member_named(newMember).mention)
            await server.get_member_named(newMember).add_roles(role)
        msg = "The Fed Term has Ended. New Fed members are " + ' '.join(newMembersNames)
        addMsgQueue(channels[guild]['actions'],msg)
    print("OnTurnChange: ", time.time() - start)


"""
Reset The Claim Timers
"""
def resetTimers(server, channel=None, playerid=None, mode=0):
    start = time.time()
    if channel is None: channel = channels[server.id][logChannel]
    guild = server.id

    if playerid is None:
        for player in Data[guild]['Players']:
            Data[guild]['Players'][player]['Claimed Today'] = mode

        addMsgQueue(channel, "Resetting Claim Timer for Everyone")

    else:
        player = getPlayer(server, playerid, channel)
        if player is not None:
            Data[guild]['Players'][player]['Claimed Today'] = 0
            Data[guild]['Players'][player]['BF Claimed Today'] = 0
            addMsgQueue(channel, "Resetting Claim Timer for " + player)
    print("resetTimers: ", time.time() - start)


"""
Extracts Coordinates From String. 
"""
def extractCoords(coords, channel):
    if len(coords) > 4 or len(coords) < 3:
        addMsgQueue(channel, "Incorrect Coordinate Formatting: "+coords)
        return None
    else:
        xcord = None
        xcordAlpha = None
        ycord = None
        if coords[:2].upper() in labels:
            xcordAlpha = coords[0:2].upper()
            xcord = int(labels.index(xcordAlpha))
            ycord = int(coords[2:]) - 1
        elif coords[-2:].upper() in labels:
            xcordAlpha = coords[-2:].upper()
            xcord = int(labels.index(xcordAlpha))
            ycord = int(coords[:-2]) - 1
        else:
            addMsgQueue(channel, "Incorrect Coordinate Formatting: "+coords)
            return None

        if xcord is None and ycord is None:
            return None
        elif ycord >= n or ycord < 0 or xcord >= n+30 or xcord < 0 or xcord == n:
            addMsgQueue(channel, coords +" is outside the map.")
            return None

        return xcord, xcordAlpha, ycord


"""
Send Map Data File
"""
async def sendMapData(guild, channel):
    await channel.send('Save File Backup After Day Change:', file=discord.File(open('DiscordBot_Data.pickle', 'br')))


"""
Is The Tile Of Type as x,y in image
"""
def isTileType(image, x, y, type):
    return np.all(image[x, y] == TILES[type.upper()])


'''
Add item of count N to player's inventory inv.
'''
def addItem(guild, player, item, count, testOnly=False):
    count = float(count)
    inv = Data[guild]['Players'][player]['Inventory']
    if inv.get(item) is None:
        Data[guild]['Players'][player]['Inventory'][item] = 0

    # If Not Allowed To Be Negative
    if inv[item] + count < 0 and item in ['BF', 'Corn', 'C-Fish', 'Food', 'Steel', 'Oil', 'Wood', 'Technology', 'Energy']:
        return False
    elif testOnly:
        return True
    else:
        Data[guild]['Players'][player]['Inventory'][item] += count
    if inv[item] == 0 and item != 'BF':
        del Data[guild]['Players'][player]['Inventory'][item]
    return True


"""
Update Messages In Annoncements
"""
async def updateInAnnouncements(server, reload=True, postToSpam = False):
    global Data, oldData
    guild = server.id


    targetChannel = "changelog-live"
    if targetChannel not in channels[guild]:
        targetChannel = 'bot-lounge'

    # Update Player Stuffs
    if not isinstance(Data[guild]['Announcements']['Items'], (list,)):
        Data[guild]['Announcements']['Items'] = []
    sortedPlayers = list(Data[guild]['Players'].keys())

    i = 0
    for player in playerOrder:
        if player not in sortedPlayers: continue
        msg = player + ' : ' + Data[guild]['Players'][player]['Color'].upper() + '\n'
        msg += '-Claims Left Today: ' + str(1 + (hasUnit(guild, player, 'explorerguild') * 5) \
                                            - Data[guild]['Players'][player]['Claimed Today'])
        msg += '\n-Next BF Claims Cost: ' + str(2 + Data[guild]['Players'][player]['BF Claimed Today'])
        msg += '\n-Times On Fed: '+str(Data[guild]['Fed']['MemberHistory'][player])
        msg += '\n-Tiles:'
        totalCornHarvests = 0
        totalSteelHarvests = 0

        totalStarfishHarvests = 0
        totalCheeseHarvests = 0
        totalAetherHarvests = 0
        totalSilicaHarvests = 0

        Total = 0
        itemDelta = {
            'BF': {'-': 0.0, '+': 0.0},
        }
        cursed = not Data[guild]['Players'][player]['Inventory'].get('Curse') in [0, None]

        for tileIndex in range(len(Data[guild]['Players'][player]['Markers']['Shape'])):
            x, y = Data[guild]['Players'][player]['Markers']['Location'][tileIndex]
            # if isTileType(Data[guild]['Image'],x , y, 'LAND'): totalLand+=1
            # if isTileType(Data[guild]['Image'],x , y, 'WATER'): totalWater+=1
            Total += 1
            for prop in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].keys():
                xcord, ycord = Data[guild]['Players'][player]['Markers']['Location'][tileIndex]
                if prop == 'Unit' and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'].get(
                            'DisabledAndPermanent') is None:
                    unit = Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']['Name']
                    double = 'Boost' in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']

                    modifier = (1 - cursed * 0.5) * (double + 1)
                    if unit == 'town':
                        itm = Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'].get('TownItem')
                        if itm == None:
                            itm = random.choice(rawMaterialsList)
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']['TownItem'] = itm
                        if itemDelta.get(itm) is None:
                            itemDelta[itm] = {'-': 0.0, '+': 0.0}
                        itemDelta[itm]['+'] += float(2) * modifier

                    if unit == 'village':
                        itm = Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit'].get('VillageItem')
                        if itm == None:
                            itm = random.choice(rawMaterialsList)
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']['VillageItem'] = itm
                        if itemDelta.get(itm) is None:
                            itemDelta[itm] = {'-': 0.0, '+': 0.0}
                        itemDelta[itm]['+'] += float(1) * modifier

                    if unit == 'sailboat' and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex] \
                            ['Unit'].get('MobileMoveCount') in [0, None]:
                        itm  = 'Oil'
                        if itemDelta.get(itm) is None:
                            itemDelta[itm] = {'-': 0.0, '+': 0.0}
                        itemDelta[itm]['+'] += float(2) * modifier


                    for cst in Data[guild]['Units'][unit]['DailyCosts']:
                        a, itm = cst.split(' ')
                        if itemDelta.get(itm) is None:
                            itemDelta[itm] = {'-': 0.0, '+': 0.0}
                        itemDelta[itm]['-'] += float(a)
                    for cst in Data[guild]['Units'][unit]['DailyReturn']:
                        a, itm = cst.split(' ')
                        a = int(a)

                        for technode in TECH_TREE:
                            if TECH_TREE[technode]['AddResource'] == unit:
                                a += Data[guild]['Players'][player]['TechTree'][technode]

                        if itemDelta.get(itm) is None:
                            itemDelta[itm] = {'-': 0.0, '+': 0.0}
                        itemDelta[itm]['+'] += float(a) * modifier

                elif prop == 'Harvest' and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                    'type'] == 'Perpetual' and 'Unit' not in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex] \
                        and isTileType(Data[guild]['Image'], xcord, ycord, 'LAND'):
                    totalCornHarvests += 1
                elif prop == 'Harvest' and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                    'type'] == 'Non Perpetual' and 'Unit' not in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]\
                        and isTileType(Data[guild]['Image'], xcord, ycord, 'LAND'):
                    totalSteelHarvests += 1

                elif prop == 'Harvest' and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                            'type'] == 'Perpetual' and 'Unit' not in \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex] \
                        and isTileType(Data[guild]['Image'], xcord, ycord, 'MOONDUST'):
                    totalCheeseHarvests += 1
                elif prop == 'Harvest' and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                            'type'] == 'Non Perpetual' and 'Unit' not in \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]\
                        and isTileType(Data[guild]['Image'], xcord, ycord, 'MOONDUST'):
                    totalSilicaHarvests += 1

                elif prop == 'Harvest' and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                            'type'] == 'Perpetual' and 'Unit' not in \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]\
                        and isTileType(Data[guild]['Image'], xcord, ycord, 'STARSEA'):
                    totalStarfishHarvests += 1
                elif prop == 'Harvest' and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                            'type'] == 'Non Perpetual' and 'Unit' not in \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]\
                        and isTileType(Data[guild]['Image'], xcord, ycord, 'STARSEA'):
                    totalAetherHarvests += 1



        msg += "\n  Total Tiles:" + str(Total) #+ \
               #'\n  Renewable Harvests:' + str(totalRenewableHarvests) + \
               #'\n  Non-Renewable Harvests:' + str(totalNonRenewableHarvests)

        msg += '\n-Tech Tree Levels:'

        for technode in TECH_TREE.keys():
            level =  Data[guild]['Players'][player]['TechTree'].get(technode)
            if level not in [None, 0]:
                msg += "\n  " + technode.title() + ' : ' + str(level)

        msg += "\n\nInventory:       |   Change "

        itemListtmp = list(itemList)
        playerItemSet = set(Data[guild]['Players'][player]['Inventory'].keys())
        playerItemSet = list((set(itemListtmp) | playerItemSet) - set(itemListtmp))
        playerItemSet.sort()
        itemListtmp = itemListtmp + playerItemSet
        for item in itemListtmp:
            amount = 0.0
            deltaplus = 0.0
            deltaloss = 0.0
            sign = '+'
            if item == 'Corn':
                deltaplus += totalCornHarvests * 3.0
            if item == 'Steel':
                deltaplus += totalSteelHarvests
            if item == 'Cheese':
                deltaplus += totalCheeseHarvests * 3.0
            if item == 'Silica':
                deltaplus += totalSilicaHarvests
            if item == 'Starfish':
                deltaplus += totalStarfishHarvests * 3.0
            if item == 'Aether':
                deltaplus += totalAetherHarvests
            if item in Data[guild]['Players'][player]['Inventory'].keys():
                amount = float(Data[guild]['Players'][player]['Inventory'][item])
            if item in itemDelta.keys():
                deltaplus += float(itemDelta[item]['+'])
                deltaloss += float(itemDelta[item]['-'])
            delta = deltaplus - deltaloss
            if delta < 0:  sign = ""
            if delta == 0 and amount == 0: continue

            #deltaloss = int(deltaloss)
            #deltaplus = int(deltaplus)
            #delta     = int(delta)

            tmpmsg = "\n " + item
            tmpmsg += (17 - len(tmpmsg) - len(str(int(amount)))) * ' ' + str(int(amount))
            tmpmsg += (18 - len(tmpmsg)) * ' ' + '|+'+str(int(deltaplus))
            tmpmsg += (23 - len(tmpmsg)) * ' ' + ' -' + str(int(deltaloss))
            tmpmsg += (28 - len(tmpmsg)) * ' ' + '= ' +sign + str(int(delta))
            msg    += tmpmsg
        if postToSpam: log(guild,"```"+msg+"```")

        if i >= len(Data[guild]['Announcements']['Items']):
            post = await channels[server.id][targetChannel].send('```' + msg + '```')
            Data[guild]['Announcements']['Items'].append(post.id)
        else:
            try:
                post = await channels[server.id][targetChannel].fetch_message(Data[guild]['Announcements']['Items'][i])
            except:
                post = None

            if post is None:
                post = await channels[server.id][targetChannel].send('```' + msg + '```')
                Data[guild]['Announcements']['Items'][i] = post.id
            else:
                await post.edit(content='```' + msg + '```')
        i += 1

    for n in range(i, len(Data[guild]['Announcements']['Items'])):
        try:
            post = await channels[server.id][targetChannel].fetch_message(Data[guild]['Announcements']['Items'][i])
            await post.delete()
            del Data[guild]['Announcements']['Items'][i]
        except:
            del Data[guild]['Announcements']['Items'][i]


    #Moon and World Images
    if reload:
        task1 = asyncio.ensure_future(
            plotMap(channels[guild][logChannel], False))

        task2 = asyncio.ensure_future(
            plotMoon(channels[guild][logChannel], False))
        await task1
        await task2
    # Update Map
    junkmsg = await channels[server.id][logChannel].send(
        'World Map:', file=discord.File(open('tmpgrid.png', 'br')))
    url = "World Map: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\n " + junkmsg.attachments[0].url
    if Data[guild]['Announcements'].get('Map') is None:
        Data[guild]['Announcements']['Map'] = await channels[server.id][targetChannel].send(url)
        Data[guild]['Announcements']['Map'] = Data[guild]['Announcements']['Map'].id
    else:
        msg = None
        try:
            msg = await channels[server.id][targetChannel].fetch_message(Data[guild]['Announcements']['Map'])
        except:
            msg = None
        if msg is None:
            Data[guild]['Announcements']['Map'] = await channels[server.id][targetChannel].send(url)
            Data[guild]['Announcements']['Map'] = Data[guild]['Announcements']['Map'].id
        else:
            await msg.edit(content=url)


    # Update Moon
    junkmsg = await channels[server.id][logChannel].send(
        'Moon Map:', file=discord.File(open('tmpMoon.png', 'br')))
    url = "Moon Map: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\n " + junkmsg.attachments[0].url

    if Data[guild]['Announcements'].get('Moon') is None:
        Data[guild]['Announcements']['Moon'] = await channels[server.id][targetChannel].send(url)
        Data[guild]['Announcements']['Moon'] = Data[guild]['Announcements']['Moon'].id
    else:
        msg = None
        try:
            msg = await channels[server.id][targetChannel].fetch_message(Data[guild]['Announcements']['Moon'])
        except:
            msg = None
        if msg is None:
            Data[guild]['Announcements']['Moon'] = await channels[server.id][targetChannel].send(url)
            Data[guild]['Announcements']['Moon'] = Data[guild]['Announcements']['Moon'].id
        else:
            await msg.edit(content=url)




    # Update Fed Board
    msg =    "FEDERAL RATES\n(Turns Left in Term: " + str(5-Data[guild]['Fed']['Term'])+')'
    msg += "\n   ITEM    :  RATE  : VELOCITY "
    msg += "\n--------------------------------"
    for item in dict(Data[guild]['Fed']['Rates']).keys():
        if item not in FedMaterialList:
            del Data[guild]['Fed']['Rates'][item]
    for item in FedMaterialList:
        if Data[guild]['Fed']['Rates'].get(item) is None:
            Data[guild]['Fed']['Rates'][item] = 100
        if Data[guild]['Fed']['Velocity'].get(item) is None:
            Data[guild]['Fed']['Velocity'][item] = 0
        rate = Data[guild]['Fed']['Rates'][item]
        vel =  Data[guild]['Fed']['Velocity'][item]

        tmpmsg = "\n" + item.upper()
        tmpmsg += (12 - len(tmpmsg)) * ' ' + ': ' + str(round(100.0/rate,3))+'%'
        tmpmsg += (21 - len(tmpmsg)) * ' ' + ': ' + str(int(vel))+'% '
        tmpmsg += (28 - len(tmpmsg)) * ' ' + '/Day'
        msg += tmpmsg

    try:
        post = await channels[server.id][targetChannel].fetch_message(Data[guild]['Announcements']['Fed'])
    except:
        post = None
    if post == None:
        post = await channels[server.id][targetChannel].send('```' + msg + '```')
        Data[guild]['Announcements']['Fed'] = post.id
    else:
        await post.edit(content='```' + msg + '```')

    print('Update Saved')


"""
Determines If PLayer Has A Unit
"""
def hasUnit(guildid, player, unit):
    unitCount = 0
    for tile in range(len(Data[guildid]['Players'][player]['Markers']['Location'])):
        props = Data[guildid]['Players'][player]['Markers']['Properties'][tile]
        if 'Unit' not in props:
            continue
        elif unit == props['Unit']['Name']:
            unitCount += 1
    return unitCount


"""
get Player
"""
def getPlayer(server, playerid, channel=None):
    guild = server.id
    if channel == None: channel = channels[guild][logChannel]
    if len(playerid) == 0:
        return None
    else:
        player = server.get_member(int(re.search(r'\d+', playerid).group()))
        if player is not None:
            playerName = player.name + "#" + str(player.discriminator)
            if playerName in Data[guild]['Players']:
                return playerName
            else:
                addMsgQueue(channel, 'Player ' + playerName + ' cannot be found in the map.')
        else:
            addMsgQueue(channel,
                        'Player with id:' + playerid + ' cannot be found in the server.')
        return None


"""
get role
"""
def getRole(server,name):
    players = {}
    role = None
    for r in server.roles:
        if r.name == name:
            role = r
            break
    return role



"""
get all memebers with role
"""
def getRoleList(server,name):
    players = {}
    role = getRole(server,name)

    if role is None:
        print("Role Not Found")
        return
    for member in role.members:
        if role in member.roles:
            players[ member.name + '#' + member.discriminator ] = member
    return players


"""
Setup Log Parameters and Channel List And Whatever You Need to Check on a Bot Reset.
Handles Change In Server Structure and the like. Probably Can Leave Alone.
"""
async def setup(inData, chans, logchan, server):
    loadData(inData)
    print('Starting Up')
    # Do Stuff Here

    global channels, logChannel, Data
    global np, plt, ticker, mcd
    import numpy as np
    import matplotlib

    matplotlib.use('Agg')
    #matplotlib.rc('font', family='Arial')

    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import matplotlib._color_data as mcd

    channels[server.id] = chans
    print('Channels',channels[server.id].keys())
    logChannel = logchan
    guild = server.id

    # Do Stuff Here
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    if Data.get(guild) is None: Data[guild] = {}
    if Data[guild].get('Pause') is None:
        Data[guild]['Pause'] = False
    if Data[guild].get('Announcements') is None: Data[guild]['Announcements'] = {
        'Map': None,
        'Items': None,
        'Fed':None
    }
    Data[guild]['ImgLock'] = False
    Data[guild]['ImgLockTime'] = 0
    if Data[guild]['Announcements'].get('Fed') is None: Data[guild]['Announcements']['Fed']=None
    if Data[guild].get('Units') is None: Data[guild]['Units'] = {}
    if Data[guild].get('Players') is None: Data[guild]['Players'] = {}
    if Data[guild].get('Date') is None: Data[guild]['Date'] = datetime.datetime.now().strftime("%Y-%m-%d")
    if Data[guild].get('Log'): del Data[guild]['Log']

    if Data[guild].get('Image') is None:
        try:
            from PIL import Image
            import numpy as np

            img = Image.open('map.png')
            img.load()

            data = np.zeros((75+31, 75, 4), dtype=np.uint8)
            dataIMG = np.asarray(img).copy()
            for r in range(dataIMG.shape[0]):
                for c in range(dataIMG.shape[1]):
                    if dataIMG[r, c, 2] > 150:
                        data[r, c] = [49, 108, 237, 255]
                    else:
                        data[r, c] = [45, 84, 55, 255]
        except ImportError:
            log(guild, "Error Initializing the Map: PIL and/or Numpy Not Available")

        try:
            from PIL import Image
            import numpy as np

            img = Image.open('moon.png')
            img.load()
            dataIMG = np.asarray(img).copy()
            for r in range(dataIMG.shape[0]):
                for c in range(dataIMG.shape[1]):
                    if dataIMG[c, r, 2] > 100:
                        data[r + n + 1, c] = TILES['MOONDUST']
                    else:
                        data[r + n + 1, c] =  TILES['STARSEA']
            Data[guild]['Image'] = data
        except ImportError:
            log(guild, "Error Initializing the Map: PIL and/or Numpy Not Available")

    if Data[guild].get('Fed') is None: Data[guild]['Fed'] = {'Rates':{}, 'Velocity':{}, 'MemberHistory':{},'Term':0}
    if Data[guild]['Players'].get(botName) is None:
        Data[guild]['Players'][botName] = {
            'Markers': {
                'Location': [],
                'Shape': [],
                'Properties': []
            },
            'Color': 'Gold',
            'Inventory': {}
        }
    if Data[guild].get('Vinny') is None:
        Data[guild]['Vinny'] = {
            'Position': [0,0],
        }

    if Data[guild]['Vinny'].get('History') in [None, set()]:
        Data[guild]['Vinny']['History'] = list()

    for player in Data[guild]['Players'].keys():
        #if Data[guild]['Players'][player].get('Object') is None:
        #    Data[guild]['Players'][player]['Object'] = server.get_member_named(player)
        if Data[guild]['Players'][player].get('Inventory') is None:
            Data[guild]['Players'][player]['Inventory'] = {'BF': 0, }

        if Data[guild]['Players'][player].get('BF Claimed Today') is None:
            Data[guild]['Players'][player]['BF Claimed Today'] = 0

        if Data[guild]['Players'][player].get('TechTree') is None:
            Data[guild]['Players'][player]['TechTree'] = {}
        for technode in TECH_TREE:
            if technode not in Data[guild]['Players'][player]['TechTree']:
                val = 0
                if Data[guild]['Players'][player]['TechTree'].get(technode+' upgrade') is not None:
                    val  = int(Data[guild]['Players'][player]['TechTree'].get(technode+' upgrade'))
                    del Data[guild]['Players'][player]['TechTree'][technode+ ' upgrade']
                Data[guild]['Players'][player]['TechTree'][technode] = val


        if player not in Data[guild]['Fed']['MemberHistory']:
            if player not in ['A Beep Booper#4870',botName]:
                Data[guild]['Fed']['MemberHistory'][player] = 0
        if Data[guild]['Players'][player]['Markers'].get('Properties') is None:
            Data[guild]['Players'][player]['Markers']['Properties'] = []
            for tile in Data[guild]['Players'][player]['Markers']['Shape']:
                Data[guild]['Players'][player]['Markers']['Properties'].append({})
        else:
            for tile in range(len(Data[guild]['Players'][player]['Markers']['Shape'])):
                props = Data[guild]['Players'][player]['Markers']['Properties'][tile]

                if 'Unit' in props:
                    if isinstance(props['Unit'], str):
                        props['Unit'] = {'Name':props['Unit'].lower()}
                    if 'TownItem' in props:
                        props['Unit']['TownItem'] = props['TownItem']
                        del props['TownItem']
                    if 'VillageItem' in props:
                        props['Unit']['VillageItem'] = props['VillageItem']
                        del props['VillageItem']
                    if 'MoveCount' in props:
                        props['Unit']['MoveCount'] = props['MoveCount']
                        del props['MoveCount']
                    if 'DisabledAndPermanent' in props:
                        props['Unit']['DisabledAndPermanent'] = props['DisabledAndPermanent']
                        del props['DisabledAndPermanent']

                Data[guild]['Players'][player]['Markers']['Properties'][tile] = props



    oldUnits = dict(Data[guild]['Units'])
    Data[guild]['Units'] = {}
    for name in oldUnits.keys():
        data = oldUnits[name]
        requirements = dict(UNIT_BASE)
        for key in data.keys():
            if requirements.get(key) is not None:
                requirements[key] = data[key]
        Data[guild]['Units'][name.lower()] = requirements

    await updateInAnnouncements(server)
    await sendMessages()
    return saveData()


"""
Plot The Map Using Matplotlib
"""
async def plotMap(channel, postReply=True):
    global Data, plt
    guild = channel.guild.id
    async with channel.typing():
        if 1:#try:
            if channel is None: channel = channels[guild][logChannel]
            # fig, ax = plt.subplots()
            fig = plt.figure(figsize=(5.0, 5.0))
            plt.subplots_adjust(left=0.04, bottom=0.04, right=0.96, top=0.96)
            ax = fig.add_subplot(111)

            axisn = np.arange(0, n, 1)
            plt.xticks(axisn + 0.5)
            plt.yticks(axisn + 0.5)

            ax.scatter( Data[guild]['Vinny']['Position'][0] ,
                        Data[guild]['Vinny']['Position'][1] ,
                        c='Gold', s=12.0, linewidths=0.075,
                        edgecolors='black',
                        marker='$😊$')

            for player in Data[guild]['Players'].keys():
                player = Data[guild]['Players'][player]
                color = player['Color']

                if len(player['Markers']['Location']) == 0: continue
                x, y = np.asarray(player['Markers']['Location']).T
                obj = np.asarray(player['Markers']['Shape'])
                obj[obj == 'Claim'] = 'None'
                obj[obj == 'Capital'] = '*'
                for unit in Data[guild]['Units'].keys():
                    obj[obj == unit] = Data[guild]['Units'][unit]['Marker']

                for i in range(obj.shape[0]):
                    outline = 'black'
                    if color == 'black': outline = 'white'

                    if obj[i] != "" and player != botName:
                        ax.scatter(x[i], y[i], c="none", edgecolors=color,
                                   linewidths=0.3, s=11, marker='s', alpha=0.7)

                    alpha = 1.0
                    if 'Unit' in player['Markers']['Properties'][i] and 'DisabledAndPermanent' in player['Markers']['Properties'][i]['Unit']:
                        alpha = 0.25
                    if player['Markers']['Properties'][i].get('Unit') is not None:
                        unit = player['Markers']['Properties'][i]['Unit']['Name']
                        obj[i] = Data[guild]['Units'][unit]['Marker']
                        if obj[i][0] == '"' and obj[i][-1] == '"':
                            obj[i] = '$' + obj[i][1:-1] + '$'
                        if player['Markers']['Properties'][i]['Unit'].get('Boost'):
                            outline = 'Gold'
                    elif player['Markers']['Properties'][i].get('Harvest') is not None:
                        if player['Markers']['Properties'][i]['Harvest']['type'] == 'Perpetual':
                            ax.scatter(x[i], y[i], c="none", edgecolors=color,
                                       linewidths=0.2, s=14, marker='.', alpha=0.7)

                        if player['Markers']['Properties'][i]['Harvest']['type'] == 'Non Perpetual':
                            ax.scatter(x[i], y[i], c=color, edgecolors=color,
                                       linewidths=0.2, s=14, marker='.', alpha=0.7)
                            ax.scatter(x[i], y[i], c=outline, edgecolors=outline,
                                       linewidths=0.1, s=2.5,
                                       marker='$' + str(5 - player['Markers']['Properties'][i]['Harvest']['age']) + '$',
                                       alpha=0.7)

                    try:
                        if len(obj[i]) <= 3: ax.scatter(x[i], y[i], c=color, alpha=alpha, s=5.0, linewidths=0.075, edgecolors=outline,
                                       marker=obj[i])
                        else: ax.scatter(x[i], y[i], c=color, alpha=alpha, s=10.0, linewidths=0.06, edgecolors=outline,
                                       marker=obj[i])
                    except:
                        try:
                            if len(obj[i]) <= 3: ax.scatter(x[i], y[i], c=color, alpha=alpha, s=5.0, linewidths=0.075, edgecolors=outline,
                                           marker='$' + obj[i] + '$')
                            else: ax.scatter(x[i], y[i], c=color, alpha=alpha, s=10.0, linewidths=0.06, edgecolors=outline,
                                           marker='$' + obj[i] + '$')
                        except:
                            if len(obj[i]) <= 3: ax.scatter(x[i], y[i], c=color, alpha=alpha, s=5.0, linewidths=0.075, edgecolors=outline,
                                           marker='$?$')
                            else: ax.scatter(x[i], y[i], c=color, alpha=alpha, s=10.0, linewidths=0.06, edgecolors=outline,
                                           marker='$?$')
                    '''
                    if 'DisabledAndPermanent' in player['Markers']['Properties'][i]:
                        if player['Markers']['Properties'][i]['DisabledAndPermanent']: color = 'red'
                        ax.scatter(x[i], y[i], c=color, alpha='1.0', s=8.0, marker='$X$', edgecolors='None')
                    '''

                    if player['Markers']['Properties'][i].get('Unit') is not None:
                        if player['Markers']['Properties'][i]['Unit'].get('Artifact'):
                            ax.scatter(x[i] + 0.25, y[i] + 0.25, c="gold", edgecolors='k',
                                       linewidths=0.2, s=7, marker='$✓$', alpha=0.7)



            ax.yaxis.set_major_formatter(ticker.NullFormatter())
            ax.yaxis.set_minor_locator(ticker.FixedLocator(axisn))
            ax.yaxis.set_minor_formatter(ticker.FixedFormatter(axisn + 1))

            ax.xaxis.set_major_formatter(ticker.NullFormatter())
            ax.xaxis.set_minor_locator(ticker.FixedLocator(axisn))
            ax.xaxis.set_minor_formatter(ticker.FixedFormatter(plotLables))

            ax.tick_params(axis='both', which='minor', labelsize=2.5, labeltop=True, labelright=True, bottom=True,
                           top=True, left=True, right=True)
            ax.tick_params(axis='both', which='minor', width=1, labeltop=True, labelright=True, bottom=True, top=True,
                           left=True, right=True)
            ax.tick_params(axis='both', which='minor', length=3, labeltop=True, labelright=True, bottom=True, top=True,
                           left=True, right=True)
            ax.tick_params(axis='both', which='major', length=0, labeltop=True, labelright=True, bottom=True, top=True,
                           left=True, right=True)

            plt.grid(color='k', linestyle='-', linewidth=0.25, alpha=0.5)
            ax.imshow(Data[guild]['Image'][:75,:,:].transpose(1, 0, 2), interpolation='none')
            plt.savefig('tmpgrid.png', format='png', dpi=500)  # , bbox_inches="tight")
            plt.close(fig)
            del fig
            delay = None
            if channel.id != channels[guild][logChannel].id:
                delay = 60 * 2
            if postReply:
                await channel.send(
                    'World Map, You may view a constantly updated map in #changelog-live \n[Auto Delete: 2 mins]:',
                    delete_after=delay, file=discord.File(open('tmpgrid.png', 'br')))
        try:pass
        except Exception as e:
            print('Plot Error', str(e))

"""
Plot The Moon Using Matplotlib
"""
async def plotMoon(channel, postReply=True):
    global Data, plt
    guild = channel.guild.id
    async with channel.typing():
        if 1:#try:
            if channel is None: channel = channels[guild][logChannel]
            # fig, ax = plt.subplots()
            fig = plt.figure(figsize=(5.0, 5.1))
            plt.subplots_adjust(left=0.04, bottom=0.04, right=0.96, top=0.96)
            ax = fig.add_subplot(111)

            axisn = np.arange(0, n, 1)
            plt.xticks(axisn + 0.5)
            plt.yticks(axisn + 0.5)


            for player in Data[guild]['Players'].keys():
                player = Data[guild]['Players'][player]
                color = player['Color']

                if len(player['Markers']['Location']) == 0: continue
                x, y = np.asarray(player['Markers']['Location']).T
                x = x - 76

                obj = np.asarray(player['Markers']['Shape'])
                obj[obj == 'Claim'] = 'None'
                obj[obj == 'Colony'] = '*'
                for unit in Data[guild]['Units'].keys():
                    obj[obj == unit] = Data[guild]['Units'][unit]['Marker']

                for i in range(obj.shape[0]):
                    outline = 'black'
                    if color == 'black': outline = 'white'

                    if obj[i] != "" and player != botName:
                        ax.scatter(x[i], y[i], c="none", edgecolors=color,
                                   linewidths=0.9, s=11*8, marker='s', alpha=0.7)

                    alpha = 1.0
                    if 'Unit' in player['Markers']['Properties'][i] and 'DisabledAndPermanent' in player['Markers']['Properties'][i]['Unit']:
                        alpha = 0.25
                    if player['Markers']['Properties'][i].get('Unit') is not None:
                        unit = player['Markers']['Properties'][i]['Unit']['Name']
                        obj[i] = Data[guild]['Units'][unit]['Marker']
                        if obj[i][0] == '"' and obj[i][-1] == '"':
                            obj[i] = '$' + obj[i][1:-1] + '$'
                        if player['Markers']['Properties'][i]['Unit'].get('Boost'):
                            outline = 'Gold'
                    elif player['Markers']['Properties'][i].get('Harvest') is not None:
                        if player['Markers']['Properties'][i]['Harvest']['type'] == 'Perpetual':
                            ax.scatter(x[i], y[i], c="none", edgecolors=color,
                                       linewidths=0.2, s=14*8, marker='.', alpha=0.7)

                        if player['Markers']['Properties'][i]['Harvest']['type'] == 'Non Perpetual':
                            ax.scatter(x[i], y[i], c=color, edgecolors=color,
                                       linewidths=0.2*3, s=14*8, marker='.', alpha=0.7)
                            ax.scatter(x[i], y[i], c=outline, edgecolors=outline,
                                       linewidths=0.1*3, s=2.5*8,
                                       marker='$' + str(5 - player['Markers']['Properties'][i]['Harvest']['age']) + '$',
                                       alpha=0.7)

                    try:
                        if len(obj[i]) <= 3: ax.scatter(x[i], y[i], c=color, alpha=alpha, s=5.0*8, linewidths=0.075*3, edgecolors=outline,
                                       marker=obj[i])
                        else: ax.scatter(x[i], y[i], c=color, alpha=alpha, s=10.0*8, linewidths=0.06*3, edgecolors=outline,
                                       marker=obj[i])
                    except:
                        if len(obj[i]) <= 3: ax.scatter(x[i], y[i], c=color, alpha=alpha, s=5.0*8, linewidths=0.075*3, edgecolors=outline,
                                       marker='$' + obj[i] + '$')
                        else: ax.scatter(x[i], y[i], c=color, alpha=alpha, s=10.0*8, linewidths=0.06*3, edgecolors=outline,
                                       marker='$' + obj[i] + '$')



            ax.yaxis.set_major_formatter(ticker.NullFormatter())
            ax.yaxis.set_minor_locator(ticker.FixedLocator(axisn))
            ax.yaxis.set_minor_formatter(ticker.FixedFormatter(axisn + 1))

            ax.xaxis.set_major_formatter(ticker.NullFormatter())
            ax.xaxis.set_minor_locator(ticker.FixedLocator(axisn))
            ax.xaxis.set_minor_formatter(ticker.FixedFormatter(plotmoonLables))

            ax.tick_params(axis='both', which='minor', labelsize=2.5*1.5, labeltop=True, labelright=True, bottom=True,
                           top=True, left=True, right=True)
            ax.tick_params(axis='both', which='minor', width=1, labeltop=True, labelright=True, bottom=True, top=True,
                           left=True, right=True)
            ax.tick_params(axis='both', which='minor', length=3, labeltop=True, labelright=True, bottom=True, top=True,
                           left=True, right=True)
            ax.tick_params(axis='both', which='major', length=0, labeltop=True, labelright=True, bottom=True, top=True,
                           left=True, right=True)

            plt.grid(color='k', linestyle='-', linewidth=0.25, alpha=0.5)
            ax.imshow(Data[guild]['Image'][76:,:30,:].transpose(1, 0, 2), interpolation='none')
            plt.savefig('tmpMoon.png', format='png', dpi=150)  # , bbox_inches="tight")
            plt.close(fig)
            del fig
            delay = None
            if channel.id != channels[guild][logChannel].id:
                delay = 60 * 2
            if postReply:
                await channel.send(
                    'Moon Map, You may view a constantly updated map in #changelog-live \n[Auto Delete: 2 mins]:',
                    delete_after=delay, file=discord.File(open('tmpMoon.png', 'br')))
        try:pass
        except Exception as e:
            print('Plot Error', str(e))


#####################################################
#  Necessary Module Functions
#####################################################

async def sendMessages():
    global msgQueue
    while len(msgQueue) != 0:
        msg = msgQueue.pop(0)
        if len(str(msg).strip()) == 0: continue
        print('Sending Msg #', len(msgQueue),'to', msg['channel'].name)
        msg['text'] = msg['text'].replace('@Krozr#0878','\"The Oracle\"')
        msg['text'] = msg['text'].replace('@392883201061814282','\"The Oracle\"')
        await msg['channel'].send(msg['text'])


def addMsgQueue(channel, msg):
    global msgQueue
    msgQueue.append({
        'text': msg,
        'channel': channel
    })


"""
Log Bot Activity To The Specified Guild/Server
Dont Modify Unless You Really Want To I Guess...
"""


def log(guild, msg):
    addMsgQueue(channels[guild][logChannel], msg)


"""
Save Memory Data To File
Dont Modify Unless You Really Want To I Guess...
"""


def saveData():
    global Data, AllData
    AllData[savefile] = Data
    return AllData


"""
Load Memory Data From File
Dont Modify Unless You Really Want To I Guess...
"""


def loadData(inData):
    global Data, AllData
    AllData = inData
    if inData.get(savefile) is None:
        try:
            with open(savefile + '_Data.pickle', 'rb') as handle:
                global Data
                AllData[savefile] = pickle.load(handle)
        except:
            AllData[savefile] = {}
    Data = AllData[savefile]


'''
Data = {
    server1 : {
        'Fed': 'Rates':{}, 'Velocity':{}, 'MemberHistory'{},'Term':0
        'Announcements': {
            'Map': message.id
            'Items': message.id
        }
        'Image': np.array([col,row])
        'Date': "2019-06-29,
        'Players': {
            Player1#0001: {
                'Markers':{
                    'Location': [
                        (23,76), 
                        (74,1),
                        .
                        .
                        (row,col)
                    ]
                    'Shape': [
                        'Claim',
                        'Capital',
                        .
                        .
                        'Claim',
                    ]
                    'Properties':[
                        {
                            'Harvest': {
                                'age': 5
                                'type': 'Perpetual'
                            }
                            'Unit': {
                                'Name':
                                'TownItm
                                'DisabledAndPermanent'
                            }
                        },                    
                        .
                        .
                        {}
                    ]
                }
                'Color': 'red'
                'Claimed Today': False
                'Inventory': {
                    'BF': 25
                    'Wood': 5
                    .
                    .
                    'Item': 999
                }
            }
            Player2#0002: {...}
            .
            .
        }

    },
    
    server2: {...},
    .
    .
    .
    serverN : {...}
}
'''

