Hi. It looks like you need some help. Some commands are listed below.

Global Commands: Allowed Channels: ALL   
-   !rule $num          
+        Diplay Rule Number $num if it exists.
-   !help       
+        Diplay This Help Text
-   !find "text" OR !search "text" OR !f "text" 
+        Display rules that contain text.

ActionCommands:        Allowed Channels: actions
-    !start {coordinates} {color name} 
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
+        Allows You to harvest a location you own.
+        Example: !harvest aj56 p, !harvest 5ca perpetual, !harvest ca5 n
+        Rule: 314
-    !map
+        Display Current Map.
+        Rule: 312
-    !unit {coords} $name
+        Buy Unit and place at coords
+        Rule: 320
-    !move {coord1} {coord2}
+        move unit form coord1 to coord2
+        Rule: 320
-    !toggle {coord}
+         disables/enables output of a unit.
+         Rule 321
-    !trade @player amount item
+         give a player resources if they accept.
+         Rule 314


+###########################################
-  !admin
-     This will post the ADMIN help screen
+###########################################
This Bot's Code May Be Found At:
https://github.com/wmhuber2/Nomitron/