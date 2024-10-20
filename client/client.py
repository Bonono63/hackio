import subprocess
import socket
import struct

log_file = open("log.txt", 'w')

def log(string):
    print(string)
    log_file.write(string)

log("HackI/O video client")

log("taking the photo")
process = subprocess.Popen(
        ['libcamera-still', '--saturation', '0', '--denoising', 'off', '--height', '480', '--width', '640', '-encoding', 'png', '-o', '-'],
        stdout=subprocess.PIPE,
        stderr=log_file
        ) 

log("photo finished")
image_data, error = process.communicate()

log("outputting image")
out_file = open("out.png", 'wb')
out_file.write(image_data)

#server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## Find a way to read these from a file or something
#server_ip = '192.168.1.252'
#port = 567
## create the socket in the OS
#server_socket.bind((server_ip, port))
#server_socket.listen(10)
#print("socket bound on {server_ip} on port {port} and listening")
#
## connect to client
#client_socket, client_address = server_socket.accept()
#print(f"[*] Accepted connection from {client_address}")
#
## read until it recieves a certain output
#while True:
#    ret, frame = video_capture.read()
#    serialized_frame = pickle.dumps(frame)
#    message_size = struct.pack("L", len(serialized_frame))
#    client_socket.sendall(message_size + serialized_frame)
#    cv2.imshow('Server Video', frame)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#
## release resources
#video_capture.release()
#cv2.destroyAllWindows()
