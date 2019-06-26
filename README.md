# Nomitron

#### Nomic Bot with implementable modules for Python 3.6 or Greater.
    
    "Nomitron.py" is the main script to be executed.
    Script "run.py" runs Nomitron in the background detached from shell. 
    
    !!! YOU MUST RUN run.py IF LAUNCHING FROM SSH TERMINAL TO PREVENT PROCESS FROM BEING KILLED ON SSH CLOSE!!!
    
    It automatically updates from git and keeps the bot active on errors.
    
    DiscordBot.py is the main bot script, and can be run independently.
    It implements all modules and passes the arguments to them.
    It has non-blocking error catching and reporting built in to print to terminal.


#### Adding Modules:
    1. Copy and Rename Blank.py
    2. Program your module in the run(), startup(), addMember(), and reaction() functions.
#### Current Modules:

    Admin [Channels: mod-lounge, actions]: 
        >> Restart              : Restart The Bot To Pull Updates
        >> disable $module      : Disable Module $module
        >> enable $module       : Enable Module $module
        >> help                 : Reply with README
    
    Rules [Channels: all]:
        !rule $num              : Diplay Rule Number $num if it exists.
        
    Map:
        Player Actions:
        !start {coordinates} {color}    : Add Capital to map, and declare your color. [Channels: actions]
        !claim {coordinates}            : Claim Coordinates [Channels: actions]
        !map                            : Display Current Map [Channels: all]  
        
        Admin/Mod Only [Channels: mod-lounge, actions]:
        !changelog                          : Display All Successfull Player Actions Since Last Changelog
        !resetTimer                         : Rest All Player Claim Timers
        !resetTimer @player                 : Rest @player Claim Timer
        !set {coordinates} {color} {marker} : Set Marker on Tile to color
        !set {coordinates} {marker} {color} : Set Marker on Tile to color
        !remove @player                     : Remove Player from map. Resets as if new.
    
    Blank:
        Blank Module As Template For New Modules.
        
        run() is called on every message
        reaction() is called on a reaction update event with add/revove events
        addMember() is called on new member joins
        setup() runs on bot restart to handle things like server structure change
   
 