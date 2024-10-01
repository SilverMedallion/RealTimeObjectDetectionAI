import cv2 as cv
import numpy as np

class visionHC:

    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        if needle_img_path:   #if check needed so we can pass none in
            # load in image we are trying to match
            self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

            #get the dimenstions of the needle image we are looking for
            self.needle_w = self.needle_img.shape[1]
            self.needle_h = self.needle_img.shape[0]


        #method for matching the image can choose from: TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method


   #pass in rectangles which are will be matches and pass in image to draw rectangles on
    def draw_rectangles(self, haystack_img, rectangles):
        
        line_color = (0, 255, 0)  #note these colours are flipped so BRG
        line_type = cv.LINE_4

        #loop for number of rectangles that will be drawn
        for (x, y, w, h) in rectangles:
            
            #set positions for rectangle corners
            top_left = (x, y)
            bottom_right = (x + w, y + h)

            #draw the rectangles
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img
    



####Old code from regular image detection
    def findClickPostions(needle_img_path, haystack_img, threshold=0.5, debug_mode=None):
    
        #load in the image files
        #haystack will be passed in directly from window capture
        needle_img = cv.imread('PlasmaPistol.jpg', cv.IMREAD_UNCHANGED)

        #get the dimenstions of the needle image
        needle_width = needle_img.shape[1]
        needle_height = needle_img.shape[0]

        #method for matching the image can choose from: TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        method = cv.TM_CCOEFF_NORMED

        #match the images, TM_CEOEFF_NORMED gives best result
        result = cv.matchTemplate(haystack_img, needle_img, method)

        #get the all positions from match result that exceed threshold
        locations = np.where(result>= threshold)
        locations = list(zip(*locations[::-1]))
        #print locations

        #group overalpping rectangels so multiple don't draw on top of each other
        #create a list of rectangles
        rectangles = []
        for loc in locations:
            rect =[int(loc[0]), int(loc[1]), needle_width, needle_height]

            #add every rect ot the list twice to keep single non overlapping boxes
            rectangles.append(rect)
            rectangles.append(rect)

        #group threshold parameter should be 1 if 0 then no grouping is done. 2 means object needs 3 overlapping rectangles to appear in result
        #0.5 is "relative differnce between sides of the rectangles to merge them into a group"
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        points =[]
        if len(rectangles):

            #define colours and shape of markers and rectangle lines
            line_colour = (0, 255, 0)
            line_type = cv.LINE_4
            marker_colour = (255, 0,255)
            marker_type = cv.MARKER_CROSS 

            #loop for all rectangles
            for(x,y,w,h) in rectangles:
            
                #fidn the centre position
                center_x = x + int(w/2)
                center_y = y + int(h/2)

                #save the points
                points.append((center_x, center_y))

                if debug_mode =='rectangles':
                    #find box pos
                    top_left =(x,y)
                    bottom_right =(x+w, y+h)

                    #draw box
                    cv.rectangle(haystack_img, top_left, bottom_right, color= line_colour, lineType=line_type, thickness=2)
                #if debug mode is set to points draw markers instead of rectangles
                elif debug_mode =='points':
                    #draw marker at centre point
                    cv.drawMarker(haystack_img, (center_x, center_y), color=marker_colour, markerType=marker_type, markerSize=40, thickness=2)

        #must ensure this is alwasys getting called otherwise rectangles will only draw when there are new results
        if debug_mode:
            cv.imshow('Matches',haystack_img)

        return points


    
