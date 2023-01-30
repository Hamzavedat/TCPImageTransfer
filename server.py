import socket
import cv2
import numpy as np
import base64
import time 
import threading
Soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
port = 2344
Buffer_Boyutu = 24576180
Buffer_Boyutu2 = 0
Soket.connect(('192.168.43.5',port))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
kayit = cv2.VideoWriter('kayit.avi',fourcc,2.50,(640,480))
image2 = np.zeros(shape=[480, 640, 3], dtype=np.uint8)
str_img = ''
str_img2 = ''
x = 0
a = 0
size = ['','','','','','','','','','','']
size2 = ['','','','','','','','','','','']

def show():
	while True:
		global str_img2,Buffer_Boyutu2,image2,a,size2
		x = 0
		y = 0
		while len(str_img2) == Buffer_Boyutu2 and Buffer_Boyutu2 != 0:
			while y != 10:	
				image = base64.b64decode(str_img2[x + 2:(x + 2 + int(size2[y]) )])
				file_bytes = np.fromstring(image, dtype=np.uint8)
				image2 = cv2.imdecode(file_bytes, 1)
				kayit.write(image2)
				cv2.imshow('goruntu', image2)
				cv2.waitKey(400)
				x += int(size2[y]) + 3
				y += 1
			str_img2 = ''
			a += 1
			if a == 10:
				kayit.release()	
				cv2.destroyAllWindows()
				Soket.close()
				exit()

thr_show = threading.Thread(target=show)
thr_show.start()

c = 0
while True:
	b = 0
	msg = ''
	while b != 11 and size[b] == '':
		while msg != '0':
			msg = Soket.recv(1).decode()
			if msg == '0':
				Soket.send('1'.encode())
				size[b] = Soket.recv(1024).decode()
				if size[b] != '':
					print('size')
					print(size[b])
					b += 1
					if b != 11:
						c += int(size[b - 1 ])
		msg = ''

	Buffer_Boyutu = int(size[10])
	print('Buffer_Boyutu')
	print(Buffer_Boyutu)
	Buffer_Boyutu2 = Buffer_Boyutu
	print('c')
	print(c)
	c = 0
	msg = ''
	for i in range(0,11):
		size2[i] = size[i]

	while msg != '1' :
		msg = Soket.recv(1).decode()
		while msg == '1' and str_img == '' :
			Soket.send('1'.encode())
			while len(str_img) != Buffer_Boyutu:
				str_img += Soket.recv(Buffer_Boyutu-len(str_img)).decode()
			if len(str_img) == Buffer_Boyutu:
				break
	print('str_img')
	print(len(str_img))
	while True:
		if str_img2 == '':
			str_img2 = str_img
			break
	str_img = ''
	for i in range(0,11):
		size[i] = ''