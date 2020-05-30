Edge Computing System  

For each device, only need to download the corresponding directory.

<br>├── src
<br>│   ├── cloud
<br>│   │   ├── log
<br>│   │   │   ├── logger.py
<br>│   │   │   ├── Cloud.log
<br>│   │   ├── data
<br>│   │   │   ├── Account.txt
<br>│   │   │   ├── Item_Region.txt
<br>│   │   │   └── Price.txt
<br>│   │   ├── Cloud_Computation.py
<br>│   │   ├── Cloud_DataParser.py
<br>│   │   └── Cloud_server.py
<br>│   │   └── get_path.py
<br>│   │   └── generate_key.py
<br>│   │   └── requirements.txt
<br>│   └── fog
<br>│   │   ├── log
<br>│   │   │   ├── logger.py
<br>│   │   │   ├── Fog.log
<br>│   │   ├── Fog.py
<br>│   │   ├── Global_Var.py
<br>│   │   └── requirements.txt
<br>│   └── edge
<br>│       ├── rpi1
<br>│       │   ├── log
<br>│       │   │   ├── logger.py
<br>│       │   │   ├── Edge_rpi1_000.log
<br>│       │   ├── Sample_TFLite_model
<br>│       │   │   ├── detect.tflite
<br>│       │   │   └── labelmap.txt
<br>│       │   ├── Edge_Client_Interface.py
<br>│       │   ├── Global_Var.py
<br>│       │   ├── TFLite_detection_face.py
<br>│       │   ├── requirements.txt
<br>│       ├── rpi2
<br>│           ├── log
<br>│           │   ├── logger.py
<br>│           │   ├── Edge_rpi2_000.log
<br>│           ├── Sample_TFLite_model
<br>│           │   ├── detect.tflite
<br>│           │   └── labelmap.txt
<br>│           ├── Edge_Client_Interface.py
<br>│           ├── Global_Var.py
<br>│           └── TFLite_detection_image.py
<br>│           └── requirements.txt
<br>├── test
<br>│   └── Edge_Client_test.py
<br>│       ├── Item_Region.txt
<br>│       └── Price.txt
<br>├── Cloud_Server.py
<br>├── Edge_Client_Send_RP1.py
<br>├── Edge_Client_Send_RP2.py
<br>├── Fog.py
<br>├── Global_Var.py
<br>└── README.md



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
﹞5.29
- refactory structure

+++++++++++++++++++++++++
﹞5.21 
- Update server model and message transmission
