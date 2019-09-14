Hi. It looks like you need some help. Some commands are listed below.

Admin: Allowed Channels: actions, mod-lounge, bot-lounge
-    !newTurn:       Starts a new turn.

-    !newDay:        Forces newDay Actions.

-    !getData:       Sends The Data Pickle File

-    !ping:     ping bot for a response

-    !setColor @player $color
+       Set A Players Color
+       Rule: N/A
-    !getTile {coords}
+       Prints the tile Informations
+       Rule: N/A
-    !setTile {coords} @player $type $params
+       Set A Tile
+       $type is Claim, Capital, etc
+       params is a dictionary like:
+           {'Harvest': {'age':0, 'type':'Perpetual'}}
+       Rule: N/A
-    !remove $object
+       Remove A Player and all data from map, or remove a Tile
+       Rule: N/A
-    !resetTimer @player
+       if a player is given reset that player's timer
+       else reset all timers
+       Rule: N/A
-    !setTimer @player
+       if a player is given disable that player's timer
+       else reset all timers
+       Rule: N/A
-    !give {list @player} #count $item
+       give players # count of $item
+        #count can be deciaml and negative
+       Rule: N/A
-    !pause
+       toggles Pause State.
+       pause stops all player commands 
+       admin commands may be executed
-    !subtractTurn
+       subtracts one from every age counter in Harvest Tiles
-    !mark {coords} @player $marker
+       Marks a tile with marker
+       use "" for letters. Refer to Docs otherwise
-    !newUnit $name {dict}
+       Creates new Unit. Leave blank to get example.
-    !adjust item1 item2... to {'increasing', 'static', 'decreasing'}
+       sets items in Fed to velocity
-    !setTerm #Num
+       Sets Fed Term to whatever. 5 is limit,



This Bot's Code May Be Found At:
https://github.com/wmhuber2/Nomitron/