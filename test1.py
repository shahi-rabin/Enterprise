

import requests
import json
import paho.mqtt.client as mqtt
import time

# Replace with your actual Firebase Realtime Database URL
database_url = "https://smart-city-de866-default-rtdb.firebaseio.com"

# Replace with your actual API key
api_key = "YOUR_FIREBASE_API_KEY"

# Endpoint to access the Firebase Realtime Database
url = f"{database_url}/.json?auth={api_key}"

# Replace with your ThingsBoard MQTT broker and access tokens for each entity group
thingsboard_broker = "localhost"  # Use "localhost" if running on the same machine
access_tokens = {
    "area_one": "X3P7IpVYfhEhbw5CzbGg",
    "parking": "MxitM89ycNPS5gVVw8ks",
    "area_two": "4BmFDSXqfJQVSYzexMK6",
    # Add more entity groups and their access tokens as needed
}

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with result code " + str(rc))

def send_to_thingsboard(token, telemetry_data):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.username_pw_set(token)
    client.connect(thingsboard_broker, 1883, 60)
    client.loop_start()

    client.publish(f"v1/devices/me/telemetry", json.dumps(telemetry_data))
    print(f"Data sent to ThingsBoard via MQTT for device with token {token}")

    client.loop_stop()
    client.disconnect()

try:
    while True:
        response = requests.get(url)
        data = response.json()

        # Print the data in a structured manner
        for area, area_data in data.items():
            print(f"--- {area} ---")
            for key, value in area_data.items():
                print(f"{key}: {value}")

            # Send the data to ThingsBoard for each entity group
            if area in access_tokens:
                token = access_tokens[area]
                send_to_thingsboard(token, area_data)

            print()  # Add an empty line between entity groups

        time.sleep(5)  # Adjust the interval (in seconds) between requests

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Script interrupted.")
