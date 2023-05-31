import cv2
import socket
import math
import pickle
import time

max_length = 1500
host = "127.0.0.1"
port = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
currentFrame = -1
while cap.isOpened():
	ret, frame = cap.read()
	cv2.imshow("Client", frame)
	retval, buffer = cv2.imencode(".jpg", frame)
	if retval:
		buffer = buffer.tobytes()
		buffer_size = len(buffer)

		num_of_packs = 1
        
		if buffer_size > max_length:
			num_of_packs = math.ceil(buffer_size/max_length)
		now = time.time() * 1000
		frame_info = {"packs":num_of_packs, "frame":currentFrame, "time":now}
		sock.sendto(pickle.dumps(frame_info), (host, port))
		
		left = 0
		right = max_length

		for i in range(num_of_packs):
			data = buffer[left:right]
			left = right
			right += max_length
			sock.sendto(data, (host, port))

	if cv2.waitKey(1) == ord('q'):
		break
	currentFrame += 1

cap.release()    
cv2.destroyWindow('Client')
