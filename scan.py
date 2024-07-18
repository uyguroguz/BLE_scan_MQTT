import simplepyble
from dataclasses import dataclass
import paho.mqtt.client as mqtt
import time


broker_address = "localhost"
port = 1883
client_id = "Bluetooth LE Scan Results"
main_topic = "scan_result"

def Merge(dict1, dict2): 
    res = dict1 | dict2
    return res

def on_message(client, userdata, message):
    print("message sent", str(message.payload.decode("utf-8")))
    print("message topic:", str(message.topic))
    print("message qos:", str(message.qos))
    print("message flag:", str(message.retain))
    print("\n")

client =mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
client.on_message = on_message


devices = {}

if __name__ == "__main__":
    adapters = simplepyble.Adapter.get_adapters()

    if len(adapters) == 0:
        print("No adapters found")

    # Query the user to pick an adapter
    print("Please select an adapter:")
    for i, adapter in enumerate(adapters):
        print(f"{i}: {adapter.identifier()} [{adapter.address()}]")

    choice = int(input("Enter choice: "))
    adapter = adapters[choice]

    print(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")

    adapter.set_callback_on_scan_start(lambda: print("Scan started."))
    adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
    adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))
        
    # Scan for 5 seconds
    adapter.scan_for(5000)

    peripherals = adapter.scan_get_results()
    print("The following peripherals were found:")
    for peripheral in peripherals:
        connectable_str = "Connectable" if peripheral.is_connectable() else "Non-Connectable"
        print(f"{peripheral.identifier()} [{peripheral.address()}] - {connectable_str}")
        print(f'    Address Type: {peripheral.address_type()}')
        print(f'    Tx Power: {peripheral.tx_power()} dBm')
        time.sleep(0.01)
        devices[peripheral.address()] = {"address": peripheral.address(), "name": peripheral.identifier(), "connectable":connectable_str, "address_type":peripheral.address_type(), "tx_pwr":peripheral.tx_power()}

        

        manufacturer_data = peripheral.manufacturer_data()
        for manufacturer_id, value in manufacturer_data.items():
            if type(value) == bytes:
                value = value.hex()
            elif type(value) == dict:
                value = next(iter(value.values()))
            print(f"    Manufacturer ID: {manufacturer_id}")
            print(f"    Manufacturer data: {value}")
            devices[peripheral.address()] = Merge(devices[peripheral.address()], {"mnf_id": manufacturer_id, "mnf_data": value})

        services = peripheral.services()
        for service in services:
            if type(service.data()) == bytes:
                srv_data = service.data().hex()
            elif type(service.data()) == dict:
                srv_data = next(iter(service.data().values()))
            print(f"    Service UUID: {service.uuid()}")
            print(f"    Service data: {srv_data} \n")
            devices[peripheral.address()] = Merge(devices[peripheral.address()], {"srv_id": service.uuid(), "srv_data": srv_data})

print("scanning complete, dict of devices: \n")
print(devices)
print("\n usinq mqtt")
print("\n connecting to", broker_address, " as ", client_id)
client.connect(broker_address, port)

client.loop_start()
print("\n starting to send data \n")

for device_id, device_info in devices.items():
    client.publish(main_topic, "\n")
    for info in device_info:
        topic = f"{main_topic}/{device_id}/{info}"
        print(topic)
        if device_info[info] != "":
            print(str(device_info[info]))
            client.publish(topic ,str(device_info[info]))
            time.sleep(0.1)
            print("info sent \n")
client.publish(main_topic, "end!")
client.loop_stop()
print("DATA COMPLETE!")


    
        