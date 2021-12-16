import numpy as np
import cv2
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import serial
import time
import os

#serial shit

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def main():
    
    #camera shit
    
    os.system('fswebcam --no-banner -r 320x240 -S 3 --jpeg 50 --save /home/pi/Desktop/yeetest.jpg')
    frame = cv2.imread("yeetest.jpg")

    if frame is not None: 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    else:
        print("no image")
    
    # filter for dark pixels only
    
    pixels = np.argwhere(gray < 100)
    
    # remove x axis duplicates
    
    mylist=np.unique(pixels,axis=0)
    
    if mylist.size > 0:

        x = (mylist[:, 1])

        y = (mylist[:, 0])
        
        # Interpolate with scipy
        
        f = interp1d(x, y)
        xnew = np.linspace(min(x)+1, max(x)-1)
        
        xmat = np.linspace(min(x)+1, max(x)-1, num = 20)
        ymat = np.array(f(xmat))
        
        yeet = np.column_stack((xmat, ymat))
        yeet2 = yeet.astype(int)
        print (yeet2)
        
        plt.figure()
        plt.imshow(frame)
        plt.scatter(yeet2[:,0], yeet2[:,1])
        plt.show()
        
        
    
    else:
        print('retake image')
    
    #serial communication of line matrix
        
    [row,col] = yeet2.shape
    print('row', row)
    print('col', col)

    for i in range(row):
        for j in range(col):
            num = str(yeet2[i,j])
            print(num)
            print("-------")
            value = write_read(num)
            print('va', value)
            time.sleep(3)
     
    value = write_read(str(0))
    print(value)
    value = write_read(str(0))
    print(value)
        
    arduino.close()

main()






