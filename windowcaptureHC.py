import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:

    w = 0
    h = 0
    hwnd = None

    #constructor
    def __init__(self, window_name):

        #FindWindow allows us to get the image data from that window even if it is behind something else
        #get window name once in the constructor
        self.hwnd = win32gui.FindWindow(None, window_name)
        
        #through an exceptio if window not found
        if not self.hwnd:
            raise Exception('Window not found : {}'.format(window_name))

        #set width and height to size of screen
        #self.w = 1920
        #self.h = 1080

        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        print('here is the width: {}'.format(self.w))
        print('here is the height: {}'.format(self.h))

        #get the exact size of the app window and set it as size
        #window_rect = win32gui.GetWindowRect(self.hwnd)   #returns the coords of the window being captured wiht 4 numbers
        #self.w = window_rect[0] - window_rect[2]    #[0] is x coord of upper left corner.      [2]is the x of bottom right corner
        #self.h = window_rect[1] - window_rect[3]    #[1] is y coord of upper left corner.      [3]is the y of bottom right corner
 
        

    def get_screenshot(self):
    
        #get image data for window
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0, 0), win32con.SRCCOPY)

        #save the screenshot
        dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')

        #instead of save to bitmap fiel changing to return an image
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        #need this or output will be wrong
        img.shape = (self.h, self.w, 4)

        #free resoureces
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())


        #need to drop the alpha channel of the image or erros with match template
        #however this line makes fps drop
        img =img[...,:3]

        #draw rectangles will error without this
        img = np.ascontiguousarray(img)

        return img
    


    def list_window_names(self):
        def winEnumHndler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHndler, None)

