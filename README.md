##Bluetooth LE Scanner and MQTT Listener

This project contains two Python scripts: scan.py and listening.py.
The scan.py script scans for Bluetooth Low Energy (BLE) devices using a Bluetooth adapter connected to the PC, and sends the information to an MQTT broker.
The listening.py script subscribes to the MQTT topic, receives the information, and writes it to a file.

###Requirements:
Python 3.x
simplepyble
paho-mqtt

You can install the required libraries using pip:

pip install simplepyble paho-mqtt

##Files:

"scan.py"
Scans for Bluetooth LE devices using the simplepyble library.
Stores the found devices' information in a dictionary.
Sends the information over a given MQTT broker using the paho-mqtt library.

###Configuration:
broker_address: The address of the MQTT broker.
port: The port number of the MQTT broker.
main_topic: The MQTT topic to publish the information.

"listening.py"
Subscribes to a given topic at the MQTT broker.
Stores the received information in a mqtt_data.txt file.
Terminates when the string "end!" is seen at the topic.

###Configuration:
broker_address: The address of the MQTT broker.
port: The port number of the MQTT broker.
topic: The MQTT topic to subscribe to.

##Usage:
Run the listening.py script to start listening to the MQTT topic and store the received information. It will terminate itself when the data sending is complete.

python listening.py

The listening.py script will terminate automatically when the string "end!" is received.

Run the scan.py script to start scanning for Bluetooth LE devices and send the information to the MQTT broker.

python scan.py

##License:
This project is licensed under the MIT License. See the LICENSE file for details.

##Contributing:
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.






