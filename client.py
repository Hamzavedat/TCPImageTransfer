import socket
import cv2
import threading
import time 
import base64

Soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
host = socket.gethostname()
port = 2344
#Buffer_Boyutu = 2360
Soket.bind(('127.0.0.1', port)) 
Soket.listen(20)
c,asa = Soket.accept()
c.send(''.encode())
kamera=cv2.VideoCapture(0)
kamera.set(cv2.CAP_PROP_FRAME_WIDTH,640)
kamera.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
 
cam = 1
image_save = {}
image = []
x = 0
z = 0
str_image = ''

def img_to_str(image):
	global str_image
	ret, buff = cv2.imencode('.jpg', image)
	c.send(str(len(base64.b64encode(buff))).encode())
	#print(base64.b64encode(buff))
	str_image += str(base64.b64encode(buff))



def capture():
	
	while True:
		global x, z, image, kamera, image_save
		while cam:
			ret,image=kamera.read()
			image_save[x] = image
			img_to_str(image)
			x += 1
			z += 1
			time.sleep(0.20)
def record():
	while True:
		global x, fourcc
		if x == 50:
			name = str(time.time())+'.avi'
			#print(name)
			kayit = cv2.VideoWriter(name,fourcc,5.00,(640,480))
			y = 0
			while y != 50:
				kayit.write(image_save[y])
				y += 1
			x = 0
			kayit.release()


thr_capture = threading.Thread(target=capture)
thr_capture.start()

thr_record = threading.Thread(target=record)
thr_record.start()
while True:

	if z == 20:		
		c.send(str(len(str_image)).encode())
		print(len(str_image))
		time.sleep(0.03)
		c.sendall(str_image.encode())
		#time.sleep(0.10)
		str_image = ''
		z = 0

Soket.close()

