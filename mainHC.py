import cv2 as cv
import numpy as np
from time import time
from windowcaptureHC import WindowCapture
import ctypes #needed to fix dpi scaling
from visionHC import visionHC


#use this to make the script dpi aware so the scaling of the capture will be fixed
ctypes.windll.shcore.SetProcessDpiAwareness(1)


#create window capture instance, pass to constructor name of window to capture
wincap = WindowCapture('Half-Life')

#load trained cascade classifier and save to variable
cascade_headcrab = cv.CascadeClassifier('cascade/cascade.xml')

#load an empty instance of visionHC class
vision_headcrab = visionHC(None)
#call ist window names to print all names of windows open
#wincap.list_window_names()

loop_time = time()
while (True):
    
    #update the image of the game
    screenshot = wincap.get_screenshot()

    #handle object detection. this uses the trained model to look at the screenshot and return 
    #list of rectangles with all the found objects
    rectangles = cascade_headcrab.detectMultiScale(screenshot)

    #draw the detection rectangles on the origninal image
    detection_image = vision_headcrab.draw_rectangles(screenshot, rectangles)
 

    cv.imshow('Matches', detection_image)


    #this will give us the fps by timing how long through each loop
    #print('FPS{}'.format(1/(time() - loop_time)))      #to output as fps need to devide one second by how long it took for each loop to get fps
    loop_time = time()

    #wait 1 ms every loop to prqocess key presses
    key = cv.waitKey(1)

    #press q with output window focused to exit
    if key == ord('q'):   #if caps lock is on this will not work
        cv.destroyAllWindows()
        break
    elif key == ord('e'):    #press e to save image in positve
        cv.imwrite('positive/{}.jpg'.format(loop_time),screenshot)   #loop time makes sure file names are unique
    elif key ==ord('c'):     #press c to save image in negative
        cv.imwrite('negative/{}.jpg'.format(loop_time),screenshot)

        

print('DONE')
    