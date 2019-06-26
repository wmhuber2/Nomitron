#
# Blank Module For Discord Bot
################################
import pickle, sys, urllib
channels   = {}
logChannel = ""
Data = {}
savefile = str(__name__) + '_Data.pickle'

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

    splitPayload = payload['Content'].split()
    if(splitPayload[0] == "!rule" and len(splitPayload) == 2):
        rulequery = int(splitPayload[1])
        if(rulequery not in Data.keys()):
            await channels[payload['Channel']].send("I couldn't find that rule.")
        else:
            answer = Data[rulequery].split("\n\n")
            response = "Rule"+answer[0]
            answer = answer[1:]
            for paragraph in answer:
                if(len(response) + len(paragraph) + 2 > 2000):
                    await channels[payload['Channel']].send(response)
                    response = ""
                response = response + "\n\n" + paragraph
            await channels[payload['Channel']].send(response)
            

    await saveData()


"""
Update Function Called Every 10 Seconds
"""
async def update(server):
    global Data
    # Do Stuff Here

    await saveData()



"""
Setup Log Parameters and Channel List And Whatever You Need to Check on a Bot Reset.
Handles Change In Server Structure and the like. Probably Can Leave Alone.
"""
async def setup(chans, logchan, guild):
    global channels, logChannel, Data
    channels = chans
    logChannel = logchan

    await loadData()
    # Do Stuff Here

    with urllib.request.urlopen('https://raw.githubusercontent.com/dmouscher/nomic/master/rules-3.md') as response:
        rules = response.read().decode()
        ruletxt = rules.split('##')[1:]
        for rule in ruletxt:
            rulenum = int(rule.split()[0])
            Data[rulenum] = rule

    await saveData()

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


