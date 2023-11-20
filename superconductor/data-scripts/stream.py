from azure.iot.device import IoTHubDeviceClient, Message
import time
import json
import serial
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

arduino = serial.Serial('/dev/cu.usbmodem14301', 9600, timeout=1)
connection = os.getenv('CONNECTION_STRING')

def convert_line_to_dict(line):
    """
    Converting lines of data to a dictionary
    """
    values = line.split()
    keys = ["SC_volt", "Divd_volt", "Divd_ratio", "Therm_R", "Ref_Volt"]

    # Create a dictionary by zipping the keys with the corresponding values
    data_dict = dict(zip(keys, map(float, values)))

    return data_dict

def main():
    time.sleep(0.1)
    try:
        client = IoTHubDeviceClient.create_from_connection_string(connection)
        while True:
            incoming_line = arduino.readline()
            incoming_line = incoming_line.decode('utf-8')

            data = convert_line_to_dict(incoming_line)
            # additional data
            data['tag'] = 'test' # future implementation: stream.py -t

            if data != {}:
                message = Message(json.dumps(data))
                client.send_message(message)
                print("Message sent: {}".format(message))
                time.sleep(1)

    except KeyboardInterrupt:
        print()
        print("Arduino Device Stopped")

if __name__ == '__main__':
    print("STREAMING DATA TO AZURE IOT HUB")
    print("SC_volt, Divd_volt, Divd_ratio, Therm_R, Ref_Volt")
    main()
