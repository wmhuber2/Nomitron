# coding: utf8
#
# Blank Module For Discord Bot
################################
import pickle, sys, random, datetime, yaml, math
channels   = {}
logChannel = ""
Data = {}
AllData = {}
Players = {}
savefile =str(__name__) #+ '_Data.pickle'

"""
Initiate New PlayerF
"""
async def addMember(inData, member):
    global Data
    loadData(inData)
    # Do Stuff Here

    return saveData()

def addItem(guild, player, item, count):
    inv = AllData['Map'][guild]['Players'][player]['Inventory']
    if inv.get(item) is None:
        AllData['Map'][guild]['Players'][player]['Inventory'][item] = 0

    # If Not Allowed To Be Negative
    if inv[item] + count < 0 and item in [
        'BF',
    ]:return False
    else: AllData['Map'][guild]['Players'][player]['Inventory'][item] += count
    if inv[item] == 0 and item != 'BF':
        del AllData['Map'][guild]['Players'][player]['Inventory'][item]
    return True

def sermonThanks(player):
    return "Thank you for attending today's Sermon, <@" + str(Players[player]['id']) + ">. "

def giveReward(player, crackerChance, wineChance,guildid):
    global AllData
    roll = random.random()
    if (roll < crackerChance):
        addItem(guildid, player, 'Cracker', 1)
        return sermonThanks(player) + "I grant you one Cracker. May you never hunger while under my tutelage."
        # todo: add cracker to player inventory
    elif (roll < crackerChance + wineChance):
        addItem(guildid, player, 'Wine', 1)
        return sermonThanks(player) + "I grant you some Wine. It represents the fruits of your labor. I am very proud of you."
        # todo: add wine to player inventory
    else:
        return sermonThanks(player) + "Unfortunately, supplies are limited, and I am unable to grant you a gift. I hope the wisdom you will carry with you from my Sermon will suffice."


"""
Function Called on Reaction
"""
async def reaction(inData, action, user, message, emoji):
    global Data
    loadData(inData)


    guild = message.guild.id
    userName = user.name + '#' + user.discriminator
    isSigil = emoji.name.encode() == Players[userName]['sigil'].encode('utf-8')

    playerData = Data[guild]['Players'][userName]
    # Do Stuff Here
    if((not playerData['tithed']) and action == "add" and isSigil and message.id == Data['sermonID']):
        playerData['tithed'] = True
        if(playerData['attended']):
            blessing = giveReward(userName, 0.3, 0.2,guild)
            await channels[guild]["actions"].send(blessing)

    return saveData()

"""
Main Run Function On Messages
"""
async def run(inData, payload, message):
    global Data, sentences
    loadData(inData)
    # Do Stuff Here


    guild = message.guild.id
    playerData = Data[guild]['Players']
    authorData = playerData[payload['Author']]

    if payload['Content'] == '!newTurn':
        endTurnMessage = ""
        for player in Players.keys():
            playerAttended = playerData[player]['attended']
            playerTithed   = playerData[player]['tithed']

            # Gifts for the flock!
            if(playerAttended and (not playerTithed)): # Tithed item rolls are handled separately
                endTurnMessage = endTurnMessage + giveReward(player, 0.2, 0.1,guild) + "\n"

            # Reset attendance
            playerData[player]['attended'] = False
            playerData[player]['tithed']   = False

        if(endTurnMessage != ""): await channels[guild]["actions"].send(endTurnMessage)

        # Nomitron gives a new sermon
        today = datetime.datetime.today()
        sermonSentence = random.choice(sentences)
        startTurnMessage = u"Welcome, players, to our sermon on this blessed day, {0}, {1} {2}{3}. I invite you all to open your Nomic rulebooks to a favorite quote of mine. “{4}” - {5} {6}:{7}. As you go about your day, think about this quote. Let it grant you wisdom and solace. Amen.".format \
        (
            today.strftime('%A'),
            today.strftime('%B'),
            int(today.strftime('%d')),
            ("th" if 4<=int(today.strftime('%d'))%100<=20 else {1:"st",2:"nd",3:"rd"}.get(int(today.strftime('%d'))%10, "th")),
            sermonSentence["text"],
            sermonSentence["category"],
            sermonSentence["paragraph"],
            sermonSentence["sentence"]
        )
        newSermon = await channels[guild]["actions"].send(startTurnMessage)
        Data['sermonID'] = newSermon.id

    if payload['Content'].lower() in ["amen.","amen"] and (not authorData['attended']):
        authorData['attended'] = True
        if(authorData['tithed']):
            message = giveReward(payload['Author'], 0.3, 0.2,guild)
            await channels[guild]["actions"].send(message)

    return saveData()


"""
Update Function Called Every 10 Seconds
"""
async def update(inData, server):
    global Data
    loadData(inData)
    # Do Stuff Here

    return saveData()



"""
Setup Log Parameters and Channel List And Whatever You Need to Check on a Bot Reset.
Handles Change In Server Structure and the like. Probably Can Leave Alone.
"""
async def setup(inData, chans, logchan, server):
    loadData(inData)
    # Do Stuff Here

    global channels, logChannel, Data, sentences, Players, playerids
    channels = chans
    logChannel = logchan
    guild = server.id

    channels[server.id] = chans

    with open("sermons.yaml",'r') as f:
        sentences = yaml.load(f)['sentences']
    with open("players.yaml",'r') as f:
        Players = yaml.load(f)

    if Data.get('sermonID') is None: Data['sermonID'] = 0
    if Data.get(guild) is None: Data[guild] = {}
    if Data[guild].get('Players') is None: Data[guild]['Players'] = {}
    for player in Players.keys():
        if Data[guild]['Players'].get(player) is None: Data[guild]['Players'][player] = {'attended': False, 'tithed': False}

    return saveData()

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


