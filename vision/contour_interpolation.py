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
    image = cv2.imread("yeetest.jpg")

    if image is not None: 
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    else:
        print("no image")
    
    
    #edge detection + filtering

    edges= cv2.Canny(gray,30,200)

    #contour detection

    contours, hierarchy= cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image,contours,-1,(255,0,0),2)  

    #output of findContours is a little weird so have to extract the points values from the array like this

    contours = contours[0]
    new = np.array(contours)

    j = 0

    #place first value of contours into output array

    fin = np.array([[new[0, 0, 0], new[0, 0, 1]]])

    for i in range(len(new)-1):
        
        #add while loop to make this part recursive in the future
        #This part of the code looks to see if points are too far away and linearly interpolates points between them

        if (np.sqrt((new[i+1, 0, 0] - new[j, 0, 0])**2 + (new[i+1, 0, 1] - new[j, 0, 1])**2) > 50):
            fin = np.append(fin, [[(new[i+1, 0, 0]+new[j, 0, 0])/2, (new[i+1, 0, 1]+new[j, 0, 1])/2]], axis = 0)
            
        #This part of the code filters out additional points that are too close together, make inequality value bigger
        #to have more space
        if (np.sqrt((new[i+1, 0, 0] - new[j, 0, 0])**2 + (new[i+1, 0, 1] - new[j, 0, 1])**2) > 30):
            fin = np.append(fin, [[new[i+1, 0, 0], new[i+1, 0, 1]]], axis = 0)
            j=i+1

    #find a way to only implement on closed shapes  
    #right now this code adds a final point between first and last values to not fuck up squares
    if (np.sqrt((new[len(new)-1, 0, 0] - new[0, 0, 0])**2 + (new[len(new)-1, 0, 1] - new[0, 0, 1])**2) > 50):
            fin = np.append(fin, [[(new[len(new)-1, 0, 0]+new[0, 0, 0])/2, (new[len(new)-1, 0, 1]+new[0, 0, 1])/2]], axis = 0)   
        
    #fin is now the matrix that contains the necessary points output to confir everything working  
    plt.figure()
    plt.imshow(image)  
    plt.scatter(fin[:, 0], fin[:, 1])
    plt.show()

    else:
        print('retake image')
    
    #serial communication of line matrix
        
    [row,col] = fin.shape
    print('row', row)
    print('col', col)

    for i in range(row):
        for j in range(col):
            num = str(fin[i,j])
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






