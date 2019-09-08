Hi. It looks like you need some help. Some commands are listed below.

Global Commands: Allowed Channels: ALL   
-   !rule $num          
+        Diplay Rule Number $num if it exists.
-   !help       
+        Diplay This Help Text
-   !find "text" OR !search "text" OR !f "text" 
+        Display rules that contain text.
-   !map
+        Display Current Map.
+        Rule: 312

ActionCommands:        Allowed Channels: actions
-    !start {coordinates} {color name} 
+        Add Capital to map at desired coordiantes and declare your color.
+        Rule: 312
-    !claim {coordinates}
+        Claim Coordinates
+        Example: !claim aj56, !claim 5ca, !claim ca5
+        Rule: 312
-    !harvest {coordinates} {mode}
+        Harvests a location with this as mode ['perpetual', 'non-perpetual', 'p', 'n']
+        Example: !harvest aj56 p, !harvest 5ca perpetual, !harvest ca5 n
+        Rule: 314
-    !unit {coords} $name OR !unit
+        Buy Unit and place at coords
+        if just !unit, then display all units
+        Rule: 321
-    !move {coord1} {coord2}
+        move unit form coord1 to coord2
+        Rule: 321
-    !toggle {coord}
+         disables/enables output of a unit.
+         Rule 321
-    !trade @player amount item
+         give a player resources if they accept.
+         Rule 314
-    !asset + Proposal 351 formatting
+         Trade Tiles
+         Rule 351

+###########################################
-  !admin
-     This will post the ADMIN help screen
+###########################################
This Bot's Code May Be Found At:
https://github.com/wmhuber2/Nomitron/