Edge Computing System for smart shopping cart system

For each device, only need to download the corresponding directory

Outline:
<br>├── src
<br>│   ├── cloud
<br>│   │   ├── log
<br>│   │   ├── data
<br>│   │   └── Cloud_server.py
<br>│   │   └── requirements.txt
<br>│   └── fog
<br>│   │   ├── log
<br>│   │   ├── Fog.py
<br>│   │   └── requirements.txt
<br>│   └── edge
<br>│       ├── rpi1
<br>│       │   ├── log
<br>│       │   ├── main.py
<br>│       │   ├── requirements.txt
<br>│       ├── rpi2
<br>│           ├── log
<br>│           ├── Edge_Client_RP2.py
<br>│           └── requirements.txt
<br>└── README.md



Process:  
1. start cloud
    ```python3 Cloud_server.py```
2. start fog
    ```python3 fog.py```
3. start edge device
    - RP1  
        * Detect Person to activate system 
        * User inputs ID and Password and 
        * Cloud confirms and returns price & region info for price
        * provide interactions  
        ```python3 main.py```
    - RP2
        * [responsible for check-out]
        * wait cloud's signal
        * scan shopping cart
        * return list of items and count for each item
        ```python3 Edge_Client_RP2.py```


+++++++++++++++++++++++++
﹞6.7 Version for submission

