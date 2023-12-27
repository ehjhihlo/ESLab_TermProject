import socketio
import cv2
import json
import time
print("hi")
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
server_address = "http://192.168.0.138:3000"
sio.connect(server_address)

cap = cv2.VideoCapture(0)
data = []
person = {}
name = input("please enter your name : ")

while True:
    # name = input("please enter your name : ")
    ret, frame = cap.read()

    cv2.imshow('frame', frame)

    k = cv2.waitKey(0)

    if k == ord('s') :
        # cv2.imwrite('img.png', frame)
        img = cv2.resize(frame, (160, 160), interpolation=cv2.INTER_AREA)
        person["name"] = name
        person["image"] = img.tolist()
        data.append(person)
        sio.emit('register_database_image', json.dumps(data))
        time.sleep(2)
        print('Image sent to server!!')
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()