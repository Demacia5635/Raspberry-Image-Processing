from networktables import NetworkTables, NetworkTable
from threading import Condition
import requests

robot_ip = '10.56.35.2'
smart_dashboard : NetworkTable = None

#TODO : put in default values
min_hsv = (-1,-1,-1)
max_hsv = (-1,-1,-1)

camera_width = 1920
camera_height = 1080
camera_fps = 30

def update_vars() -> None:
    global camera_width, camera_height, camera_fps

    min_hsv[0] = smart_dashboard.getNumber('vision_min_h', min_hsv[0])
    min_hsv[1] = smart_dashboard.getNumber('vision_min_s', min_hsv[1])
    min_hsv[2] = smart_dashboard.getNumber('vision_min_v', min_hsv[2])

    max_hsv[0] = smart_dashboard.getNumber('vision_max_h', max_hsv[0])
    max_hsv[1] = smart_dashboard.getNumber('vision_max_s', max_hsv[1])
    max_hsv[2] = smart_dashboard.getNumber('vision_max_v', max_hsv[2])

def connect() -> None:
    global smart_dashboard
    cond = Condition()
    notified = False
    NetworkTables.initialize(server='10.56.35.2')
    NetworkTables.addConnectionListener(lambda connected, info: connection_listener(connected, info, cond), immediateNotify=True)

    with cond:
        print("Connecting...")
        if not notified:
            cond.wait()

    print("Connected!")
    smart_dashboard = NetworkTables.getTable('SmartDashboard')
    update_vars()


def connection_listener(connected, info, cond : Condition) -> None:
    print(info, '; Connected=%s' % connected)
    with cond:
        cond.notify()

def connected_to_robot():
    try:
        print("Searching for robot...")
        status_code = requests.get(robot_ip, timeout=(2, 1)).status_code
        return status_code == 200
    except:
        print('robot is dead 🦀')
        return False