Hi. It looks like you need some help. Some commands are listed below.

Admin:
-    !map
+        Allowed Channels: ALL excluding Actions
+        Display Current Map.
+        Rule: 312
-    !newTurn
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       Starts a new turn. Prints Current Player Resources
+       Rule: 314
-    !changelog
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       Prints The Completed Actions Since the last changelog
+       Rule: N/A
-    !getData {coords}
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       Sends The Current Map File
+       Rule: N/A
-    !setColor @player $color
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       Set A Players Color
+       Rule: N/A
-    !getTile {coords}
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       Prints the tile Informations
+       Rule: N/A
-    !setTile {coords} @player $type $params
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       Set A Tile
+       $type is Claim, Capital, etc
+       params is a dictionary like:
+           {'Harvest': {'age':0, 'type':'Perpetual'}}
+       Rule: N/A
-    !remove @player
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       Remove A Player and all data from map
+       Rule: N/A
-    !resetTimer @player
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       if a player is given reset that player's timer
+       else reset all timers
+       Rule: N/A
-    !setTimer @player
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       if a player is given disable that player's timer
+       else reset all timers
+       Rule: N/A
-    !give {list @player} #count $item
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       give players # count of $item
+        #count can be deciaml and negative
+       Rule: N/A
-    !pause
+       toggles Pause State.
+       pause stops all player commands 
+       admin commands may be executed
-    !subtractTurn
+       subtracts one from every age counter in Harvest Tiles
-    !ping
+       ping bot for a response
This Bot's Code May Be Found At:
https://github.com/wmhuber2/Nomitron/