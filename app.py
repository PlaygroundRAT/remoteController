import socketio
from pyfiglet import Figlet
import os

f = Figlet(font='slant')

cls = lambda: os.system('cls' if os.name=='nt' else 'clear')

sio = socketio.Client()

@sio.event
def connect():
  cls()
  print(f.renderText('Remote Controller'))
  while True:
    a = input(">> ")
    if a == 'a':
      sio.emit('test event', {'hello': 'world'})

if __name__ == '__main__':
  sio.connect('http://localhost:8000')