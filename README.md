Edge Computing System  
Edge Computing System  
├── data
│   ├── Account.txt
<br>│   ├── Item_Region.txt

│   └── Price.txt

├── src

│   ├── cloud

│   │   ├── Cloud_Computation.py

│   │   ├── Cloud_DataParser.py

│   │   └── get_path.py

│   └── edge

│       ├── Sample_TFLite_model

│       │   ├── detect.tflite

│       │   └── labelmap.txt

│       ├── Edge_Client_Interface.py

│       ├── TFLite_detection_face.py

│       └── TFLite_detection_image.py

├── test

│   └── Edge_Client_test.py

│       ├── Item_Region.txt

│       └── Price.txt

├── Cloud_Server.py

├── Edge_Client_Send_RP1.py

├── Edge_Client_Send_RP2.py

├── Fog.py

├── Global_Var.py

└── README.md



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
﹞5.21 
- Update server model and message transmission
