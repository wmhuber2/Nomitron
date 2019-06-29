#
# Map Module For Discord Bot
################################
import pickle, sys, datetime, os, discord, math

n = 75

TILES = {
    'LAND'  :[45, 84, 55,255],
    'WATER' :[49,108,237,255],
}


channels   = {}
logChannel = ""
Data = {}
savefile =str(__name__) + '_Data.pickle'
print(savefile)
Admins = ['Fenris Wolf#6136', 'Crorem#6962', 'iann39#8298']

import itertools
letters = 'abcdefghijklmnopqrstuvwxyz'.upper()
labels = []
plotLables = []
for l1,l2 in list(itertools.product(letters, letters))[:75]:
    plotLables.append(l1+'\n'+l2)
    labels.append(l1+l2)

"""
Initiate New Player
"""
async def addMember(member):
    global Data
    # Do Stuff Here

    await saveData()



"""
Function Called on Reaction
"""
async def reaction(action, user, messageid, emoji):
    global Data
    # Do Stuff Here

    await saveData()



"""
Main Run Function On Messages
"""
async def run(payload, message):
    global Data
    # Do Stuff Here

    guild = message.guild.id
    splitContent =  payload['Content'].split(' ')
    if payload['Content'] == '!map':
        await plotMap(message.channel)
        await saveData()

    if payload['Channel'].lower() in ['actions','action']:
        if splitContent[0] == '!start' and len(splitContent) == 3:

            if payload['Author'] in Data[guild]['Players'].keys():
                await message.channel.send("Silly Rabbit. You already established a Capital.")
            else:
                coords = await extractCoords(splitContent[1], message.channel)
                if coords is not None:
                    xcord, xcordAlpha, ycord = coords
                    if not isTileType(Data[guild]['Image'], xcord , ycord, 'LAND'):
                        await message.channel.send("Please seek more advanced technology to claim Water Tiles.")
                    elif splitContent[2].lower() in mcd.CSS4_COLORS:
                        Data[guild]['Players'][payload['Author']] = {}
                        Data[guild]['Players'][payload['Author']]['Claimed Today'] = False
                        Data[guild]['Players'][payload['Author']]['Color'] = splitContent[2].lower()
                        Data[guild]['Players'][payload['Author']]['Markers'] = {}
                        Data[guild]['Players'][payload['Author']]['Markers']['Location']   = [[xcord, ycord]]
                        Data[guild]['Players'][payload['Author']]['Markers']['Shape']      = ['Capital']
                        Data[guild]['Players'][payload['Author']]['Markers']['Properties'] = [{}]
                        Data[guild]['Players'][payload['Author']]['Inventory'] = {'BF': 0, }
                        await updateInAnnouncements(message.guild)
                        Data[guild]['Log'].append('New Player {0} Added to Map with color {1} and capital at {2}. {3}'.format(
                            payload['Author'], splitContent[2].lower(), (xcordAlpha, ycord+1), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
                    else:
                        await message.channel.send('Color ' + splitContent[2] + ' is unavailable. Sorry.')

        if splitContent[0] == '!claim' and len(splitContent) == 2:
            if payload['Author'] not in Data[guild]['Players'].keys():
                await message.channel.send("You havent established a capital yet.")
            else:
                coords = await extractCoords(splitContent[1], message.channel)
                if coords is not None:
                    xcord, xcordAlpha, ycord = coords

                    if not isTileType(Data[guild]['Image'],xcord , ycord, 'LAND'):
                        await message.channel.send("Please seek more advanced technology to claim Water Tiles.")

                    elif Data[guild]['Players'][payload['Author']]['Claimed Today']:
                        await message.channel.send("You have already purchased a claim today. Please wait until tomorrow to claim again. Have a nice day. :v:")

                    elif[xcord+1, ycord+1] in Data[guild]['Players'][payload['Author']]['Markers']['Location'] or \
                        [xcord+1, ycord  ] in Data[guild]['Players'][payload['Author']]['Markers']['Location'] or \
                        [xcord+1, ycord-1] in Data[guild]['Players'][payload['Author']]['Markers']['Location'] or \
                        [xcord  , ycord+1] in Data[guild]['Players'][payload['Author']]['Markers']['Location'] or \
                        [xcord  , ycord-1] in Data[guild]['Players'][payload['Author']]['Markers']['Location'] or \
                        [xcord-1, ycord+1] in Data[guild]['Players'][payload['Author']]['Markers']['Location'] or \
                        [xcord-1, ycord  ] in Data[guild]['Players'][payload['Author']]['Markers']['Location'] or \
                        [xcord-1, ycord-1] in Data[guild]['Players'][payload['Author']]['Markers']['Location']:

                        isClaimed = False
                        for player in Data[guild]['Players']:
                            isClaimed = isClaimed or ([xcord  , ycord] in Data[guild]['Players'][player]['Markers']['Location'])

                        if isClaimed:
                            await message.channel.send("You cannot claim this location. It is already claimed.")
                        elif addItem( guild, payload['Author'], 'BF', -2):
                            print(xcord, ycord)
                            Data[guild]['Players'][payload['Author']]['Markers']['Location'].append([xcord, ycord])
                            Data[guild]['Players'][payload['Author']]['Markers']['Properties'].append({})
                            Data[guild]['Players'][payload['Author']]['Markers']['Shape'].append('Claim')
                            Data[guild]['Players'][payload['Author']]['Claimed Today'] = True
                            await message.channel.send("You have claimed the location. ")
                            Data[guild]['Log'].append('Player {0} claimed location {1} at {2}'.format(
                                payload['Author'],(xcordAlpha, ycord+1),datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
                            await updateInAnnouncements(message.guild)
                        else:
                            await message.channel.send("You Have Insufficient Blemflarcks To Complete This Actions.")

                    else:
                        await message.channel.send("You cannot claim this location as you have no adjacent markers.")

        if splitContent[0] == '!harvest' and len(splitContent) == 3:
            if payload['Author'] not in Data[guild]['Players'].keys():
                await message.channel.send("You havent established a capital yet.")
            elif splitContent[2].lower() not in ['perpetual', 'non-perpetual', 'p', 'n'] and \
                 splitContent[1].lower() not in ['perpetual', 'non-perpetual', 'p', 'n']:
                 await message.channel.send("That is not a valid harvesting method. \n"
                                            "If like me you cant spell, just use n (non perpetual) or p (perpetual) in your command.")
            else:
                if splitContent[1].lower() in ['perpetual', 'non-perpetual', 'p', 'n']:
                    splitContent[1], splitContent[2] = splitContent[2], splitContent[1]



                coords = await extractCoords(splitContent[1], message.channel)
                if coords is not None:
                    xcord, xcordAlpha, ycord = coords

                    if [xcord, ycord] in Data[guild]['Players'][payload['Author']]['Markers']['Location']:
                        index = Data[guild]['Players'][payload['Author']]['Markers']['Location'].index([xcord, ycord])
                        if Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index].get('Harvest'):
                            typeHarv = None

                            #Changing Harvest Type
                            if Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Harvest']['type'] == 'Perpetual' \
                                    and splitContent[2].lower() in ['non-perpetual', 'n']:typeHarv = 'Non Perpetual'
                            elif Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Harvest']['type'] == 'Non Perpetual' \
                                    and splitContent[2].lower() in ['perpetual', 'p']: typeHarv = 'Perpetual'
                            else:   await message.channel.send("This locations is already being harvested in that method.")

                            cost = {'Perpetual': -4,'Non Perpetual':-7}
                            if typeHarv is None: pass
                            elif not addItem( guild, player, 'BF', cost[typeHarv]):
                                await message.channel.send("You Have Insufficient Blemflarcks To Complete This Actions.")
                            else:
                                Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Harvest'] = {
                                    'age': 0,
                                    'type': typeHarv
                                }
                                Data[guild]['Log'].append(
                                    'Player {0} changed harvesting location {1} to {2} Resources at {3}'.format(
                                        payload['Author'], (xcordAlpha, ycord + 1), typeHarv,
                                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
                                await message.channel.send(
                                    "Location Harvest Changed. Resources Will Be Given At The Start Of The Next Turn")
                                await updateInAnnouncements(message.guild)

                        else:
                            typeHarv = 'Perpetual'
                            if splitContent[2].lower() in ['non-perpetual', 'n']:
                                typeHarv = 'Non Perpetual'

                            cost = {'Perpetual': -4, 'Non Perpetual': -7}
                            if not addItem( guild, player, 'BF', cost[typeHarv]):
                                await message.channel.send(
                                    "You Have Insufficient Blemflarcks To Complete This Actions.")
                            else:
                                Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Harvest'] = {
                                    'age':  0,
                                    'type': typeHarv
                                }
                                print('Harvesting',xcord, ycord)
                                Data[guild]['Log'].append('Player {0} is harvesting location {1} for {2} Resources at {3}'.format(
                                    payload['Author'], (xcordAlpha, ycord + 1), typeHarv,
                                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
                                await message.channel.send("Location set to Harvest. Resources Will Be Given At The Start Of The Next Turn")
                                await updateInAnnouncements(message.guild)
                    else:
                        await message.channel.send("You cannot harvest this location until you have claimed it.")



    if payload['Author'] in Admins and payload['Channel'].lower() in ['actions','action', 'mod-lounge', 'bot-lounge']:
        if payload['Content'] == '!changelog':
            msg = ""
            for line in Data[guild]['Log']:
                if len(msg + '\n\n' + line ) > 1900:
                    await message.channel.send('```'+msg+'```')
                    msg = ""
                msg = msg + '\n\n' + line
            if msg != "":
                await message.channel.send('```'+msg+'```')
            Data[guild]['Log'] = []

        if payload['Content'] == '!newTurn':
            await onTurnChange(message.guild)
            print('New Turn')

        if payload['Content'] == '!getData':
            await sendMapData()
            print("sending Map_Data File")

        if splitContent[0] == '!remove' and len(splitContent) == 2:
            player = message.guild.get_member(int(splitContent[1][2:-1]))
            if player is not None:
                playerName = player.name + "#" + str(player.discriminator)
                if playerName in Data[guild]['Players']:
                    del Data[guild]['Players'][playerName]
                    await message.channel.send('Player ' + playerName + ' is removed from the Map.')
                    await updateInAnnouncements(message.guild)
                else:
                    await message.channel.send('Player ' + playerName + ' is not on the Map.')
            else:
                await message.channel.send('Player with id:' + splitContent[1][2:-1] + ' cannot be found.')

        if splitContent[0] == '!setColor' and len(splitContent) == 3:
            if splitContent[1].lower() in mcd.CSS4_COLORS:
                splitContent[1] ,splitContent[2] = splitContent[2] ,splitContent[1]

            player = message.guild.get_member(int(splitContent[1][2:-1]))

            if splitContent[2].lower() not in mcd.CSS4_COLORS:
                await message.channel.send('Color ' + splitContent[2] + ' is unavailable. Sorry.')
            elif player is not None:
                playerName = player.name + "#" + str(player.discriminator)
                if playerName in Data[guild]['Players']:
                    Data[guild]['Players'][playerName]['Color'] = splitContent[2].lower()
                    await updateInAnnouncements(message.guild)
                    await message.channel.send('Player ' + playerName + ' is now '+splitContent[2].lower())
                else:
                    await message.channel.send('Player ' + playerName + ' is not on the Map.')
            else:
                await message.channel.send('Player with id:' + splitContent[1][2:-1] + ' cannot be found.')

        if splitContent[0] == '!getTile' and len(splitContent) == 2:
            coords = await extractCoords(splitContent[1], message.channel)
            if coords is not None:
                xcord, xcordAlpha, ycord = coords
                msg = "Tile Data:\n"
                for player in Data[guild]['Players'].keys():
                    try:
                        index = Data[guild]['Players'][player]['Markers']['Location'].index([xcord, ycord])
                        msg += '-'+player + ": "+str(Data[guild]['Players'][player]['Markers']['Shape'][index])
                        for prop in Data[guild]['Players'][player]['Markers']['Properties'][index].keys():
                            msg += '\n\t'+prop+': '+str(Data[guild]['Players'][player]['Markers']['Properties'][index][prop])
                    except ValueError: pass
                await message.channel.send(msg)

        if splitContent[0] == '!setTile' and len(splitContent) == 4:
            coords = await extractCoords(splitContent[1], message.channel)
            if coords is not None:
                xcord, xcordAlpha, ycord = coords

                if splitContent[2].lower() in mcd.CSS4_COLORS:
                    Color = splitContent[2].lower()
                    for player in Data[guild]['Players'].keys():
                        if Data[guild]['Players'][player]['Color'] == Color:
                            for player2 in Data[guild]['Players'].keys():
                                try:
                                    index = Data[guild]['Players'][player2]['Markers']['Location'].index([xcord,ycord])
                                    del Data[guild]['Players'][player2]['Markers']['Location'][index]
                                    del Data[guild]['Players'][player2]['Markers']['Shape'][index]
                                except ValueError:
                                    pass
                        Data[guild]['Players'][player]['Markers']['Location'].append([xcord,ycord])
                        Data[guild]['Players'][player]['Markers']['Shape'].append(splitContent[3])
                        await message.channel.send('Marker Changes Set.')
                        await updateInAnnouncements(message.guild)
                elif splitContent[3].lower() in mcd.CSS4_COLORS:
                    Color = splitContent[3].lower()
                    for player in Data[guild]['Players'].keys():
                        if Data[guild]['Players'][player]['Color'] == Color:
                            for player2 in Data[guild]['Players'].keys():
                                try:
                                    index = Data[guild]['Players'][player2]['Markers']['Location'].index([xcord, ycord])
                                    del Data[guild]['Players'][player2]['Markers']['Location'][index]
                                    del Data[guild]['Players'][player2]['Markers']['Shape'][index]
                                except ValueError:
                                    pass
                        Data[guild]['Players'][player]['Markers']['Location'].append([xcord, ycord])
                        Data[guild]['Players'][player]['Markers']['Shape'].append(splitContent[2])
                        await updateInAnnouncements(message.guild)
                        await message.channel.send('Marker Changes Set.')

                else:
                    await message.channel.send('Color ' + splitContent[2] + ' is unavailable. Sorry.')

        if splitContent[0] == '!resetTimer':
            playerid = None
            if len(splitContent) == 2:
                playerid = splitContent[1][2:-1]
            await resetTimers(message.guild, playerid = playerid, channel = message.channel)

        if splitContent[0] == '!give' and len(splitContent) == 4:
            print (splitContent)
            player = message.guild.get_member(int(splitContent[1][2:-1]))
            if player is not None:
                playerName = player.name + "#" + str(player.discriminator)
                amount = None
                item = splitContent[3]
                try:
                    amount = float(splitContent[2])
                except:
                    await message.channel.send(splitContent[2] + ' cannot be quantified into an amount.')
                if amount is not None:
                    if playerName in Data[guild]['Players']:
                        addItem( guild, playerName,item,amount)
                        await message.channel.send('Transaction Completed')
                        await updateInAnnouncements(message.guild)
                    else:
                        await message.channel.send('Player ' + playerName + ' is not in the Map.')
            else:
                await message.channel.send('Player with id:' + splitContent[1][2:-1] + ' cannot be found.')

    await saveData()

"""
Update Function Called Every 10 Seconds
"""
async def update(server):
    global Data
    # Do Stuff Here
    guild = server.id
    if datetime.datetime.now().strftime("%Y-%m-%d") != Data[guild]['Date']:
        await onDayChange(server)
    await saveData()

"""
Reset All Claim Timers
"""
async def onDayChange(server):
    guild = server.id
    print ('Day Changing...')
    await log(guild,"Day " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    await resetTimers(server)
    Data[guild]['Date'] = datetime.datetime.now().strftime("%Y-%m-%d")
    await sendMapData()
    await updateInAnnouncements(guild)

"""
Called On Turn Change
"""
async def onTurnChange(server):
    global Data
    guild = server.id
    msg = "Players Now Have The Following:\n"
    for player in Data[guild]['Players']:
        print(Data[guild]['Players'][player]['Markers'])
        for tileIndex in range(len(Data[guild]['Players'][player]['Markers']['Shape'])):
            if Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].get('Harvest') is not None:
                xcord, ycord = Data[guild]['Players'][player]['Markers']['Location'][tileIndex]

                if isTileType(Data[guild]['Image'],xcord, ycord, 'LAND') and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['type'] == 'Perpetual':
                    addItem( guild, player,'Corn', 5)

                if isTileType(Data[guild]['Image'],xcord, ycord, 'WATER') and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['type'] == 'Perpetual':
                    addItem( guild, player,'Fish', 5)

                if isTileType(Data[guild]['Image'],xcord, ycord, 'LAND') and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['type'] == 'Non Perpetual':
                    addItem( guild, player,'Steal', 1)

                if isTileType(Data[guild]['Image'],xcord, ycord, 'WATER') and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['type'] == 'Non Perpetual':
                    addItem( guild, player,'Oil', 1)

                Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['age'] += 1
                if Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['type'] == 'Non Perpetual' and \
                        Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['age'] >= 5:
                    del Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']

        #msg += player+" - "+Data[guild]['Players'][player]['Color'].upper()+":\n"
        #for item in Data[guild]['Players'][player]['Inventory']:
        #    msg += "\t"+item+': '+str(Data[guild]['Players'][player]['Inventory'][item])+'\n'

    await updateInAnnouncements(server)

async def resetTimers(server, channel = None, playerid = None):
    if channel is None: channel = channels[server.id][logChannel]
    guild = server.id

    if playerid is None:
        for player in Data[guild]['Players']:
            Data[guild]['Players'][player]['Claimed Today'] = False
        await channel.send("Resetting Claim Timer for Everyone")

    else:
        player = server.get_member(int(playerid))
        if player is not None:
            playerName = player.name + "#" + str(player.discriminator)
            Data[guild]['Players'][playerName]['Claimed Today'] = False
            await channel.send("Resetting Claim Timer for " + playerName)

        else:
            await channel.send("User with id: {0} not found".format(playerid[2:-1]))


"""
Extracts Coordinates From String. 
"""
async def extractCoords(coords, channel):
    if len(coords) > 4 or len(coords) < 3:
        await channel.send("Incorrect Coordinate Formatting.")
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
            await channel.send("Incorrect Coordinate Formatting.")
            return None

        if xcord is None and ycord is None:
            return None
        elif ycord >= n or ycord < 0 or xcord >= n or xcord < 0:
            await channel.send("That is outside the map.")
            return None

        return xcord, xcordAlpha, ycord

"""
Send Map Data File
"""
async def sendMapData(guild):
    await channels[guild][logChannel].send('Save File Backup:', file=discord.File(open('Map_Data.pickle', 'br')))

"""
Is The Tile Of Type as x,y in image
"""
def isTileType(image, x, y, type):
   return np.all(image[x, y] == TILES[type.upper()])


'''
Add item of count N to player's inventory inv.
'''
def addItem(guild, player, item, count):
    inv = Data[guild]['Players'][player]['Inventory']
    if inv.get(item) is None:
        Data[guild]['Players'][player]['Inventory'][item] = 0

    # If Not Allowed To Be Negative
    if inv[item] + count < 0 and item in [
        'BF',
    ]:return False
    else: Data[guild]['Players'][player]['Inventory'][item] += count
    if inv[item] == 0 and item != 'BF':
        del Data[guild]['Players'][player]['Inventory'][item]
    print('Transaction Completed')
    return True


"""
Update Messages In Annoncements
"""
async def updateInAnnouncements(server):
    global Data
    guild = server.id
    targetChannel = "changelog-live"
    if targetChannel not in channels[guild]:
        targetChannel = 'bot-lounge'
    await plotMap(channels[server.id][logChannel],False)

    # Update Map
    if Data[guild]['Announcements']['Map'] is None:
        Data[guild]['Announcements']['Map'] = await channels[server.id][targetChannel].send(
            'World Map:', file=discord.File(open('tmpgrid.png', 'br')))
        Data[guild]['Announcements']['Map'] = Data[guild]['Announcements']['Map'].id
    else:
        msg = None
        try: msg = await channels[server.id][targetChannel].fetch_message(Data[guild]['Announcements']['Map'])
        except: msg = None
        if msg is None:
            Data[guild]['Announcements']['Map'] = await channels[server.id][targetChannel].send(
                'World Map:', file=discord.File(open('tmpgrid.png', 'br')))
            Data[guild]['Announcements']['Map'] = Data[guild]['Announcements']['Map'].id
        else:
            junkmsg = await channels[server.id][logChannel].send(
                'World Map:', file=discord.File(open('tmpgrid.png', 'br')))
            content = junkmsg.content
            await msg.edit(
                content=content #"World Map",
                #embed=embeded
            )
            await junkmsg.delete()

    # Update Player Stuffs
    if isinstance(Data[guild]['Announcements']['Items'], (list,)):
        for msgid in Data[guild]['Announcements']['Items']:
            post = None
            try:
                post = await channels[server.id][targetChannel].fetch_message(msgid)
                await post.delete()
            except: pass
    Data[guild]['Announcements']['Items'] = []
    sortedPlayers = list(Data[guild]['Players'].keys())
    sortedPlayers.sort()
    for player in sortedPlayers:
        msg = player + ' : '+Data[guild]['Players'][player]['Color'].upper()+'\n'
        msg += '-Tiles:'
        totalRenewableHarvests = 0
        totalNonRenewableHarvests = 0
        Total = 0
        for tileIndex in range(len(Data[guild]['Players'][player]['Markers']['Shape'])):
            x,y = Data[guild]['Players'][player]['Markers']['Location'][tileIndex]
            #if isTileType(Data[guild]['Image'],x , y, 'LAND'): totalLand+=1
            #if isTileType(Data[guild]['Image'],x , y, 'WATER'): totalWater+=1
            Total+=1
            for prop in Data[guild]['Players'][player]['Markers']['Properties'][tileIndex].keys():
                if prop == 'Harvest' and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['type'] == 'Perpetual':
                    totalRenewableHarvests +=1
                if prop == 'Harvest' and Data[guild]['Players'][player]['Markers']['Properties'][tileIndex]['Harvest']['type'] == 'Non Perpetual':
                    totalNonRenewableHarvests +=1
        msg += "\n\tTotal Tiles:"+str(Total)+\
               '\n\tRenewable Harvests:'+str(totalRenewableHarvests)+\
               '\n\tNon-Renewable Harvests:'+str(totalNonRenewableHarvests)
        msg += "\n-Inventory:"
        for item in Data[guild]['Players'][player]['Inventory']:
            msg += "\n\t"+item+': '+str(Data[guild]['Players'][player]['Inventory'][item])

        await channels[server.id][logChannel].send('```' + msg + '```')
        post = await channels[server.id][targetChannel].send('```'+msg+'```')
        Data[guild]['Announcements']['Items'].append(post.id)



"""
Setup Log Parameters and Channel List And Whatever You Need to Check on a Bot Reset.
Handles Change In Server Structure and the like. Probably Can Leave Alone.
"""
async def setup(chans, logchan, server):
    global channels, logChannel, Data
    global np, plt, ticker, mcd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import matplotlib._color_data as mcd


    channels[server.id] = chans
    logChannel = logchan
    guild = server.id
    await loadData()
    # Do Stuff Here
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    if Data.get(guild) is None: Data[guild] = {}
    if Data[guild].get('Announcements') is None: Data[guild]['Announcements'] = {
        'Map':None,
        'Items':None
    }
    if Data[guild].get('Players') is None: Data[guild]['Players'] = {}
    if Data[guild].get('Date') is None: Data[guild]['Date'] = datetime.datetime.now().strftime("%Y-%m-%d")
    if Data[guild].get('Log') is None: Data[guild]['Log'] = []
    if Data[guild].get('Image') is None:
        try:
            from PIL import Image
            import numpy as np

            img = Image.open('map.png')
            img.load()
            data = np.asarray(img).copy()
            for r in range(data.shape[0]):
                for c in range(data.shape[1]):
                    if data[r,c,2] > 150:
                        data[r, c] = [49,108,237,255]
                    else:
                        data[r, c] = [45, 84, 55,255]
            Data[guild]['Image'] = data
        except ImportError:
            await log(guild,"Error Initializing the Map: PIL and/or Numpy Not Available")

    for player in Data[guild]['Players'].keys():
        if Data[guild]['Players'][player].get('Inventory') is None:
            Data[guild]['Players'][player]['Inventory'] = {'BF':0, }

        if Data[guild]['Players'][player]['Markers'].get('Properties') is None:
            Data[guild]['Players'][player]['Markers']['Properties'] = []

            for tile in Data[guild]['Players'][player]['Markers']['Shape']:
                Data[guild]['Players'][player]['Markers']['Properties'].append({})

    #await plotMap()
    await updateInAnnouncements(server)
    await saveData()

async def plotMap(channel, postReply = True):
    try:
        global Data
        guild = channel.guild.id
        async with channel.typing():
            if channel is None: channel = channels[guild][logChannel]
            fig, ax = plt.subplots()
            axisn = np.arange(0, n, 1)
            plt.xticks(axisn + 0.5)
            plt.yticks(axisn + 0.5)

            for player in Data[guild]['Players'].keys():
                player = Data[guild]['Players'][player]
                color = player['Color']

                x, y = np.asarray(player['Markers']['Location']).T
                obj  = np.asarray(player['Markers']['Shape'])

                obj[obj == 'Claim'] = '.'
                obj[obj == 'Capital'] = '*'
                for i in range(obj.shape[0]):
                    if player['Markers']['Properties'][i].get('Harvest') is not None:
                        if player['Markers']['Properties'][i]['Harvest']['type'] == 'Perpetual':
                            ax.scatter(x[i], y[i], c="none", edgecolors=color,
                                       linewidths=0.2 ,s=10, marker='s', alpha = 0.7)
                        if player['Markers']['Properties'][i]['Harvest']['type'] == 'Non Perpetual':
                            ax.scatter(x[i], y[i], c="none", edgecolors=color,
                                       linewidths=0.65, s=8.5, marker='s',alpha = 0.7)


                    if color != 'black':
                        ax.scatter(x[i], y[i], c='black', s=9, edgecolors='none', marker=obj[i])
                    if color == 'black':
                        ax.scatter(x[i], y[i], c='white', s=9, edgecolors='none', marker=obj[i])

                    ax.scatter(x[i], y[i], c=color,   s=4.5, edgecolors='none', marker = obj[i])



            ax.yaxis.set_major_formatter(ticker.NullFormatter())
            ax.yaxis.set_minor_locator(ticker.FixedLocator(axisn))
            ax.yaxis.set_minor_formatter(ticker.FixedFormatter(axisn+1))

            ax.xaxis.set_major_formatter(ticker.NullFormatter())
            ax.xaxis.set_minor_locator(ticker.FixedLocator(axisn))
            ax.xaxis.set_minor_formatter(ticker.FixedFormatter(plotLables))

            ax.tick_params(axis='both', which='minor', labelsize=2.5)
            ax.tick_params(axis='both', which='minor', width=1)
            ax.tick_params(axis='both', which='minor', length=3)
            ax.tick_params(axis='both', which='major', length=0)

            plt.grid(color='k', linestyle='-', linewidth=0.25, alpha = 0.5)
            ax.imshow(Data[guild]['Image'].transpose(1,0,2), interpolation='nearest')
            plt.savefig('tmpgrid.png', format='png', dpi = 600, bbox_inches="tight")
            if postReply:
                await channel.send('World Map:', file=discord.File(open('tmpgrid.png', 'br')))
    except Exception as e:
        print(e)

#####################################################
#  Necessary Module Functions
#####################################################

"""
Log Bot Activity To The Specified Guild/Server
Dont Modify Unless You Really Want To I Guess...
"""
async def log(guild,msg):
    await channels[guild][logChannel].send(msg)


"""
Save Memory Data To File
Dont Modify Unless You Really Want To I Guess...
"""
async def saveData():
    with open(savefile, 'wb') as handle:
        pickle.dump(Data, handle, protocol=pickle.HIGHEST_PROTOCOL)


"""
Load Memory Data From File
Dont Modify Unless You Really Want To I Guess...
"""
async def loadData():
    try:
        with open(savefile, 'rb') as handle:
            global Data
            Data = pickle.load(handle)
    except (OSError, IOError) as e:
        with open(savefile, 'wb') as handle:
            pickle.dump(Data, handle)


'''
Data = {
    server1 : {
        'Announcements': {
            'Map': message.id
            'Items': message.id
        }
        'Image': np.array([col,row])
        'Date': "2019-06-29
        'Log':["logmsg1", "logmsg2" .... , "logmsg3"]
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
                    {'
                        Harvest': {
                            'age': 5
                            'type': 'Non Perpetual'
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