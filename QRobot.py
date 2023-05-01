from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
import pybricks.nxtdevices

class SensorMotor:
    def __init__(self, ev3):
        self.ev3 = ev3
        self.left = Motor(Port.A)
        self.right = Motor(Port.D)
        self.claw = Motor(Port.C)
        self.left_sonar = pybricks.nxtdevices.UltrasonicSensor(Port.S4)
        self.right_sonar = pybricks.nxtdevices.UltrasonicSensor(Port.S3)
        self.light = ColorSensor(Port.S2)
        self.loops = 0
        self.clawclosed = False

    def stop_all(self):
        self.left.run(0)
        self.right.run(0)

    def values(self):
        return ["SN:" + str(self.sonar.distance())]

    def show(self, state, action, reward, total_reward):
        self.ev3.screen.clear()
        self.ev3.screen.draw_text(0, 0, str(state))
        self.ev3.screen.draw_text(0, 16, str(action))
        self.ev3.screen.draw_text(0, 32, str(reward) + "(" + str(total_reward) + ")")
        y = 48
        for value in self.values():
            self.ev3.screen.draw_text(0, y, value)
            y += 16

SPEED = 360

def go_forward(robot):
    robot.left.run(SPEED)
    robot.right.run(SPEED)

def go_right(robot):
    robot.left.run(-SPEED)
    robot.right.run(SPEED)

def go_left(robot):
    robot.left.run(SPEED)
    robot.right.run(-SPEED)

def go_back(robot):
    robot.left.run(-SPEED)
    robot.right.run(-SPEED)

def stop(robot):
    robot.left.run(0)
    robot.right.run(0)

def grab(robot):
    distance_turned = robot.claw.angle()
    if 0 <= distance_turned <= 90 or robot.light.color() != Color.BLACK:
        robot.claw.run(SPEED)
        robot.clawclosed = True

def let_go(robot):
    distance_turned = robot.claw.angle()
    if 0 >= distance_turned >= 90 or robot.light.color() != Color.BLACK:
        robot.claw.run(-SPEED)
        robot.clawclosed = False