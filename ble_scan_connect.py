from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle
import struct
import json

import picamera
from picamera.array import PiRGBArray 
from picamera import PiCamera 
import time 
import cv2
global PictureNum
PictureNum = 1

import socketio
import cv2
import base64


global dev
#global alert

flag = 0
alert="false"
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server")

@sio.event
def disconnect():
    print("Disconnected from the server")

@sio.event
def receive(data):
    global alert
    print("result:",data)
    alert = data

#server_address = "http://192.168.11.12:3000"
server_address = "http://192.168.0.138:3000"
sio.connect(server_address)


class NewDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, handle, data):

        data = struct.unpack('<h', data)[0]/(2**8)       
        print(f"Notification, handle: {handle}, data:{data}")
        if data == 1:
            flag = 1
            print("human detected!!")
            time.sleep(0.1)
            global PictureNum
            with picamera.PiCamera() as camera:
                camera.capture('detect_faces/image'+str(PictureNum)+'.jpg')
                PictureNum = 1
            img = cv2.imread('detect_faces/image'+str(PictureNum)+'.jpg')
            img = cv2.resize(img, (160, 160), interpolation=cv2.INTER_AREA)
            img_json = json.dumps(img.tolist())
            sio.emit("image", img_json)
        else:
            flag = 0
        #print('flag = ', flag)
    
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(3.0)

n=0
addr = []
num = -1
for dev in devices:
    print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print (" %s = %s" % (desc, value))
        if (value=='EnJhih' and desc=='Complete Local Name'):
            num = n-1
            break
    if (num != -1):
        break
assert(num!=-1)


print ("Connecting...")
dev = Peripheral(addr[num], 'random')
#
print ("Services...")
for svc in dev.services:
    print (str(svc))
#
setup_data = b"\x01\x00"
notify = dev.getCharacteristics(uuid=0x2a37)[0]
notify_handle = notify.getHandle() + 1
dev.writeCharacteristic(notify_handle, setup_data, withResponse=True)

while True:
    dev.setDelegate(NewDelegate())
    print(alert)
    if alert=="true":
        ch = dev.getCharacteristics(uuid=UUID(0xA001))[0]
        ch.write(b"\x01")
        print("hewlqwhrejlqwh")
        alert = "false"
    #print("writing done")
    if dev.waitForNotifications(1.0):
        print(" ")

    print("waiting")

sio.disconnect()
