import cv2 as cv
import numpy as np
import sys 

import utils

WINDOW_NAME = "Display"
DEFAULT_FRAME_RATE = 25
VIDEO_WIDTH = 900
VIDEO_HEIGHT = 1600
RESOURCE_DIR = "res/"

def captureImage(path):
    img = cv.imread(path)
    utils.rescaleFrame(img,0.3)
    assert img is not None, "File could not be read"
    cv.namedWindow(WINDOW_NAME, cv.WINDOW_GUI_EXPANDED)
    cv.imshow(WINDOW_NAME, img)
    cv.waitKey(0)

def saveVideo(path, outname):
    cap = cv.VideoCapture(path)
    fourcc = cv.VideoWriter_fourcc(*"XVID")
    vidWidth = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    vidHeight = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    print(f"{vidWidth}x{vidHeight}")
    outname = outname + ".avi"
    out = cv.VideoWriter(outname, fourcc, 20.0, (vidWidth, vidHeight))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    cap.release()
    out.release()
    cv.destroyAllWindows()

face_cascade = cv.CascadeClassifier("frontal_face.xml")
profile_cascade = cv.CascadeClassifier("profiles.xml")
def faceDetect(imgPath):
    pic = cv.imread(imgPath)
    assert pic is not None, "Could not get file"
    pic_scaled = utils.rescaleFrame(pic, 0.3)
    grayImg = utils.gray(pic_scaled)

    # make rectangles
    faces_rect = face_cascade.detectMultiScale(grayImg, minNeighbors=3)
    print(f"Number of faces={len(faces_rect)}")
    for (x,y,w,h) in faces_rect:
        cv.rectangle(pic_scaled, (x,y), (x+w,y+h), (0,255,0), thickness=3)

    cv.imshow(WINDOW_NAME, pic_scaled)
    cv.waitKey(0)

def playVideo(path):
    print("Press \'q\' to quit video")
    cap = cv.VideoCapture(path)
    print(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    print(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    assert cap.isOpened() is not None, "Cannot open Camera"
    while cap.isOpened():
        ret, frame = cap.read()
        assert ret is not None
        frame = utils.rescaleFrame(frame)
        gframe = utils.gray(frame)
        gfaces = face_cascade.detectMultiScale(gframe, minNeighbors=3)
        if len(gfaces) >= 1:
            gfaces = gfaces[0]
            cv.rectangle(frame, (gfaces[0],gfaces[1]), (gfaces[0]+gfaces[2],gfaces[1]+gfaces[3]), (0,255,0), thickness=3)
            middle = ((gfaces[0] + gfaces[2]//2), ((gfaces[1] + gfaces[3]//2)))
            cv.circle(frame, middle, 2, (0,0,255), 1)
            print(f"X{middle[0]}Y{middle[1]}")
            #print(middle)
        cv.namedWindow(WINDOW_NAME)
        cv.imshow(WINDOW_NAME, frame) 
        key = cv.waitKey(DEFAULT_FRAME_RATE)
        if key == ord("q"):
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    #captureImage(RESOURCE_DIR+"img.jpg")
    playVideo(0)
