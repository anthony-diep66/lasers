import cv2 as cv 
import numpy as np
import math
import utils 
from time import sleep

class Tracker:

    ix = 0
    iy = 0

    def __init__(self, serialPort, winName="Display", 
                 frameRate=25, resourceDir="res/", arduinoWidth=600, 
                 arduinoHeight = 600, fcascadeXML="frontal_face.xml"):
        self.serialPort = serialPort
        self.winName = winName
        self.frameRate = frameRate 
        self.resourceDir = resourceDir 
        self.arduinoWidth = arduinoWidth
        self.arduinoHeight = arduinoHeight
        self.faceCascadeXML = fcascadeXML

    def setVidDim(self, cap, defaults=False):
        if defaults is True:
            self.vidWidth = self.arduinoWidth
            self.vidHeight = self.arduinoHeight
            return

        self.vidHeight = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.vidWidth = cap.get(cv.CAP_PROP_FRAME_WIDTH)
        print(f"h={self.vidHeight} w={self.vidWidth}")

    def toArduinoSpecificData(self, pos):
        return "X" + str(180-math.floor(pos[0]//(self.arduinoWidth/180))) + "Y" + str(180-math.floor(pos[1]//(self.arduinoHeight/180)))

    def sendSerialData(self, packet):
        print(packet)
        self.serialPort.write(packet.encode("utf-8"))
        sleep(0.015)

    def scaleAndSend(self, x, y, factor=1, printMode=False):
        sx = int((self.arduinoWidth * x) // self.vidWidth) * factor
        sy = int((self.arduinoHeight * y) // self.vidHeight) * factor
        self.ix, self.iy = x, y
        if printMode is True:
            print(f"({sx},{sy})")
        self.sendSerialData(self.toArduinoSpecificData((sx,sy)))

    def drawCircleOnFrame(self, frame, xy):
        cv.circle(frame, xy, utils.DEFAULT_CIRCLE_RADIUS, utils.RED, thickness=3)

    def drawRectangleOnFrame(self, frame, gface):
        cv.rectangle(frame, (gface[0],gface[1]), 
                     (gface[0]+gface[2],gface[1]+gface[3]), utils.RED, thickness=3)

    def trackMouse(self, event, x, y, flags, param):
        self.scaleAndSend(x, y, param[0], param[1])

    def quit(self, frameRate):
        if cv.waitKey(frameRate) == ord("q"):
            return True
        return False

    def track(self):
        raise NotImplementedError() 

class MouseTracker(Tracker):

    def __init__(self, serialPort):
        super().__init__(serialPort)

    def track(self, path):
        cap = cv.VideoCapture(path)
        self.setVidDim(cap)
        cv.namedWindow(self.winName, cv.WINDOW_GUI_EXPANDED) 
        if path == 0:
            frameResizeFactor = 1
        else:
            frameResizeFactor = 0.5
        cv.setMouseCallback(self.winName, self.trackMouse, param=(int(1/frameResizeFactor), True))
        while cap.isOpened():
            ret, frame = cap.read()
            assert ret is not None 

            # rescale smaller to improve performance 
            frame = utils.rescaleFrame(frame, scale=frameResizeFactor)

            self.drawCircleOnFrame(frame, (self.ix, self.iy))

            cv.imshow(self.winName, frame) 
            if self.quit(self.frameRate) is True:
                break
        
        cap.release()
        cv.destroyAllWindows()
    
    def trackBlackScreen(self):
        blackScreen = np.zeros((600,600,3), np.uint8)
        self.setVidDim(None, defaults=True)
        cv.imshow(self.winName, blackScreen)
        cv.setMouseCallback(self.winName, self.trackMouse, (1, False))
        if self.quit(0) is True:
            return

class FaceTracker(Tracker):

    def __init__(self, serialPort):
        super().__init__(serialPort)
        self.faceCascade = cv.CascadeClassifier(self.faceCascadeXML)

    def track(self):
        cap = cv.VideoCapture(utils.LIVE_VIDEO)
        self.setVidDim(cap)
        cv.namedWindow(self.winName) 
        while cap.isOpened():
            ret, frame = cap.read()
            assert ret is not None 

            # convert to grayscale
            gframe = utils.gray(frame)

            # detect faces
            gfaces = self.faceCascade.detectMultiScale(gframe, scaleFactor=1.1, minNeighbors=3, minSize=[50,50])

            # if faces are detected
            if len(gfaces) >= 1:
                gface = gfaces[0]

                # calculates middle of drawn box
                middle = ((gface[0] + gface[2]//2), ((gface[1] + gface[3]//2)))
                self.scaleAndSend(middle[0], middle[1], factor=1, printMode=False)
                self.drawRectangleOnFrame(frame, gface)
                self.drawCircleOnFrame(frame, middle)

            cv.imshow(self.winName, frame) 
            if self.quit(self.frameRate) is True:
                break
        
        cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    ports = utils.serial.tools.list_ports.comports()
    templateSerialPort = utils.serial.Serial()
    serialPort = utils.initSerialPorts(ports, templateSerialPort)
    serialPort.open()
    tracker = FaceTracker(serialPort)
    tracker.track()
    serialPort.close()

    