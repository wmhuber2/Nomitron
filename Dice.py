#
# Blank Module For Discord Bot
################################
import pickle, sys, random
channels   = {}
logChannel = ""
Data = {}
AllData = {}
savefile =str(__name__) # + '_Data.pickle'

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

    return saveData()



"""
Main Run Function On Messages
"""
async def run(inData, payload, message):
    global Data
    loadData(inData)
    # Do Stuff Here
    guild = message.guild.id
    splitContent = payload['Content'].split(' ')

    if payload['Channel'].lower() in ['actions', 'actions-map', 'mod-lounge','bot-spam','bot-lounge', 'pizza-party','anti-league-league'] and len(splitContent) != 0:
        if splitContent[0] == '!roll' and len(splitContent) == 2:
            if 'd' in splitContent[1]:
                n, d = splitContent[1].split('d')
                intable = False
                try:
                    n = int(n)
                    d = int(d)
                    intable = True
                except:
                    pass
                if intable:
                    rolls = [random.randint(1,d) for i in range(n)]
                    s = sum(rolls)
                    await message.channel.send("Rolled: "+str(s)+" : "+str(rolls))


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
async def setup(inData, chans, logchan, guild):
    global channels, logChannel, Data
    channels, logChannel = chans, logchan
    loadData(inData)
    # Do Stuff Here

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

