import time
import zmq

context = zmq.Context()

# Configuration
num_messages = 1000

# Create a PUB-SUB pair
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:5556")

sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:5556")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

# Start the benchmark
latencies = []

for _ in range(num_messages):
    message_time = time.time()
    pub_socket.send(str(message_time).encode("utf-8"))

    received_message = sub_socket.recv()
    received_time = time.time()
    latency = (received_time - message_time) * 1000  # Convert to milliseconds
    latencies.append(latency)

# Calculate and print statistics
average_latency = sum(latencies) / len(latencies)
min_latency = min(latencies)
max_latency = max(latencies)

print(f"Average Latency: {average_latency:.2f} ms")
print(f"Minimum Latency: {min_latency:.2f} ms")
print(f"Maximum Latency: {max_latency:.2f} ms")

# Clean up sockets
pub_socket.close()
sub_socket.close()

context.term()
