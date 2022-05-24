import socketio
from requests import get
import socket
import platform

sio = socketio.Client()

@sio.event
def connect():
  print("I'm connected!")

@sio.on('info')
def myInfo():
  ip = get("https://api.ipify.org").text

  sio.emit('my info', {
    'name': socket.gethostname(),
    'ip': ip,
    'os': "mac" if platform.system() == "Darwin" else platform.system()
  })

if __name__ == '__main__':
  sio.connect('http://localhost:8000')