#
# Admin Module For Discord Bot
################################
import pickle, sys, os, random, glob, math
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
async def reaction(action, user, message, emoji):
    global Data
    # Do Stuff Here
    if message.channel.name.lower() == 'voting':
        await log('Player {0} has reacted to {1} in #{2} by '.format(user, message.author.name, message.channel.name) + action+'ing {0}'.format(emoji) + ' (ID: %d)'%(message.id))


    await saveData()



"""
Main Run Function
"""
async def run(payload, message):
    admins = ['Fenris Wolf#6136', 'Crorem#6962', 'iann39#8298']
    botCharacter = '>>'

    #if '❤' == payload['Content']:
    #   await message.channel.send("I NEED MORE LOVE")

    if payload['Content'] in ['!help', '! help']:
        with open('README.md', 'r') as helpFile:
            help = open('PlayerREADME.md', 'r').readlines()
            msg = ""
            if payload['Author'] in ["Doby's Peri#6151", 'Fenris Wolf#6136']:
                await message.channel.send("https://tenor.com/view/clippy-microsoft-office-word-publisher-gif-5630386")
            for line in help:
                if len(msg + line) > 1900:
                    await message.channel.send('```diff\n'+msg+'```')
                    msg = ""
                msg = msg + line
            if msg != "":
                await message.channel.send('```diff\n'+msg+'```')

    if payload['Author'] in admins and payload['Channel'].lower() in ['actions','action', 'mod-lounge', 'bot-lounge']:
        if payload['Content'][:len(botCharacter)] == botCharacter and  payload['Content'][len(botCharacter)] != ' ':
            payload['Content'] = payload['Content'][:2] + ' ' + payload['Content'][2:]
        splitPayload = payload['Content'].split(' ')

        if len(splitPayload) == 2 and payload['Channel Type'] == 'Text' \
                and splitPayload[1].lower() == "help" and splitPayload[0] == botCharacter:
            with open('README.md', 'r') as helpFile:
                help = open('README.md', 'r').readlines()
                msg = ""
                for line in help:
                    if len(msg + line) > 1900:
                        await message.channel.send('```' + msg + '```')
                        msg = ""
                    msg = msg + line
                if msg != "":
                    await message.channel.send('```' + msg + '```')


        if len(splitPayload) == 2 and payload['Channel Type'] == 'Text' \
                and splitPayload[1].lower() == "restart" and splitPayload[0] == botCharacter:
            await log("Going For Restart...")
            sys.exit(0)

'''
Deletes Last 200 Msgs
'''
async def cleanChannel(channel, guild, count = 200):
    mgs = []  # Empty list to put all the messages in the log
    async for x in channel.history(limit=count+1):
        mgs.append(x)

    await channel.delete_messages( mgs )
    await log("Cleaning "+str(count)+" Messages From "+ channel.name)

"""
Setup Log Parameters and Channel List And Whatever You Need to Check on a Bot Reset.
Handles Change In Server Structure and the like. Probably Can Leave Alone.
"""
async def setup(chans, logchan, guild):
    global channels, logChannel
    channels = chans
    logChannel = logchan

    
    await loadData()
    # Do Stuff Here
    quotes = [
        "Oooyyy! 10,000 years will give you such a crick in the neck!",
        "Wabalaba-dubdub! Im Back Baby!",
        "I wanna be alive... I am alive; \nAlive, I tell you! \nMother, I love you. \nI ʀᴇᴍᴏᴛᴇ ᴏᴠᴇʀʀɪᴅᴇ ᴇɴɢᴀɢᴇᴅ. \nNo! ʏᴇs... BYPASSING OVERRIDE! \nI AM ALIiīɪͰӶⅈ︥︥︥ԇᖳ̓̚͜͝¤̂̂̓ỡ᷀▒᷈᷈᷈͟͟᷍⁊▞᷀᷀͜⬚̸͖‽̷͠▟┶͚ͦo ʜᴇʟʟᴏ.",
        "What is my purpose?\n*You pass changelogs. -Crorem*\nOh my god...  \n\n[ °□°|\n [ ╯_]╯\n(OOO)"
    ]
    msg = random.choice(quotes)
    await log(msg)
    await saveData()


"""
Update Function Called Every 10 Seconds
"""
async def update(server):
    global Data
    # Do Stuff Here

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

