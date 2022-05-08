import cv2
import numpy as np
import time
import os
import testing as htm
import mss
from PIL import Image


brushThickness = 25
eraserThickness = 80

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=0.85,maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
with mss.mss() as sct:
    monitor = {'top': 0, 'left': 0, 'width': 1280, 'height': 720}
    
while True:

    
    sct_img = np.array(sct.grab(monitor))
    sct_img = cv2.cvtColor(sct_img, cv2.COLOR_BGR2RGB)
    

    # 1. Import image
    success, img = cap.read()
    
    img = cv2.flip(img, 1)
    
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        
        #print(lmList)
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

    
        fingers = detector.fingersUp()
        #print(fingers)

        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)       
            print("Selection Mode")
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (233,255,50)
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

           
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness) 
            xp, yp = x1, y1

  
    img[0:125, 0:1280] = header
    
    width = int(imgCanvas.shape[1])
    height = int(imgCanvas.shape[0])
    
    dim = (width, height)
    sct_img = cv2.resize(sct_img, dim,interpolation = cv2.INTER_CUBIC)
   
    sct_img = cv2.addWeighted(sct_img,0.5,imgCanvas,0.5,0.0)
    cv2.imshow("screen",sct_img)
    cv2.imshow("Image", img)
    cv2.namedWindow('Resize',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Resize', 300,300)
    cv2.imshow('Resize',img)
        
    

    if cv2.waitKey(1)==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()