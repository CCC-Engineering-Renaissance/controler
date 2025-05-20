import socket
import cv2
import numpy as np

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('192.168.8.161', 5005))

while True:
    packet, _ = sock.recvfrom(65536)
    print(packet)
    img = cv2.imdecode(np.frombuffer(packet, dtype=np.uint8), 1)
    img = cv2.resize(img, (720, 720))
    if img is not None:
        cv2.imshow('Video', img)
    if cv2.waitKey(20) == ord('q'):
        break
