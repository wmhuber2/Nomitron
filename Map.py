#
# Map Module For Discord Bot
################################
import pickle, sys, datetime, os, discord, math, re, socket, time, random
np, plt, ticker, mcd = None,None,None,None
n = 75

TILES = {
    'LAND': [45, 84, 55, 255],
    'WATER': [49, 108, 237, 255],
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
itemList = ['BF', 'Corn', 'Fish', 'Food', 'Steel', 'Oil', 'Wood', 'Technology', 'Energy','Gloop']
resourceList = ['Corn', 'Fish', 'Food', 'Steel', 'Oil', 'Wood', 'Technology', 'Energy', 'Gloop']
rawMaterialList = ['Corn', 'Fish', 'Food', 'Steel', 'Oil', 'Wood', 'Technology', 'Energy']
import itertools

letters = 'abcdefghijklmnopqrstuvwxyz'.upper()
labels = []
plotLables = []
for l1, l2 in list(itertools.product(letters, letters))[:75]:
    plotLables.append(l1 + '\n' + l2)
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
                    addMsgQueue(message.channel, "Units Must Be Upgraded On Your Claimed Tile")
                elif unit['UpgradeUnit'] != "" and unit['UpgradeUnit'] != \
                        Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]['Unit']:
                    addMsgQueue(message.channel, "This location cannot be Upgraded To " + name)
                elif unit['UpgradeUnit'] == "" and 'Unit' in \
                        Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]:
                    addMsgQueue(message.channel, "This location Already Has Unit")
                elif canAfford:
                    for cost in unit['Costs']:
                        amount, item = cost.split(' ')
                        addItem(guild, playerName, item, -float(amount))

                    Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]['Unit'] = name
                    addMsgQueue(message.channel, name + "Unit Added On " + str(xa) + str(y + 1) + " For " + playerName)
                else:
                    addMsgQueue(message.channel, "Insufficent Funds")
        else:
            addMsgQueue(message.channel, "Unit Not Found")

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
                    amount = Data[guild]['Players'][playerName]['Claimed Today'] + 2
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
                if addItem(guild, playerName, cost, -1 * amount):
                    if reactorName in ["Doby's Peri#6151", ]:
                        addMsgQueue(message.channel,
                                    "Bad Kid " + reactorName + " has Claimed with " + str(amount) + ' ' + cost)

                    properties = {}
                    if [xcord, ycord] in Data[guild]['Players'][botName]['Markers']['Location']:
                        index = Data[guild]['Players'][botName]['Markers']['Location'].index([xcord,ycord])
                        properties = dict(Data[guild]['Players'][botName]['Markers']['Properties'][index])
                        Data[guild]['Players'][botName]['Markers']['Location'].pop(index)
                        Data[guild]['Players'][botName]['Markers']['Properties'].pop(index)
                        Data[guild]['Players'][botName]['Markers']['Shape'].pop(index)

                    Data[guild]['Players'][playerName]['Markers']['Location'].append([xcord, ycord])
                    Data[guild]['Players'][playerName]['Markers']['Properties'].append(properties)
                    Data[guild]['Players'][playerName]['Markers']['Shape'].append('Claim')
                    Data[guild]['Players'][playerName]['Claimed Today'] += 1
                    addMsgQueue(message.channel, "You have claimed the location. ")
                else:
                    addMsgQueue(message.channel, "You Do Not Have " + str(amount) + ' ' + cost + " To Claim The Tile")

    elif splitContent[0] == '!trade':
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
                            and addItem(guild, targetName, item, amount, testOnly=True):
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
                            for x,y,a in assets:
                                if [x,y] in Data[guild]['Players'][giver]['Markers']['Location'] and (\
                                    [x+1, y+1] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x+1, y  ] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x+1, y-1] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x  , y+1] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
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
                                    print('Region Seed',x,y)
                            assetsToMap = list(assets)
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
                            print('End ATM', assetsToMap)
                            if len(assetsToMap) != 0:            
                                addMsgQueue(message.channel, "Error Trading Tiles:\n "+str('\n\t'.join(badassets)))
                                failed = True
                            else:
                                for x,y,a in set(assets):
                                    tile = [x,y,giver,reciptient]
                                    toSet.append(tile)
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
    elif str(emoji) == str('🔄') and reactorName in Admins:
        payload = {}
        payload['Author'] = message.author.name + "#" + str(message.author.discriminator)
        payload['Nickname'] = message.author.name
        payload['Nickname'] = message.author.nick
        payload['Channel'] = message.channel.name
        payload['Channel Type'] = 'Text'
        payload['Category'] = message.guild.get_channel(message.channel.category_id)
        payload['Content'] = message.system_content.strip()
        payload['Attachments'] = {}

        for file in message.attachments:
            payload['Attachments'][file.filename] = file.url

        await run(inData, payload, message)
    await sendMessages()
    await updateInAnnouncements(message.guild)
    return saveData()


"""
Main Run Function On Messages
"""


async def run(inData, payload, message):
    global Data
    loadData(inData)

    start = time.time()
    # Do Stuff Here

    guild = message.guild.id
    splitContent = payload['Content'].split(' ')

    #  IF A SERVER CHANNEL
    if payload['Channel Type'] == 'Text':
        if Data[guild]['Pause'] and payload['Content'][0] == '!':
            addMsgQueue(message.channel, "Warning: The Bot Has Been Paused.\n Admins May Ignore This Message")

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

        if payload['Channel'].lower() in ['actions-map',] and len(splitContent) != 0:

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

            if splitContent[0] == '!claim' and len(splitContent) == 2:
                if payload['Author'] not in Data[guild]['Players'].keys():
                    addMsgQueue(message.channel, "You havent established a capital yet.")
                else:
                    coords = extractCoords(splitContent[1], message.channel)
                    if coords is not None:
                        xcord, xcordAlpha, ycord = coords
                        claimsLeft = 1 + (hasUnit(guild, payload['Author'], 'explorerguild') * 5) \
                                     - Data[guild]['Players'][payload['Author']]['Claimed Today']

                        if not isTileType(Data[guild]['Image'], xcord, ycord, 'LAND'):
                            addMsgQueue(message.channel, "Please seek more advanced technology to claim Water Tiles.")

                        elif claimsLeft <= 0:
                            addMsgQueue(message.channel,
                                        "You have already purchased a claim today. Please wait until tomorrow to claim again. Have a nice day. :v:")

                        elif [xcord + 1, ycord + 1] in Data[guild]['Players'][payload['Author']]['Markers'][
                            'Location'] or \
                                [xcord + 1, ycord] in Data[guild]['Players'][payload['Author']]['Markers'][
                            'Location'] or \
                                [xcord + 1, ycord - 1] in Data[guild]['Players'][payload['Author']]['Markers'][
                            'Location'] or \
                                [xcord, ycord + 1] in Data[guild]['Players'][payload['Author']]['Markers'][
                            'Location'] or \
                                [xcord, ycord - 1] in Data[guild]['Players'][payload['Author']]['Markers'][
                            'Location'] or \
                                [xcord - 1, ycord + 1] in Data[guild]['Players'][payload['Author']]['Markers'][
                            'Location'] or \
                                [xcord - 1, ycord] in Data[guild]['Players'][payload['Author']]['Markers'][
                            'Location'] or \
                                [xcord - 1, ycord - 1] in Data[guild]['Players'][payload['Author']]['Markers'][
                            'Location']:

                            isClaimed = False
                            for player in Data[guild]['Players'].keys(): 
                                if botName == player: continue
                                isClaimed = isClaimed or (
                                            [xcord, ycord] in Data[guild]['Players'][player]['Markers']['Location'])

                            if isClaimed:
                                addMsgQueue(message.channel, "You cannot claim this location. It is already claimed.")
                            elif hasUnit(guild, payload['Author'], 'explorerguild') != 0:
                                await message.add_reaction('💵')
                                await message.add_reaction('🌮')
                            elif addItem(guild, payload['Author'], 'BF', -2):
                                properties = {}
                                if [xcord, ycord] in Data[guild]['Players'][botName]['Markers']['Location']:
                                    index = Data[guild]['Players'][botName]['Markers']['Location'].index([xcord,ycord])
                                    properties = dict(Data[guild]['Players'][botName]['Markers']['Properties'][index])
                                    Data[guild]['Players'][botName]['Markers']['Location'].pop(index)
                                    Data[guild]['Players'][botName]['Markers']['Properties'].pop(index)
                                    Data[guild]['Players'][botName]['Markers']['Shape'].pop(index)


                                Data[guild]['Players'][payload['Author']]['Markers']['Location'].append([xcord, ycord])
                                Data[guild]['Players'][payload['Author']]['Markers']['Properties'].append(properties)
                                Data[guild]['Players'][payload['Author']]['Markers']['Shape'].append('Claim')
                                Data[guild]['Players'][payload['Author']]['Claimed Today'] += 1
                                addMsgQueue(message.channel, "You have claimed the location. ")
                            else:
                                addMsgQueue(message.channel,
                                            "You Have Insufficient Blemflarcks To Complete This Actions.")

                        else:
                            addMsgQueue(message.channel,
                                        "You cannot claim this location as you have no adjacent markers.")

            if splitContent[0] == '!harvest' and len(splitContent) == 3:
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

                        if [xcord, ycord] in Data[guild]['Players'][payload['Author']]['Markers']['Location']:
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

            if splitContent[0] in ['!unit', '!units'] and len(splitContent) == 3:
                coords, name = splitContent[1:]
                playerName = payload['Author']
                if coords in Data[guild]['Units'].keys(): coords, name = name, coords
                name = name.lower()

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
                        missingItems = ""
                        for cost in unit['Costs']:
                            amount, item = cost.split(' ')
                            if not addItem(guild, playerName, item, -float(amount), testOnly=True):
                                canAfford = False
                                missingItems += '   ' + str(amount) + ' ' + item + "\n"

                        if Data[guild]['Players'][playerName]['Markers']['Shape'][indexTile] == "":
                            addMsgQueue(message.channel, "Units Must Be Upgraded On Your Claimed Tile")
                        elif unit['LandOnly'] and not isTileType(Data[guild]['Image'], x, y, 'LAND'):
                            addMsgQueue(message.channel, "This Can Only Be Placed On Land")
                        elif unit['WaterOnly'] and not isTileType(Data[guild]['Image'], x, y, 'WATER'):
                            addMsgQueue(message.channel, "This Can Only Be Placed On Water")
                        elif unit['BeachOnly'] and not (
                                isTileType(Data[guild]['Image'], x, y, 'LAND')
                                and (
                                        isTileType(Data[guild]['Image'], x + 1, y, 'WATER') or
                                        isTileType(Data[guild]['Image'], x - 1, y, 'WATER') or
                                        isTileType(Data[guild]['Image'], x, y + 1, 'WATER') or
                                        isTileType(Data[guild]['Image'], x, y - 1, 'WATER')
                                )
                        ):
                            addMsgQueue(message.channel, "This Can Only Be Placed On A Beach")
                        elif unit['UpgradeUnit'] != "" and unit['UpgradeUnit'] != \
                                Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]['Unit']:
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

                            Data[guild]['Players'][playerName]['Markers']['Properties'][indexTile]['Unit'] = name
                            addMsgQueue(message.channel, name + "Unit Added On " + str(xa) + str(y + 1) + " ")
                        else:
                            addMsgQueue(message.channel, "Insufficent Funds You Need:" + missingItems)
                elif coords is not None:
                    addMsgQueue(message.channel, "Unit Not Found")

            if splitContent[0] == '!move' and len(splitContent) == 3:
                coord1 = extractCoords(splitContent[1], message.channel)
                coord2 = extractCoords(splitContent[2], message.channel)
                player = payload['Author']
                if coord1 is not None and coord2 is not None:
                    x1, x1a, y1 = coord1
                    x2, x2a, y2 = coord2
                    index1 = None
                    try:
                        index1 = Data[guild]['Players'][player]['Markers']['Location'].index([x1, y1])
                    except ValueError:
                        pass

                    index2 = None
                    try:
                        index2 = Data[guild]['Players'][player]['Markers']['Location'].index([x2, y2])
                    except ValueError:
                        pass

                    targetOccupied = False
                    for playerTest in Data[guild]['Players']:
                        try:
                            ind = Data[guild]['Players'][playerTest]['Markers']['Location'].index([x2, y2])
                            if 'Unit' in Data[guild]['Players'][playerTest]['Markers']['Properties'][ind]:
                                targetOccupied = True
                        except ValueError:
                            pass

                    if abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2 >= 4 or abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2 == 0:
                        addMsgQueue(message.channel, "Movement Must Be to Adjacent Tiles")
                    elif index1 is None:
                        addMsgQueue(message.channel, "No Unit There To Move")
                    elif 'Unit' not in Data[guild]['Players'][player]['Markers']['Properties'][index1]:
                        addMsgQueue(message.channel, "No Unit There To Move")
                    elif targetOccupied:
                        addMsgQueue(message.channel, "2 Units cant exist in the same location")
                    elif not Data[guild]['Units'][
                        Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']
                    ]['isMobile']:
                        addMsgQueue(message.channel, "Unit Is Not Mobile")
                    elif 'DisabledAndPermanent' in Data[guild]['Players'][player]['Markers']['Properties'][index1]:
                        addMsgQueue(message.channel, "Unit Is Disabled")
                    else:
                        unit = Data[guild]['Units'][
                            Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']
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
                            if index2 is None:
                                Data[guild]['Players'][player]['Markers']['Properties'].append({
                                    'Unit': Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']
                                })
                                Data[guild]['Players'][player]['Markers']['Shape'].append("")
                                Data[guild]['Players'][player]['Markers']['Location'].append([x2, y2])
                                del Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']
                            else:
                                Data[guild]['Players'][player]['Markers']['Properties'][index2]['Unit'] \
                                    = "" + str(Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit'])
                                del Data[guild]['Players'][player]['Markers']['Properties'][index1]['Unit']

                            if Data[guild]['Players'][player]['Markers']['Shape'][index1] == "":
                                del Data[guild]['Players'][player]['Markers']['Location'][index1]
                                del Data[guild]['Players'][player]['Markers']['Shape'][index1]
                                del Data[guild]['Players'][player]['Markers']['Properties'][index1]
                            addMsgQueue(message.channel,
                                        "Moving Unit From " + x1a + str(y1 + 1) + " to " + x2a + str(y2 + 1))

            if splitContent[0] == '!toggle' and len(splitContent) == 2:
                coords = extractCoords(splitContent[1], message.channel)
                if coords is not None:
                    xcord, xcordAlpha, ycord = coords
                    index = Data[guild]['Players'][payload['Author']]['Markers']['Location'].index([xcord, ycord])

                    if 'DisabledAndPermanent' in Data[guild]['Players'][payload['Author']]['Markers']['Properties'][
                        index] and \
                            Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index][
                                'DisabledAndPermanent']:
                        Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index][
                            'DisabledAndPermanent'] = False
                        addMsgQueue(message.channel, "Location Enabled. Will Take Effect After Midnight")
                    else:
                        Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index][
                            'DisabledAndPermanent'] = True
                        addMsgQueue(message.channel, "Location Disabled.")
                else:
                    addMsgQueue(message.channel, "You cannot disable this location.")

            if splitContent[0].lower() == '!asset':
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
                            assets.append((coord[0],coord[2],asset))
                            badassets.append(asset)
                            print('asset added',(coord[0],coord[2]) )
                    if 'gives to' in line or linenum == len(msg)-1:
                        if giver is not None and reciptient is not None:
                            #generate map to ensure all tiles are connected by adjacency
                            regionExpanded = True
                            for x,y,a in assets:
                                if [x,y] in Data[guild]['Players'][giver]['Markers']['Location'] and (\
                                    [x+1, y+1] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x+1, y  ] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x+1, y-1] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
                                    [x  , y+1] in Data[guild]['Players'][reciptient]['Markers']['Location'] or \
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
                                    print('Region Seed',x,y)
                            assetsToMap = list(assets)
                            print('Start ATM', assetsToMap)
                            while regionExpanded:
                                regionExpanded = False
                                print(assetsToMap)
                                for x,y,a in set(assetsToMap):
                                    if (x,y) in region:
                                        assetsToMap.remove((x,y,a))
                                        badassets.remove(a)
                                        regionExpranded = True
                                        region.add((x+1,y+1))
                                        region.add((x  ,y+1))
                                        region.add((x-1,y+1))
                                        region.add((x+1,y  ))
                                        region.add((x-1,y  ))
                                        region.add((x+1,y-1))
                                        region.add((x  ,y-1))
                                        region.add((x-1,y-1))
                            print('End ATM', assetsToMap)
                            if len(assetsToMap) != 0:            
                                addMsgQueue(message.channel, "Error Trading Tiles:\n "+str('\n\t'.join(badassets)))
                                failed = True
                            else:
                                for x,y,a in set(assets):
                                    tile = [x,y,giver,reciptient]
                                    toSet.append(tile)
                                print('Done')
                        if linenum != len(msg)-1:
                            giver, reciptient = line.split('gives to')
                            giver      = getPlayer(message.guild, giver.strip()     )
                            reciptient = getPlayer(message.guild, reciptient.strip())
                            players.add(giver)
                            players.add(reciptient)
                    else:
                        print('Else:', line)
                if not failed:
                    addMsgQueue(message.channel, "Asset Trade Requires Approval of: \n"+str(' '.join(players)))
                    await message.add_reaction('👍')
                    await message.add_reaction('👎')

        if payload['Channel'].lower() in ['actions',] and len(splitContent) != 0:
            if splitContent[0] == '!trade':
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

            if splitContent[0].lower() == '!asset':
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

            if splitContent[0] == '!sell' and len(splitContent) == 3:
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

    if payload['Author'] in Admins and payload['Channel'].lower() in ['actions', 'actions-map', 'mod-lounge',
                                                                          'bot-lounge']:

            if payload['Content'] == '!newTurn':
                await onTurnChange(message.guild)
                addMsgQueue(message.channel, "New Turn Initiated")
                print('New Turn')

            if splitContent[0] == '!newDay':
                onDayChange(message.guild)
                await updateInAnnouncements(message.guild, postToSpam=True)

            if payload['Content'] == '!getData':
                await sendMapData(guild=message.guild.id, channel=message.channel)
                print("sending Map_Data File")

            if splitContent[0] == '!remove' and len(splitContent) == 2:
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
                        addMsgQueue(message.channel, "New Turn Initiated")

                else:
                    player = getPlayer(message.guild, splitContent[1], message.channel)
                    if player is not None:
                        del Data[guild]['Players'][player]
                        addMsgQueue(message.channel, 'Player ' + player + ' is removed from the Map.')

            if splitContent[0] == '!setColor' and len(splitContent) == 3:
                if splitContent[1].lower() in mcd.CSS4_COLORS:
                    splitContent[1], splitContent[2] = splitContent[2], splitContent[1]

                player = getPlayer(message.guild, splitContent[1], message.channel)
                if splitContent[2].lower() not in mcd.CSS4_COLORS:
                    addMsgQueue(message.channel, 'Color ' + splitContent[2] + ' is unavailable. Sorry.')
                elif player is not None:
                    Data[guild]['Players'][player]['Color'] = splitContent[2].lower()
                    addMsgQueue(message.channel, 'Player ' + player + ' is now ' + splitContent[2].lower())

            if splitContent[0] == '!getTile' and len(splitContent) == 2:
                coords = extractCoords(splitContent[1], message.channel)
                if coords is not None:
                    xcord, xcordAlpha, ycord = coords
                    msg = "Tile Data:\n"
                    for player in Data[guild]['Players'].keys():
                        try:
                            index = Data[guild]['Players'][player]['Markers']['Location'].index([xcord, ycord])
                            msg += '-' + player + ": " + str(Data[guild]['Players'][player]['Markers']['Shape'][index])
                            msg += '\n' + str(Data[guild]['Players'][player]['Markers']['Properties'][index])
                        except ValueError:
                            pass
                    addMsgQueue(message.channel, msg)

            if splitContent[0] == '!setTile' and len(splitContent) >= 5:
                coords = extractCoords(splitContent[1], message.channel)
                playerName = getPlayer(message.guild, splitContent[2], message.channel)
                shape = splitContent[3]
                properties = eval(' '.join(splitContent[4:]))

                if not isinstance(properties, (dict,)):
                    addMsgQueue(message.channel, 'Properties Is Not Dict.')
                elif shape not in ['Claim', 'Capital']:
                    addMsgQueue(message.channel, 'Shape is Not Claim or Capital')
                elif coords is not None and playerName is not None:
                    x, xa, y = coords
                    for player2 in Data[guild]['Players'].keys():
                        try:
                            index = Data[guild]['Players'][player2]['Markers']['Location'].index([x, y])
                            del Data[guild]['Players'][player2]['Markers']['Location'][index]
                            del Data[guild]['Players'][player2]['Markers']['Shape'][index]
                            del Data[guild]['Players'][player2]['Markers']['Properties'][index]
                        except ValueError:
                            pass

                    Data[guild]['Players'][playerName]['Markers']['Location'].append([x, y])
                    Data[guild]['Players'][playerName]['Markers']['Shape'].append(shape)
                    Data[guild]['Players'][playerName]['Markers']['Properties'].append(properties)

                    addMsgQueue(message.channel, 'Marker Changes Set.')

            if splitContent[0] in ['!resetTimer', '!resetTimers']:
                playerid = None
                if len(splitContent) == 2:
                    playerid = splitContent[1]
                resetTimers(message.guild, playerid=playerid, channel=message.channel)

            if splitContent[0] == ['!setTimer', '!setTimers']:
                playerid = None
                if len(splitContent) == 2:
                    playerid = splitContent[1]
                resetTimers(message.guild, playerid=playerid, channel=message.channel, mode=True)

            if splitContent[0] == '!give':
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

            if payload['Content'] == '!pause':
                Data[guild]['Pause'] = not Data[guild]['Pause']
                addMsgQueue(message.channel, "You Have Paused/Unpaused The Bot. Pause is " + str(Data[guild]['Pause']))

            if payload['Content'] == '!subtractTurn':
                for player in Data[guild]['Players'].keys():
                    for i in range(len(Data[guild]['Players'][player]['Markers']['Shape'])):
                        for prop in Data[guild]['Players'][player]['Markers']['Properties'][i].keys():
                            if prop == 'Harvest':
                                Data[guild]['Players'][player]['Markers']['Properties'][i][prop]['age'] -= 1
                addMsgQueue(message.channel, "Every Player Had one Turn Removed Form Harvest Count")

            if payload['Content'] == '!ping':
                addMsgQueue(message.channel, "pong")

            if splitContent[0] == '!mark' and len(splitContent) == 4:
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

            if splitContent[0] == '!newUnit' and len(splitContent) == 1:
                addMsgQueue(message.channel, str(UNIT_BASE))

            if splitContent[0] == '!newUnit' and len(splitContent) > 1:
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

            if splitContent[0] == '!removeUnit' and len(splitContent) == 2:
                name = splitContent[1]

                if name in Data[guild]['Units']:
                    del Data[guild]['Units'][name]
                    addMsgQueue(message.channel, "Removeing Existing Unit...")
                else:
                    addMsgQueue(message.channel, "Unit Not Found")

            if splitContent[0] == '!setTerm' and len(splitContent) == 2:
                try:
                    term = int(splitContent[1])
                    Data[guild]['Fed']['Term']=term
                except:
                    addMsgQueue(message.channel, splitContent[-2] + ' cannot be quantified into a term 0-5')

            if splitContent[0] == '!adjust':
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
                else:
                    addMsgQueue(message.channel, "Not a valid velocity")
                addMsgQueue(message.channel,'Fed Market Updated')

            if splitContent[0] == '!specialCommand':

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
                                        'TownItem'] = random.choice(resourceList)

                                isOnPlayer = True
                        if not isOnPlayer:
                            Data[guild]['Players'][botName]['Markers']['Shape'].append("")
                            Data[guild]['Players'][botName]['Markers']['Location'].append([x,y])
                            Data[guild]['Players'][botName]['Markers']['Properties'].append({
                                'Unit': 'town',
                                'TownItem': random.choice(resourceList)
                            })

    #  IF A DM CHANNEL
    if payload['Channel Type'] == 'DM':
        pass
    if '!' in payload['Content']:
        print("Run- " + payload['Content'] + ': ', time.time() - start)
    await sendMessages()
    await updateInAnnouncements(message.guild)
    return saveData()


"""
Update Function Called Every 10 Seconds
"""


async def update(inData, server):
    global Data
    loadData(inData)
    # Do Stuff Here

    guild = server.id
    if datetime.datetime.now().strftime("%Y-%m-%d") != Data[guild]['Date']:
        onDayChange(server)
        await sendMapData(guild, channels[guild][logChannel])
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
    Data[guild]['Date'] = datetime.datetime.now().strftime("%Y-%m-%d")

    for chan in ['action', 'actions']:
        if chan in channels[guild].keys():
            addMsgQueue(channels[guild][chan],
                        "New Day Actions Completed: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    log(guild, "Day " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    for player in Data[guild]['Players']:
        for tileIndex in range(len(Data[guild]['Players'][player]['Markers']['Shape'])):

            # IF HARVEST
            if Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].get('Harvest') is not None \
                    and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].get('Unit') is None:
                xcord, ycord = Data[guild]['Players'][player]['Markers']['Location'][tileIndex]

                if isTileType(Data[guild]['Image'], xcord, ycord, 'LAND') and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                            'type'] == 'Perpetual':                    addItem(guild, player, 'Corn', 3)

                if isTileType(Data[guild]['Image'], xcord, ycord, 'WATER') and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                            'type'] == 'Perpetual':                    addItem(guild, player, 'Fish', 3)

                if isTileType(Data[guild]['Image'], xcord, ycord, 'LAND') and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                            'type'] == 'Non Perpetual':                    addItem(guild, player, 'Steel', 1)

                if isTileType(Data[guild]['Image'], xcord, ycord, 'WATER') and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                            'type'] == 'Non Perpetual':                    addItem(guild, player, 'Oil', 1)

                Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['age'] += 1
                if Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                    'type'] == 'Non Perpetual' and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['age'] >= 5:
                    del Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']

            # IF UNIT
            if 'Unit' in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex] \
                    and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].get('DisabledAndPermanent') is not True:
                name = Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']
                unit = dict(Data[guild]['Units'][name])

                canAfford = True
                for cost in unit['DailyCosts']:
                    if ' ' in cost:
                        amount, item = cost.split(' ')
                        canAfford = canAfford and addItem(guild, player, item, -float(amount), testOnly=True)

                if not canAfford:
                    addMsgQueue(channels[guild]['actions'],
                                '@' + player + ' You Have Insufficient Funds For Your ' + name + '.\n Unit is disabled, will retry in 1 Day.')
                    Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['DisabledAndPermanent'] = False
                else:
                    if 'DisabledAndPermanent' in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex] and \
                            not Data[guild]['Players'][player]['Markers']['Properties'][tileIndex][
                                'DisabledAndPermanent']:
                        del Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['DisabledAndPermanent']
                    
                    if name == 'town':                    
                        gift = Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].get('TownItem')
                        if gift == None:
                            gift = random.choice(resourceList)
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['TownItem'] = gift
                        addItem(guild, player, gift, float(2))
                        
                    for cost in unit['DailyCosts']:
                        if ' ' in cost:
                            amount, item = cost.split(' ')
                            addItem(guild, player, item, -float(amount))
                    for cost in unit['DailyReturn']:
                        if ' ' in cost:
                            amount, item = cost.split(' ')
                            addItem(guild, player, item, float(amount))

    for item in Data[guild]['Fed']['Rates'].keys():
        vel = Data[guild]['Fed']['Velocity'][item]
        Data[guild]['Fed']['Rates'][item] += vel/100.0 * Data[guild]['Fed']['Rates'][item]
                    
    print("OnDayChange: ", time.time() - start)


"""
Called On Turn Change
"""
async def onTurnChange(server):
    global Data

    start = time.time()
    guild = server.id
    Data[guild]['Fed']['Term'] += 1
    if Data[guild]['Fed']['Term'] >= 5:
        Data[guild]['Fed']['Term'] += 0
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
            newMember = random.choice(minList)
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
        elif ycord >= n or ycord < 0 or xcord >= n or xcord < 0:
            addMsgQueue(channel, Coords +" is outside the map.")
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
    if inv[item] + count < 0 and item in ['BF', 'Corn', 'Fish', 'Food', 'Steel', 'Oil', 'Wood', 'Technology', 'Energy']:
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
    if not postToSpam and oldData == pickle.dumps(
            [
                Data[guild]['Players'],
                Data[guild]['Fed'],
            ]
            , protocol=pickle.HIGHEST_PROTOCOL):
        # print('Up To Date. Skipping Plot')
        return 1
    else:
        print('Updating Plot')
        oldData = pickle.dumps(Data[guild]['Players'], protocol=pickle.HIGHEST_PROTOCOL)

    playerOrder = [
        'Alekosen#8467',
        'Boolacha#4539',
        'Krozr#0878',
        'Crorem#6962',
        'Fenris Wolf#6136',
        'Rabz12#9343',
        'Steam:HaphStealth Bnet#1191#5187',
        "Doby's Peri#6151",
        'Janwich#4842',
        'gfigs#6656',
        'iann39#8298',
    ]
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
        msg += '\n-Times On Fed: '+str(Data[guild]['Fed']['MemberHistory'][player])
        msg += '\n-Tiles:'
        totalRenewableHarvests = 0
        totalNonRenewableHarvests = 0
        Total = 0
        itemDelta = {
            'BF': {'-': 0.0, '+': 0.0},
        }
        for tileIndex in range(len(Data[guild]['Players'][player]['Markers']['Shape'])):
            x, y = Data[guild]['Players'][player]['Markers']['Location'][tileIndex]
            # if isTileType(Data[guild]['Image'],x , y, 'LAND'): totalLand+=1
            # if isTileType(Data[guild]['Image'],x , y, 'WATER'): totalWater+=1
            Total += 1
            for prop in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].keys():
                if prop == 'Unit' and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].get(
                            'DisabledAndPermanent') is None:
                    unit = Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Unit']

                    if unit == 'town':
                        itm = Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].get('TownItem')
                        if itm == None:
                            itm = random.choice(resourceList)
                            Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['TownItem'] = itm
                        if itemDelta.get(itm) is None:
                            itemDelta[itm] = {'-': 0.0, '+': 0.0}
                        itemDelta[itm]['+'] += float(2)
                        
                    for cst in Data[guild]['Units'][unit]['DailyCosts']:
                        a, itm = cst.split(' ')
                        if itemDelta.get(itm) is None:
                            itemDelta[itm] = {'-': 0.0, '+': 0.0}
                        itemDelta[itm]['-'] += float(a)
                    for cst in Data[guild]['Units'][unit]['DailyReturn']:
                        a, itm = cst.split(' ')
                        if itemDelta.get(itm) is None:
                            itemDelta[itm] = {'-': 0.0, '+': 0.0}
                        itemDelta[itm]['+'] += float(a)
                elif prop == 'Harvest' and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                    'type'] == 'Perpetual' and 'Unit' not in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]:
                    totalRenewableHarvests += 1
                elif prop == 'Harvest' and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest'][
                    'type'] == 'Non Perpetual' and 'Unit' not in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]:
                    totalNonRenewableHarvests += 1

        msg += "\n\tTotal Tiles:" + str(Total) + \
               '\n\tRenewable Harvests:' + str(totalRenewableHarvests) + \
               '\n\tNon-Renewable Harvests:' + str(totalNonRenewableHarvests)
        msg += "\n-Inventory:       | Gains  | Loss   | Total "

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
                deltaplus += totalRenewableHarvests * 3.0
            if item == 'Steel':
                deltaplus += totalNonRenewableHarvests
            if item in Data[guild]['Players'][player]['Inventory'].keys():
                amount = float(Data[guild]['Players'][player]['Inventory'][item])
            if item in itemDelta.keys():
                deltaplus += float(itemDelta[item]['+'])
                deltaloss += float(itemDelta[item]['-'])
            delta = deltaplus - deltaloss
            if delta < 0:
                sign = ""
            if delta == 0 and amount == 0: continue

            #deltaloss = int(deltaloss)
            #deltaplus = int(deltaplus)
            #delta     = int(delta)

            tmpmsg = "\n   " + item + ': ' + str(amount)
            tmpmsg += (19 - len(tmpmsg)) * ' ' + '| +'+str(deltaplus)
            tmpmsg += (28 - len(tmpmsg)) * ' ' + '| -' + str(deltaloss)
            tmpmsg += (37 - len(tmpmsg)) * ' ' + '| ' +sign + str(delta)
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

    # Update Map
    if reload: await plotMap(channels[guild][logChannel], False)

    junkmsg = await channels[server.id][logChannel].send(
        'World Map:', file=discord.File(open('tmpgrid.png', 'br')))
    url = "World Map: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\n " + junkmsg.attachments[0].url
    if Data[guild]['Announcements']['Map'] is None:
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


    # Update Fed Board
    msg =    "FEDERAL RATES (Turns Left in Term: " + str(5-Data[guild]['Fed']['Term'])+')'
    msg += "\n    ITEM     :: BF RATE ::  VELOCITY "
    msg += "\n----------------------------------------"
    for item in rawMaterialList:
        if Data[guild]['Fed']['Rates'].get(item) is None:
            Data[guild]['Fed']['Rates'][item] = 100
        if Data[guild]['Fed']['Velocity'].get(item) is None:
            Data[guild]['Fed']['Velocity'][item] = 0
        rate = Data[guild]['Fed']['Rates'][item]
        vel =  Data[guild]['Fed']['Velocity'][item]

        tmpmsg = "\n " + item.upper()
        tmpmsg += (14 - len(tmpmsg)) * ' ' + '::  ' + str(round(rate,1))
        tmpmsg += (25 - len(tmpmsg)) * ' ' + '::  ' + str(int(vel))+'% / Day'
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


"""
Determines If PLayer Has A Unit
"""
def hasUnit(guildid, player, unit):
    unitCount = 0
    for tile in range(len(Data[guildid]['Players'][player]['Markers']['Location'])):
        props = Data[guildid]['Players'][player]['Markers']['Properties'][tile]
        if 'Unit' not in props:
            continue
        elif unit in props['Unit']:
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
    # Do Stuff Here

    global channels, logChannel, Data
    global np, plt, ticker, mcd
    import numpy as np
    import matplotlib

    matplotlib.use('Agg')

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
            data = np.asarray(img).copy()
            for r in range(data.shape[0]):
                for c in range(data.shape[1]):
                    if data[r, c, 2] > 150:
                        data[r, c] = [49, 108, 237, 255]
                    else:
                        data[r, c] = [45, 84, 55, 255]
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

    for player in Data[guild]['Players'].keys():
        #if Data[guild]['Players'][player].get('Object') is None:
        #    Data[guild]['Players'][player]['Object'] = server.get_member_named(player)
        if Data[guild]['Players'][player].get('Inventory') is None:
            Data[guild]['Players'][player]['Inventory'] = {'BF': 0, }

        if player not in Data[guild]['Fed']['MemberHistory']:
            if player in ['NomicBotPossibly#4870',botName]: continue
            Data[guild]['Fed']['MemberHistory'][player] = 0
        if Data[guild]['Players'][player]['Markers'].get('Properties') is None:
            Data[guild]['Players'][player]['Markers']['Properties'] = []
            for tile in Data[guild]['Players'][player]['Markers']['Shape']:
                Data[guild]['Players'][player]['Markers']['Properties'].append({})
        else:
            for tile in range(len(Data[guild]['Players'][player]['Markers']['Shape'])):
                props = Data[guild]['Players'][player]['Markers']['Properties'][tile]
                if 'Unit' not in props:
                    continue
                else:
                    Data[guild]['Players'][player]['Markers']['Properties'][tile]['Unit'] = props['Unit'].lower()



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

            for player in Data[guild]['Players'].keys():
                player = Data[guild]['Players'][player]
                color = player['Color']
                
                outline = 'black'
                if color == 'black': outline = 'white'

                if len(player['Markers']['Location']) == 0: continue
                x, y = np.asarray(player['Markers']['Location']).T
                obj = np.asarray(player['Markers']['Shape'])
                obj[obj == 'Claim'] = 'None'
                obj[obj == 'Capital'] = '*'
                for unit in Data[guild]['Units'].keys():
                    obj[obj == unit] = Data[guild]['Units'][unit]['Marker']
                for i in range(obj.shape[0]):
                    if obj[i] != "":
                        ax.scatter(x[i], y[i], c="none", edgecolors=color,
                                   linewidths=0.3, s=11, marker='s', alpha=0.7)

                    if player['Markers']['Properties'][i].get('Unit') is not None:
                        unit = player['Markers']['Properties'][i]['Unit']
                        obj[i] = Data[guild]['Units'][unit]['Marker']
                        if obj[i][0] == '"' and obj[i][-1] == '"':
                            obj[i] = '$' + obj[i][1:-1] + '$'
                    elif player['Markers']['Properties'][i].get('Harvest') is not None:
                        if player['Markers']['Properties'][i]['Harvest']['type'] == 'Perpetual':
                            ax.scatter(x[i], y[i], c="none", edgecolors=color,
                                       linewidths=0.2, s=14, marker='.', alpha=0.7)

                        if player['Markers']['Properties'][i]['Harvest']['type'] == 'Non Perpetual':
                            ax.scatter(x[i], y[i], c=color, edgecolors=color,
                                       linewidths=0.2, s=14, marker='.', alpha=0.7)
                            ax.scatter(x[i], y[i], c=outline, edgecolors=outline,
                                       linewidths=0.1, s=2.5, 
                                       marker='$'+str(5-player['Markers']['Properties'][i]['Harvest']['age'])+'$', alpha=0.7)
                    alpha = 1.0
                    if 'DisabledAndPermanent' in player['Markers']['Properties'][i]:
                        alpha = 0.25

                    try:
                        if len(obj[i]) <= 3:
                            ax.scatter(x[i], y[i], c=color, alpha=alpha, s=5.0, linewidths=0.075, edgecolors=outline,
                                       marker=obj[i])
                        else:
                            ax.scatter(x[i], y[i], c=color, alpha=alpha, s=10.0, linewidths=0.06, edgecolors=outline,
                                       marker=obj[i])
                    except:
                        if len(obj[i]) <= 3:
                            ax.scatter(x[i], y[i], c=color, alpha=alpha, s=5.0, linewidths=0.075, edgecolors=outline,
                                       marker='$' + obj[i] + '$')
                        else:
                            ax.scatter(x[i], y[i], c=color, alpha=alpha, s=10.0, linewidths=0.06, edgecolors=outline,
                                       marker='$' + obj[i] + '$')
                    '''
                    if 'DisabledAndPermanent' in player['Markers']['Properties'][i]:
                        if player['Markers']['Properties'][i]['DisabledAndPermanent']: color = 'red'
                        ax.scatter(x[i], y[i], c=color, alpha='1.0', s=8.0, marker='$X$', edgecolors='None')
                    '''
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
            ax.imshow(Data[guild]['Image'].transpose(1, 0, 2), interpolation='none')
            plt.savefig('tmpgrid.png', format='png', dpi=500)  # , bbox_inches="tight")
            del fig
            print('Saved')
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


#####################################################
#  Necessary Module Functions
#####################################################

async def sendMessages():
    global msgQueue
    while len(msgQueue) != 0:
        msg = msgQueue.pop(0)
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
