Edge Computing System  
©À©¤©¤ data
©¦   ©À©¤©¤ Account.txt
©¦   ©À©¤©¤ Item_Region.txt
©¦   ©¸©¤©¤ Price.txt
©À©¤©¤ src
©¦   ©À©¤©¤ cloud
©¦   ©¦   ©À©¤©¤ Cloud_Computation.py
©¦   ©¦   ©À©¤©¤ Cloud_DataParser.py
©¦   ©¦   ©¸©¤©¤ get_path.py
©¦   ©¸©¤©¤ edge
©¦       ©À©¤©¤ Sample_TFLite_model
©¦       ©¦   ©À©¤©¤ detect.tflite
©¦       ©¦   ©¸©¤©¤ labelmap.txt
©¦       ©À©¤©¤ Edge_Client_Interface.py
©¦       ©À©¤©¤ TFLite_detection_face.py
©¦       ©¸©¤©¤ TFLite_detection_image.py
©À©¤©¤ test
©¦   ©¸©¤©¤ Edge_Client_test.py
©¦       ©À©¤©¤ Item_Region.txt
©¦       ©¸©¤©¤ Price.txt
©À©¤©¤ Cloud_Server.py
©À©¤©¤ Edge_Client_Send_RP1.py
©À©¤©¤ Edge_Client_Send_RP2.py
©À©¤©¤ Fog.py
©À©¤©¤ Global_Var.py
©¸©¤©¤ README.md


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
* data/Item_Region.txt

+++++++++++++++++++++++++
¡¤5.21 
- Update server model and message transmission
