#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import socket
import QRobot, lib

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.
ev3.speaker.beep()

SERVER_IP = "172.17.4.118"
PORT = 8888

def send_message(message):
    reply = None
    try:
        sock = socket.socket()
        sock.connect((SERVER_IP, PORT))
        sock.send(message.encode())
        reply = sock.recv(1024).decode()
    except Exception as e:
        reply = str(e)
    finally:
        sock.close()
    return reply

robot = QRobot.SensorMotor(ev3)
send_message("knn 3 Qlearning")

LABEL_CLEAR = 0
LABEL_OBJECT = 1
LABEL_PERSON = 2
LABEL_OBSTACLE = 3
TOO_FAR_RIGHT = 4
TOO_FAR_LEFT = 5

def find_state(robot):
    distance_left = robot.left_sonar.distance()
    distance_right = robot.right_sonar.distance()
    msg = send_message("classify")
    if (msg == "Label_Object") and (distance_left < 50) and (distance_right <50):
        return LABEL_OBJECT
    elif (distance_right < distance_left):
        return TOO_FAR_RIGHT
    elif (distance_left < distance_right):
        return TOO_FAR_LEFT
    elif (msg == "Label_Person") and (robot.clawclosed):
        return LABEL_PERSON
    elif msg == "Label_Clear":
        return LABEL_CLEAR
    elif msg == "Label_Obstacle":
        return LABEL_OBSTACLE
    else:
        return LABEL_CLEAR
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, msg)
    wait(100)


def reward(robot, state, action):
    if state == LABEL_OBJECT:
        return 10
    elif state == LABEL_PERSON:
        return 15
    elif (state == LABEL_OBSTACLE) or (state == TOO_FAR_LEFT) or (state == TOO_FAR_RIGHT):
        return -5
    elif state == LABEL_CLEAR:
        return 1
    elif action == 0:
        return 1
    else:
        return 0

params = lib.QParameters()
params.pause_ms = 500
params.actions = [QRobot.go_forward, QRobot.go_left, QRobot.go_right, QRobot.go_back, QRobot.grab, QRobot.let_go]
params.num_states = 6
params.state_func = find_state
params.reward_func = reward
params.target_visits = 5
params.discount = 0.5
params.rate_constant = 10
params.max_steps = 200

lib.run_q(QRobot.SensorMotor(ev3), params)