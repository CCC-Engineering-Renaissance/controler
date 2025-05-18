import moto_proto_pb2
import socket

controller = moto_proto_pb2.ControllerInput()
thurst.A = 0.5

data = thurst.SerializeToString()

SERVER_IP = '192.168.8.117'  # or your server's IP
SERVER_PORT = 12345

# Create a UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2.0)  # Optional: timeout in seconds

# Send message to server
        while True:
            MESSAGE = data
            sock.sendto(MESSAGE, (SERVER_IP, SERVER_PORT))
#print(f"Sent: {MESSAGE}")

