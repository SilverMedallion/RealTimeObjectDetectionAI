import cv2 as cv
import numpy as np
import os     #need to write to files
from windowcaptureHC import WindowCapture
from visionHC import visionHC

#files containg images wfor tsting
POSITIVE_test_folder = 'positiveTest' 
NEGATIVE_test_folder = 'negativeTest' 

#process images and get the number of true positives, false positives, true negatives and false negatives
#takes the folder of images to be used for testing and if it is evaluating positive or negative images
def evaluate_model(test_folder, label):
    #get the names of the images files for testing
    files = os.listdir(test_folder)
    
    print(f"Testing in {test_folder}: Found {len(files)} files.") 

    #initialise counts for this dataset
    truePositive = 0
    falsePositive = 0
    trueNegative = 0
    falseNegative = 0  
    
    #loop for the number of test images
    for file in files:
        img_path = os.path.join(test_folder, file) #need to get the full filename
        img = cv.imread(img_path)    

        if img is None:
            print(f"Failed to load image: {img_path}")
            continue
        else:
            print(f"Image loaded successfulllly : {img_path}")
        if img is None: #make sure the image is valid 
            continue
        
        #return a list of rectangles found in the image
        rectangles = cascade_headcrab.detectMultiScale(img)
        detected = len(rectangles) > 0
        print(f"Detection in {file}: {len(rectangles)}")

        #check if rectanlges were detectd and set number of them
        detected = len(rectangles) > 0

        #increase counts, based on if the images should have headcrabs or not
        if label == 'positive' and detected:
            truePositive += 1
        elif label == 'positive' and not detected:
            falseNegative += 1
        elif label == 'negative' and detected:
            falsePositive += 1
        elif label == 'negative' and not detected:
            trueNegative += 1
    
    return truePositive, falsePositive, trueNegative, falseNegative

#Load the trained cascade classifier and save to variable
cascade_headcrab = cv.CascadeClassifier('cascade/cascade.xml')

#check classifier is loading correctly
if cascade_headcrab.empty():
    print("Fiale dto load cascade classifier")
else:
    print("Cascade classifier loaded scucessfully")

#there values will be increased by return of evaluate model
overallTruePositive = 0
overallFalsePositive = 0
overallTrueNegative = 0
overallFalseNegative = 0


truePositive, falsePositive, trueNegative, falseNegative = evaluate_model(POSITIVE_test_folder, 'positive')
overallTruePositive += truePositive
overallFalsePositive += falsePositive
overallTrueNegative += trueNegative
overallFalseNegative += falseNegative

truePositive, falsePositive, trueNegative, falseNegative = evaluate_model(NEGATIVE_test_folder, 'negative')
overallTruePositive += truePositive
overallFalsePositive += falsePositive
overallTrueNegative += trueNegative
overallFalseNegative += falseNegative

#calculate results
accuracy = (overallTruePositive + overallTrueNegative) / (overallTruePositive + overallFalsePositive + overallTrueNegative + overallFalseNegative) if (overallTruePositive + overallFalsePositive + overallTrueNegative + overallFalseNegative) > 0 else 0
precision = overallTruePositive / (overallTruePositive + overallFalsePositive) if (overallTruePositive + overallFalsePositive) > 0 else 0
recall = overallTruePositive / (overallTruePositive + overallFalseNegative) if (overallTruePositive + overallFalseNegative) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

#display calculated results
print(f'Accuracy: {accuracy:.4f}')
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
print(f'F1 Score: {f1_score:.4f}')
