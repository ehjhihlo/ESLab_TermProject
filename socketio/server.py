import socketio
import eventlet
import numpy as np
import json
import cv2

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
    sio.emit('receive', 'photo received')

if __name__ == '__main__':
    port = 3000
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', port)), app)
    # print(f'Server is running on port {port}')
