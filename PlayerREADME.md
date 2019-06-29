Hi. It looks like you need some help. Some commands are listed below.


Rules:
-   !rule $num  
+        Allowed Channels: ALL            
+        Diplay Rule Number $num if it exists.
+        Rule: N/A
-   !help
+        Allowed Channels: ALL            
+        Diplay This Help Text
+        Rule: N/A

Map:
-    !start {coordinates} {color name} 
+        Allowed Channels: actions
+        Add Capital to map at desired coordiantes (row,col order doesnt matter)
+        and declare your color.
+        Example: !start aj56 red, !start 6ca red
+        Rule: 312
-    !claim {coordinates} 
+        Allowed Channels: actions
+        Claim Coordinates
+        Example: !claim aj56, !claim 5ca, !claim ca5
+        Rule: 312
-    !harvest {coordinates} {mode}
+        mode may be any of the following: ['perpetual', 'non-perpetual', 'p', 'n']
+        Allowed Channels: actions
+        Allows You to harvest a location you own.
+        Example: !harvest aj56 p, !harvest 5ca perpetual, !harvest ca5 n
+        Rule: 314
-    !map
+        Allowed Channels: ALL 
+        Display Current Map.
+        Rule: 312


Admin:
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
-    !setTile {coords} ..stuff (Eh Not Finished)
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       Set A Tile
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
-    !give @player #count $item
+       Allowed Channels: actions, mod-lounge, bot-lounge
+       give play er# count of $item
+        #count can be deciaml and negative
+       Rule: N/A

This Bot's Code May Be Found At:
https://github.com/wmhuber2/Nomitron/