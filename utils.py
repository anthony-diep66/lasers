import cv2 as cv

def rescaleFrame(frame, scale=0.6):
    height = int(frame.shape[0] * scale)
    width = int(frame.shape[1] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def rescaleDim(dim, scale=0.6):
    height = int(dim[0] * scale)
    width = int(dim[1] * scale)
    return (width, height)

def gray(frame):
    return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

