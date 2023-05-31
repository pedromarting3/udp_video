import cv2
import socket
import pickle
import numpy as np
import time

max_length = 1500
host = "127.0.0.1"
port = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

frame_info = 0
buffer = None
frame = None
frame_anterior = -1
frame_actual = 0
print("-> Waiting for client")

while True:
    data, address = sock.recvfrom(max_length)
    aux = str(data)
    if len(data) < 100 and aux[4] == "8":
        frame_info = pickle.loads(data)
        frame_anterior = frame_actual
        frame_actual = frame_info["frame"]
        if frame_info and frame_actual > frame_anterior:
            nums_of_packs = frame_info["packs"]
            print("-> Receiving package:")
            print("-> Packets received: ", nums_of_packs)
            print("-> Getting frame: ", frame_info["frame"])
            print("-> Jitter: ", (time.time() * 1000) - frame_info["time"])
            for i in range(nums_of_packs):
                data, address = sock.recvfrom(max_length)
                if i == 0:
                    buffer = data
                else:
                    buffer += data

            frame = np.frombuffer(buffer, dtype=np.uint8)
            frame = frame.reshape(frame.shape[0], 1)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            
            if frame is not None and type(frame) == np.ndarray:
                cv2.imshow("Server", frame)
                if cv2.waitKey(1) == 27:
                    break