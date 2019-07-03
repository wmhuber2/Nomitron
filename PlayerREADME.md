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
-   !find "text" OR !search "text"
+        Allowed Channels: ALL            
+        Display rules that contain text.
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
+        Allowed Channels: ALL excluding Actions
+        Display Current Map.
+        Rule: 312


+###########################################
-  !admin
-     This will post the ADMIN help screen
+###########################################
This Bot's Code May Be Found At:
https://github.com/wmhuber2/Nomitron/