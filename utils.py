import cv2 as cv
import serial.tools.list_ports
from time import sleep 

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
DEFAULT_CIRCLE_RADIUS = 2
LIVE_VIDEO = 0
BAUDRATE = 9600

def getComPortNumber(token):
    num = ""
    for c in str(token):
        if c.isnumeric() == True:
            num += c
    val = "COM" + num
    return val

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

def initSerialPorts(ports, serial_port):
    plist = []

    for port in ports:
        plist.append(str(port))

    port = None
    if len(plist) == 0:
        print("No ports available")
        exit()
    if len(plist) == 1:
        port = getComPortNumber(str(plist.pop()).split().pop()) # take the port name, split to token, get the first token and pass to function
    else:
        for i in range(0, len(plist)):
            print(str(i) + ": " + str(plist[i]))
        usrinput = int(input(("Multiple ports available, choose one: ")))
        port = getComPortNumber(str(plist.pop(usrinput)).split().pop())

    print("Chosen port: " + str(port))

    serial_port.baudrate = BAUDRATE
    serial_port.port = port
    return serial_port
