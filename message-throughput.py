import time
import random
import threading
import zmq
import paho.mqtt.client as mqtt
import logging
logging.basicConfig(level=logging.DEBUG)

# MQTT Configuration
mqtt_broker_address = "127.0.0.1"
mqtt_topic = "benchmark"
mqtt_qos = 0
mqtt_msg_count = 10000

# ZeroMQ Configuration
zmq_msg_count = 10000

def mqtt_publisher():
    client = mqtt.Client()
    client.connect(mqtt_broker_address)
    for i in range(mqtt_msg_count):
        message = f"Message {i}"
        client.publish(mqtt_topic, message, qos=mqtt_qos)

def mqtt_subscriber():
    client = mqtt.Client()
    client.connect(mqtt_broker_address)
    client.subscribe(mqtt_topic, qos=mqtt_qos)
    client.on_message = lambda client, userdata, msg: print(f"Received: {msg.payload}")
    client.loop_start()

def zmq_publisher():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")
    for i in range(zmq_msg_count):
        message = f"Message {i}"
        socket.send_string(message)

def zmq_subscriber():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    for i in range(zmq_msg_count):
        message = socket.recv_string()
        print(f"Received: {message}")

if __name__ == "__main__":
    mqtt_pub_thread = threading.Thread(target=mqtt_publisher)
    mqtt_sub_thread = threading.Thread(target=mqtt_subscriber)
    zmq_pub_thread = threading.Thread(target=zmq_publisher)
    zmq_sub_thread = threading.Thread(target=zmq_subscriber)

    start_time = time.time()

    # Start MQTT and ZeroMQ threads
    mqtt_pub_thread.start()
    mqtt_sub_thread.start()
    zmq_pub_thread.start()
    zmq_sub_thread.start()

    # Wait for all threads to finish
    mqtt_pub_thread.join()
    mqtt_sub_thread.join()
    zmq_pub_thread.join()
    zmq_sub_thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Calculate throughput for both MQTT and ZeroMQ
    mqtt_throughput = mqtt_msg_count / elapsed_time
    zmq_throughput = zmq_msg_count / elapsed_time

    print(f"MQTT Throughput: {mqtt_throughput} messages per second")
    print(f"ZeroMQ Throughput: {zmq_throughput} messages per second")
