import socketio

sio = socketio.Client()

@sio.event
def connect():
  print("I'm connected!")

@sio.on('test event')
def event(data):
  print(data)

if __name__ == '__main__':
  sio.connect('http://localhost:8000')