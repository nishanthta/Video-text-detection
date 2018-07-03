
import sys
import os

import cv2 as cv
import numpy as np

srcfile = '' #replace with source address  

cap = cv.VideoCapture(srcfile)

maxArea = 700*700 / 4
minCnt = 3000
maxCnt = 9000

fourcc = cv.VideoWriter_fourcc('M','P','E','G')
out = cv.VideoWriter('finalout.avi',fourcc, 20.0, (700,700))

cnt = 0

while(cap.isOpened()):

  ret,img = cap.read()

  cnt = cnt + 1
  print "frame ", cnt
  '''
  if cnt < minCnt:
    continue
  '''
  # for visualization
  vis = img.copy()

  textSpotter = cv.text.TextDetectorCNN_create("textbox.prototxt", "TextBoxes_icdar13.caffemodel")
  rects, outProbs = textSpotter.detect(img);
  vis = img.copy()
  thres = 0.045

  for r in range(np.shape(rects)[0]):
    if outProbs[r] > thres: #check if rectangle is above threshold
      rect = rects[r]
      ln = rect[2]
      br = rect[3]
      if ln*br < maxArea:
        rect[0] = rect[0] - int(ln/8)
        rect[1] = rect[1] - int(br/8)
        ln = ln + int(ln/4)
        br = br + int(br/3.5)
        cv.rectangle(vis, (rect[0],rect[1]), (rect[0] + ln, rect[1] + br), (255, 0, 0), 3)

  vis = cv.resize(vis,(700,700))
  #cv.imshow('video',vis)
  #cv.waitKey()
  if cnt%20 < 10:
    for i in range(cnt % 10):
      sys.stdout.write(" ")
  else:
    for i in range(10 - cnt % 10):
      sys.stdout.write(" ")
  out.write(vis)
  '''
  if cnt == maxCnt:
    break
  '''

  if cv.waitKey(1) and 0xFF == ord('q'):
    break 


cap.release()
out.release()
cv.DestroyAllWindows()
