Hi. It looks like you need some help. Some commands are listed below.

Global Commands: Allowed Channels: ALL   
-   !rule $num          
+        Display Rule Number $num if it exists.
-   !help       
+        Display This Help Text
-   !find "text" OR !search "text" OR !f "text" 
+        Display rules that contain text.
-   !map
+        Display Current Map.
+        Rule: 312

ActionCommands:        Allowed Channels: actions
-    !start {coordinates} {color name} 
+        Add Capital to map at desired coordiantes and declare your color.
+        (Rule: 312)
-    !claim {coordinates}
+        Claim Coordinates (Rule: 312)
-    !harvest {coordinates} {mode}
+        Harvests a location with this as mode ['perpetual', 'non-perpetual', 'p', 'n']
+        (Rule: 314)
-    !unit {coords} $name OR !unit
+        Buy Unit at coords, if just !unit, display all units (Rule: 321)
-    !move {coord1} {coord2}
+        move unit form coord1 to coord2 (Rule: 321)
-    !toggle {coord}
+         disables/enables output of a unit. (Rule 321)
-    !trade @player amount item
+         give a player resources if they accept. (Rule 314)
-    !asset + Proposal 351 formatting
+         Trade Tiles (Rule 351)
-    !sell #amount item
+         Sell at fed rate (Rule 351)
-    !raze @object {coord}
+         removes a object from map (See rule 360)

+###########################################
-  !admin
-     This will post the ADMIN help screen
+###########################################
This Bot's Code May Be Found At:
https://github.com/wmhuber2/Nomitron/