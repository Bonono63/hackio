import cv2
import socket
import pickle
import struct

print("HackI/O video server")
print("Running CV2 verison: ", cv2.__version__)


connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Find a way to read these from a file or something
client_ip = '192.168.1.63'
port = 567
# create the socket in the OS
connection_socket.connect((client_pi, port))

received_data = b""
payload_size = struct.calcsize("L")

# read until it recieves a certain output
while True:
    while len(received_data) < payload_size:
        received_data += connection_socket.recv(4096)

    packed_msg_size = received_data[:payload_size]
    received_data = received_data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    
    while len(received_data) < msg_size:
        received_data += connection_socket.recv(4096)

    frame_data = received_data[:msg_size]
    received_data = received_data[msg_size:]

    received_frame = pickle.loads(frame_data)

    cv2.imshow('Client Video', received_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release resources
cv2.destroyAllWindows()
connection_socket.close()
