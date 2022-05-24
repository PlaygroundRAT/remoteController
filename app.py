import socketio
from pyfiglet import Figlet
import os

f = Figlet(font='slant')

cls = lambda: os.system('cls' if os.name=='nt' else 'clear')

sio = socketio.Client()

target = {}
isWhile = True


def showMenu():
  print(f.renderText('Remote Controller'))
  print("1. set target")
  print("2. remote") if target else ''
  print("\nexit. exit")
  print(f"\n\ntarget : [ {target['ip']} | {target['os']} | {target['name']} ]") if target else ''

def main():
  cls()
  global isWhile
  global target
  while isWhile:
    cls()
    showMenu()
    print("\n>> ", end='')
    a = input()
    if a == '1':
      showTargetList()
    elif a == 'exit':
      sio.disconnect()
      exit()
    # elif a == '2':
    #   print("개발중..")




# 감염된 pc 정보들 가져오기
def showTargetList():
  global isWhile
  isWhile = False
  sio.emit('target list')
@sio.on('t list')
def getTargetLlist(data):
  global isWhile
  w = True
  cls()
  print(f.renderText('Targets'))
  print("\n\n")
  for i, v in enumerate(data['targets']):
    print(f"{i+1}. {v['ip']} | {v['os']} | {v['name']}")
  print("\n999. exit\n\n")
  while w:
    print(">> ", end='')
    st = int(input())
    if st == 999:
      isWhile = True
      main()
    if st > len(data['targets']):
      print("The number passed.")
      continue
    else:
      w = False
    
    global target
    target = data['targets'][st-1]
  isWhile = True
  main()

# 타겟이 연결 끊길 때
@sio.on('del target')
def delTarget(data):
  global target
  if target['sid'] == data['sid']:
    target  = {}

@sio.event
def connect():
  main()

if __name__ == '__main__':
  sio.connect('http://localhost:8000')