from socketio import Server, WSGIApp

sio = Server()
app = WSGIApp(sio)

@sio.event
def connect(sid, environ, auth):
  print('connect ', sid)

@sio.event
def disconnect(sid):
  print('disconnect ', sid)

@sio.on('test event')
def testEvent(sid, data):
  sio.emit('test event', data)