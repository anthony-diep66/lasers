import math
import serial.tools.list_ports
import pygame 
from time import sleep
BAUDRATE = 9600

ports = serial.tools.list_ports.comports()
serial_port = serial.Serial()
WIDTH = 600
HEIGHT = 600
def get_com_num(token):
    num = ""
    for c in str(token):
        if c.isnumeric() == True:
            num += c
    val = "COM" + num
    return val

def init():
    plist = []

    for port in ports:
        plist.append(str(port))

    port = None
    if len(plist) == 0:
        print("No ports available")
        exit()
    if len(plist) == 1:
        port = get_com_num(str(plist.pop()).split().pop()) # take the port name, split to token, get the first token and pass to function
    else:
        for i in range(0, len(plist)):
            print(str(i) + ": " + str(plist[i]))
        usrinput = int(input(("Multiple ports available, choose one: ")))
        port = get_com_num(str(plist.pop(usrinput)).split().pop())

    print("Chosen port: " + str(port))

    serial_port.baudrate = BAUDRATE
    serial_port.port = port
    serial_port.open()

def SendSerial(pos):
    packet = "X" + str(180-math.floor(pos[0]//(WIDTH/180))) + "Y" + str(180-math.floor(pos[1]//(HEIGHT/180)))
    print(packet)
    serial_port.write(packet.encode("utf-8"))
    sleep(0.015)

def _run(screen, timer, fps):
    done = False
    while done is False:
        screen.fill("black")
        timer.tick(fps)
        mouse_pos = pygame.mouse.get_pos()
        SendSerial(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    pygame.display.flip()
    pygame.quit() 

def setup_and_run():
    pygame.init()

    timer = pygame.time.Clock()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    fps = 60

    _run(screen, timer, fps)

if __name__ == "__main__":
    init()
    setup_and_run()
    