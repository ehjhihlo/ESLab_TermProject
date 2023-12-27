import socketio
import eventlet
import numpy as np
import json
import cv2
import sys
import os
import threading
import time
from faceRecognizer import FaceRecognition

sio = socketio.Server()
app = socketio.WSGIApp(sio)

count = 0

@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

# @sio.event
# def image(sid, data):
#     print(f'Received image from rpi: {data}')
#     img = np.fromstring(data, dtype=int)
#     print(img)
#     img = img.reshape((160, 160))
#     print(img)

@sio.event
def image(sid, data):
    global count
    print(f'Received image from rpi!!!')
    img = np.array(json.loads(data))
    count += 1
    # print(img)
    # print(img.shape)
    cv2.imwrite(f"./images/img_{count}.png", img)
    print(f'image {count} saved!!')
    alert = FaceRecognition(f"./images/img_{count}.png")
    print("alert: ", alert)
    sio.emit('receive', json.dumps(alert))


@sio.event
def register_database_image(sid, data):
    print(data)
    print(f'register new image to database!!!')
    # Load the JSON data
    data_load = json.loads(data)[0]
    # Extract information from the loaded data
    name = data_load["name"]
    img = np.array(data_load["image"])
    # Create a directory for the authorized face if it doesn't exist
    try:
        os.makedirs('./faceRecognition/authorized_face/' + name)
    except:
        pass
    # Save the image to the specified path
    cv2.imwrite(f'./faceRecognition/authorized_face/{name}/1.png', img)
    print(f'new image: {name} saved in database!!')



# # 子執行緒的工作函數
# def job():
#   for i in range(15):
#     print("Child thread:", i)
#     time.sleep(1)

# # 建立一個子執行緒
# t = threading.Thread(target = job)





if __name__ == '__main__':
    try:
        os.mkdir('./images')
    except:
        pass
    port = 3000
    
    # # 執行該子執行緒
    # t.start()
    
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', port)), app)
    # print(f'Server is running on port {port}')
    
    # t.join()
