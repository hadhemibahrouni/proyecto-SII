import time
import random
import string
import paho.mqtt.client as mqtt

# MQTT broker settings
mqtt_broker = "127.0.0.1"
mqtt_port = 1883

# Number of messages to publish
num_messages = 1000

# Message payload (256 bytes)
message_payload = ''.join(random.choice(string.ascii_letters) for _ in range(256))

# MQTT client setup
client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port)

# Callback when a message is published
def on_publish(client, userdata, mid):
    if mid == num_messages:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Published {num_messages} messages in {elapsed_time:.2f} seconds.")
        client.disconnect()

client.on_publish = on_publish

start_time = time.time()
for i in range(1, num_messages + 1):
    client.publish("test/topic", message_payload, qos=1)

client.loop_forever()

