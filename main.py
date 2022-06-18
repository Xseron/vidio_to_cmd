import os
import time
from sys import stdout
import threading
try:
  import cv2
  import numpy as np
  import moviepy.editor as mp
  from playsound import playsound
  from dotenv import dotenv_values
except:
  input("Install useful libs? \n press any key to install")
  os.system("pip install opencv-python moviepy playsound python-dotenv")
  import cv2
  import numpy as np
  import moviepy.editor as mp
  from playsound import playsound
  from dotenv import dotenv_values

config = dotenv_values("config.env")
vidio = config['vidio']
out_oudio = config['out_audio']

vidcap = cv2.VideoCapture(vidio)
my_clip = mp.VideoFileClip(vidio)
my_clip.audio.write_audiofile(out_oudio)
framespersecond= int(vidcap.get(cv2.CAP_PROP_FPS))
length = int(vidcap.get(cv2. CAP_PROP_FRAME_COUNT))
success,image = vidcap.read()

HEIGHT_CMD = int(config['HEIGHT_CMD'])
WIDTH_CMD = int(config['WIDTH_CMD'])

HEIGHT_VID = image.shape[0]
WIDTH_VID = image.shape[1]

HEIGHT_CHAR = int(HEIGHT_VID/HEIGHT_CMD)
WIDTH_CHAR = int(WIDTH_VID/WIDTH_CMD)

CHAR_SET = config['CHAR_SET']

res = []

count = 0
def play(href:str):
  playsound(href)
while success:
  print('\r'+'Загрузка '+str(count),'/'+str(length), end='')
  grayFrame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  a = np.zeros((HEIGHT_CMD,WIDTH_CMD),dtype='U')
  for i in range(0,grayFrame.shape[0],HEIGHT_CHAR):
    for j in range(0, grayFrame.shape[1],WIDTH_CHAR):
      t = grayFrame[i:i+HEIGHT_CHAR,j:j+WIDTH_CHAR]
      g = int(np.average(t)/int(256/len(CHAR_SET)))
      x = min(int(j/WIDTH_CHAR),WIDTH_CMD-1)
      y = min(int(i/HEIGHT_CHAR),HEIGHT_CMD-1)
      ch = CHAR_SET[len(CHAR_SET)-g-1]
      a[y,x] = ch
  g = []
  for i in a:
    g.append(''.join(i))
  res.append('\n'.join(g))
  success,image = vidcap.read()
  count += 1
input("\n PRESS ANY KEY")
os.system(f'mode con: cols={WIDTH_CMD} lines={HEIGHT_CMD}')
tr = threading.Thread(target=play,args=('./play.mp3',))
tr.start()
for i in res:
  time.sleep(1/framespersecond-0.001)
  stdout.write(i)
