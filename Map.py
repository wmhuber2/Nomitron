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
            elif len(splitContent[1]) > 4 or len(splitContent[1]) < 3:
                await message.channel.send("Incorrect Coordinate Formatting.")
            else:
                xcord = None
                xcordAlpha = None
                ycord = None
                if splitContent[1][:2].upper() in labels:
                    xcordAlpha = splitContent[1][0:2].upper()
                    xcord = int(labels.index(xcordAlpha))
                    ycord = int(splitContent[1][2:]) - 1
                elif splitContent[1][-2:].upper() in labels:
                    xcordAlpha = splitContent[1][-2:].upper()
                    xcord = int(labels.index(xcordAlpha))
                    ycord = int(splitContent[1][:-2]) - 1
                else:
                    await message.channel.send("Incorrect Coordinate Formatting.")

                if xcord is None and ycord is None:
                    pass
                elif not np.all(Data[guild]['Image'][xcord , ycord] == TILES['LAND']):
                    await message.channel.send("Please seek more advanced technology to claim Water Tiles.")
                elif ycord >= n  or ycord < 0:
                    await message.channel.send("That is outside the map.")
                elif splitContent[2].lower() in mcd.CSS4_COLORS:
                    Data[guild]['Players'][payload['Author']] = {}
                    Data[guild]['Players'][payload['Author']]['Claimed Today'] = False
                    Data[guild]['Players'][payload['Author']]['Color'] = splitContent[2].lower()
                    Data[guild]['Players'][payload['Author']]['Markers'] = {}
                    Data[guild]['Players'][payload['Author']]['Markers']['Location'] = [[xcord, ycord]]
                    Data[guild]['Players'][payload['Author']]['Markers']['Shape']    = ['Capital']
                    Data[guild]['Players'][payload['Author']]['Inventory'] = {'BF': 0, }
                    await plotMap(message.channel)
                    Data[guild]['Log'].append('New Player {0} Added to Map with color {1} and capital at {2}. {3}'.format(
                        payload['Author'], splitContent[2].lower(), (xcordAlpha, ycord+1), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

                else:
                    await message.channel.send('Color ' + splitContent[2] + ' is unavailable. Sorry.')

        if splitContent[0] == '!claim' and len(splitContent) == 2:
            if payload['Author'] not in Data[guild]['Players'].keys():
                await message.channel.send("You havent established a capital yet.")
            elif len(splitContent[1]) > 4 or len(splitContent[1]) < 3:
                await message.channel.send("Incorrect Coordinate Formatting.")
            else:
                xcord = None
                xcordAlpha = None
                ycord = None
                if splitContent[1][:2].upper() in labels:
                    xcordAlpha = splitContent[1][0:2].upper()
                    xcord = int(labels.index(xcordAlpha))
                    ycord = int(splitContent[1][2:]) - 1
                elif splitContent[1][-2:].upper() in labels:
                    xcordAlpha = splitContent[1][-2:].upper()
                    xcord = int(labels.index(xcordAlpha))
                    ycord = int(splitContent[1][:-2]) - 1
                else:
                    await message.channel.send("Incorrect Coordinate Formatting.")


                if xcord is None and ycord is None:
                    pass

                elif ycord >= n  or ycord < 0 or xcord >= n  or xcord < 0:
                    await message.channel.send("That is outside the map.")

                elif not np.all(Data[guild]['Image'][xcord , ycord] == TILES['LAND']):
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
                    else:
                        print(xcord, ycord)
                        Data[guild]['Players'][payload['Author']]['Markers']['Location'].append([xcord, ycord])
                        Data[guild]['Players'][payload['Author']]['Markers']['Shape'].append('Claim')
                        Data[guild]['Players'][payload['Author']]['Claimed Today'] = True
                        await message.channel.send("You have claimed the location. ")
                        Data[guild]['Log'].append('Player {0} claimed location {1} at {2}'.format(
                            payload['Author'],(xcordAlpha, ycord+1),datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
                        await plotMap(message.channel)
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

                if len(splitContent[1]) > 4 or len(splitContent[1]) < 3:
                    await message.channel.send("Incorrect Coordinate Formatting.")
                else:
                    xcord = None
                    xcordAlpha = None
                    ycord = None
                    if splitContent[1][:2].upper() in labels:
                        xcordAlpha = splitContent[1][0:2].upper()
                        xcord = int(labels.index(xcordAlpha))
                        ycord = int(splitContent[1][2:]) - 1
                    elif splitContent[1][-2:].upper() in labels:
                        xcordAlpha = splitContent[1][-2:].upper()
                        xcord = int(labels.index(xcordAlpha))
                        ycord = int(splitContent[1][:-2]) - 1
                    else:
                        await message.channel.send("Incorrect Coordinate Formatting.")


                    if xcord is None and ycord is None:
                        pass

                    elif ycord >= n  or ycord < 0 or xcord >= n  or xcord < 0:
                        await message.channel.send("That is outside the map.")

                    elif [xcord, ycord] in Data[guild]['Players'][payload['Author']]['Markers']['Location']:
                        index = Data[guild]['Players'][payload['Author']]['Markers']['Location'].index([xcord, ycord])
                        if Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index].get('Harvest'):
                            await message.channel.send("This locations is already being hravested. (Fuck Spelling)")
                        else:

                            Data[guild]['Players'][payload['Author']]['Markers']['Properties'][index]['Harvest'] = {
                                'age':  0,
                                'type': splitContent[2][0].lower()
                            }
                            print('Harvesting',xcord, ycord)
                            await message.channel.send("Location set to Harvest. Resources Will Be Given At The Start Of The Next Turn")
                            await plotMap(message.channel)
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
        
        if splitContent[0] == '!remove' and len(splitContent) == 2:
            player = message.guild.get_member(int(splitContent[1][2:-1]))
            if player is not None:
                playerName = player.name + "#" + str(player.discriminator)
                if playerName in Data[guild]['Players']:
                    del Data[guild]['Players'][playerName]
                    await message.channel.send('Player ' + playerName + ' is removed from the Map.')
                else:
                    await message.channel.send('Player ' + playerName + ' is not on the Map.')
            else:
                await message.channel.send('Player with id:' + splitContent[1][2:-1] + ' cannot be found.')

        if splitContent[0] == '!set' and len(splitContent) == 4:
            if len(splitContent[1]) > 4 or len(splitContent[1]) < 3:
                await message.channel.send("Incorrect Coordinate Formatting.")
            else:
                xcord = None
                ycord = None
                if splitContent[1][:2].upper() in labels:
                    xcord = splitContent[1][0:2].upper()
                    xcord = int(labels.index(xcord))
                    ycord = int(splitContent[1][2:]) - 1
                elif splitContent[1][-2:].upper() in labels:
                    xcord = splitContent[1][-2:].upper()
                    xcord = int(labels.index(xcord))
                    ycord = int(splitContent[1][:-2]) - 1
                else:
                    await message.channel.send("Incorrect Coordinate Formatting.")

                if xcord is None and ycord is None:
                    pass
                elif ycord >= n or ycord < 0:
                    await message.channel.send("That is outside the map.")
                elif splitContent[2].lower() in mcd.CSS4_COLORS:
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
                        await plotMap(message.channel)
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
                        await plotMap(message.channel)
                        await message.channel.send('Marker Changes Set.')

                else:
                    await message.channel.send('Color ' + splitContent[2] + ' is unavailable. Sorry.')

        if splitContent[0] == '!resetTimer':
            if len(splitContent) == 1:
                await message.channel.send("Admin Resetting Claim Timers... Day " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                for player in Data[guild]['Players']:
                    Data[guild]['Players'][player]['Claimed Today'] = False
            if len(splitContent) == 2:
                player = message.guild.get_member(int(splitContent[1][2:-1]))
                if player is not None:
                    playerName = player.name + "#" + str(player.discriminator)

                    await message.channel.send("Resetting Claim Timer for "+playerName)
                    Data[guild]['Players'][playerName]['Claimed Today'] = False
                else:
                    await message.channel.send("User with id: {0} not found".format(splitContent[1][2:-1]))

    await saveData()

"""
Update Function Called Every 10 Seconds
"""
async def update(server):
    global Data
    # Do Stuff Here
    guild = server.id
    if datetime.datetime.now().strftime("%Y-%m-%d") != Data[guild]['Date']:
        await log("Resetting Claim Timers... Day "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        for player in Data[guild]['Players']:
            Data[guild]['Players'][player]['Claimed Today'] = False
        Data[guild]['Date'] = datetime.datetime.now().strftime("%Y-%m-%d")
        await channels[logChannel].send('Save File Backup:', file=discord.File(open('Map_Data.pickle', 'br')))

    await saveData()

async def onTurnChange(server):
    global Data
    guild = server.id
    for player in Data[guild]['Players']:
        for tileIndex in range(len(Data[guild]['Players'][player]['Markers']))


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


    channels = chans
    logChannel = logchan
    guild = server.id
    await loadData()
    # Do Stuff Here
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    if Data.get(guild) is None: Data[guild] = {}
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
            await log("Error Initializing the Map: PIL and/or Numpy Not Available")

    for player in Data[guild]['Players'].keys():
        if Data[guild]['Players'][player].get('Inventory') is None:
            Data[guild]['Players'][player]['Inventory'] = {'BF':0, }
        if Data[guild]['Players'][player]['Markers'].get('Properties') is None:
            Data[guild]['Players'][player]['Markers']['Properties'] = []
            for tile in Data[guild]['Players'][player]['Markers']['Shape']:
                Data[guild]['Players'][player]['Markers']['Properties'].append({})

    #await plotMap()
    await saveData()


async def plotMap(channel = None):
    global Data
    guild = channel.guild.id
    async with channel.typing():
        if channel is None: channel = channels[logChannel]
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
                if player['Markers']['Properties'].get('Harvest'):
                    if player['Markers']['Properties']['Harvest']['type'] == 'p':
                        ax.scatter(x[i], y[i], c='none', s=15, edgecolors=color, marker='x')
                    if player['Markers']['Properties']['Harvest']['type'] == 'n':
                        ax.scatter(x[i], y[i], c='none', s=15, edgecolors=color, marker='X')

                if color != 'black':
                    ax.scatter(x[i], y[i], c='black', s=8, edgecolors='none', marker=obj[i])
                if color == 'black':
                    ax.scatter(x[i], y[i], c='white', s=8, edgecolors='none', marker=obj[i])
                
                ax.scatter(x[i], y[i], c=color,   s=5, edgecolors='none', marker = obj[i])



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
        await channel.send('World Map:', file=discord.File(open('tmpgrid.png', 'br')))


#####################################################
#  Necessary Module Functions
#####################################################

"""
Log Bot Activity To The Specified Guild/Server
Dont Modify Unless You Really Want To I Guess...
"""
async def log(msg):
    await channels[logChannel].send(msg)


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
                            'type': 'p'
                        }
                        
                    },
                    {'
                        Harvest': {
                            'age': 5
                            'type': 'n'
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