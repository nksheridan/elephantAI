# DETER DEVICE
# this is test code for putting the deter device into server mode, and getting a message via bluetooth from the detection device, and
# then going ahead and playing scare sounds. You need to determine your MAC address. It is for the server in this case, so the MAC address
# of the deter device. You also need to pair the deter device with the detection device via Bluetooth prior to using this. You can do
# that from the Bluetooth icon in the Raspian GUI.

import socket
import time
import os
import random

hostMACaddress = 'xxx'
port = 9
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACaddress, port))
s.listen(backlog)

print("We are waiting for a message from the detection device to arrive via bluetooth!")

try:
	client, address = s.accept()
	data = client.recv(size)
	if data:
		print(data)
		client.send(data)
		#echo back
except:
	print("closing the socket")
	client.close()
	s.close()

message = str(data)
#convert the data received to a string
print(message)

if message == "b'yes_audio'":
	print("play scare sounds now")
	time.sleep(3)
	scare_sounds = ['aplay bees1.wav', 'aplay bees2.wav', aplay bees3.wav']
	i = 0
	while i <10:
		i = i+1
		to_play = random.choice(scare_sounds)
		print(to_play)
		os.system(to_play)

print("Finished scare. Now can message detection device, and await another message from it")
