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

flag = 0
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
    print("result:",data)
    if data==True:
        ch = dev.getCharacteristics(uuid=UUID(0xA001))[0]
        ch.write(b"\x01")

#server_address = "http://192.168.11.12:3000"
server_address = "http://192.168.0.186:3000"
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
        print('flag = ', flag)
    
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


# number = input('Enter your device number: ')
# print ('Device', number)
# num = int(number)
# print (addr[num])
#

#Instantiate and configure picamera 
#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 32
#raw_capture = PiRGBArray(camera, size=(640, 480))

#let camera module warm up 
#time.sleep(0.1)

# define an OpenCV window to display  video
#cv2.namedWindow("Frame")

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
#for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    #for ch in dev.getCharacteristics(uuid=UUID(0xfff4)):
        # ch.write('52399254'.encode('utf-8'))
    #image = frame.array
    #cv2.imshow("Frame", image)
    #key = cv2.waitKey(1) & 0xFF
    #raw_capture.truncate(0)
    #if 'q' is pressed, close OpenCV window and end video
    #if key != ord('q'):
        #pass
    #else:
        #cv2.destroyAllWindows()
        #break
    
    dev.setDelegate(NewDelegate())

    print("writing done")
    if dev.waitForNotifications(1.0):
        #ch.write('44444'.encode('utf-8'))
        # handleNotification() was called
        print("write notify")
        #print(flag)
        #if flag == 1:
            #cv2.imwrite("image.png", image)

        # pseudo for testing write characteristic to server
        # ch = dev.getCharacteristics(uuid=UUID(0xA001))[0]
        # # print(ch)
        # ch.write(b"\x01")
        # #print('write 1 to stm')
        
        #ch = dev.getCharacteristics(uuid=UUID(0xfff4))[0]
        #if (ch.supportsRead()):
        #print(ch.read())
    print("waiting")

sio.disconnect()
#finally:
    #dev.disconnect() 
