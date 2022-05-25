# import cv2
# import numpy as np
# import pyautogui

# # cam = cv2.VideoCapture(0)

# while True:
#   # ret, frame = cam.read()
#   frame = pyautogui.screenshot()
#   size = frame.size()
#   frame = size.resize((100, 100))
#   src = np.array(frame)
#   src = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)
#   cv2.imshow('result', src)
#   if cv2.waitKey(1) == 27:
#     break

# cv2.destroyAllWindows()

import pyautogui
import cv2
import numpy as np

while True:
  frame = pyautogui.screenshot()
  frame = frame.resize((600, 350))
  frame = np.array(frame)
  frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
  cv2.imshow('result', frame)
  if cv2.waitKey(1) == 27:
    break

cv2.destroyAllWindows()