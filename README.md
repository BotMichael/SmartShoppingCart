
Edge Computing System  
* Cloud_Server.py
* Fog.py
* Edge_Client_Send_RP1.py
* Edge_Client_Send_RP2.py

Process:  
1. start cloud
2. start fog
3. start edge device
    - RP1  
        * Detect Person to activate system 
        * User inputs ID and Password and 
        * Cloud confirms and returns path to users' favorite item (one item based on previous shopping history)
        * provide interactions  
            - user inputs `current location` + `item`
            - cloud returns `a list of regions from current pos to item's region`
    - RP2
        * [responsible for check-out]
        * wait cloud's signal
        * scan shopping cart
        * return list of items and count for each item
        
Current Merchandise List
* Data/Item_Region.txt

