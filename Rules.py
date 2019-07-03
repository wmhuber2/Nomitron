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

    if (splitPayload[0] == "!search" or splitPayload[0] == "!find"):
        text = ' '.join(splitPayload[1:]).lower()
        if text[0] == '"': text = text[1:]
        if text[1] == '"': text = text[:-2]
        print (text)
        for rule in Data.keys():
            low = Data[rule].lower()
            if text in low:
                isIn = 1
                count = 5
                initIndex = 0
                msg = '`'+str(rule)+':`\n'
                while isIn and count > 0:
                    try:
                        index = low[initIndex:].index(text)
                        index += initIndex

                        initIndex = index + len(text)

                        boundLower = index - 40
                        if boundLower < 0:boundLower = 0

                        boundUpper = index + 120
                        if boundUpper >= len(low): boundUpper = len(low)-1

                        msg +=('\t...'\
                              +Data[rule][boundLower:index]\
                              +'**'+ Data[rule][index:index+len(text)]\
                              +'**'+ Data[rule][index+len(text):boundUpper]\
                              +'...').replace('\n','  ')+'\n\n'
                    except ValueError:
                        isIn = 0
                    count -= 1
                if count <= 0:
                    msg += '...and more...'
                await message.channel.send(msg)

        pass

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


