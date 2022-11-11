#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize motors
B = Motor(Port.B)
C = Motor(Port.C)

# Initialise sensors
ultrasonic_sensor = UltrasonicSensor(Port.S4)
trigger_button = TouchSensor(Port.S1)
gyro_sensor = GyroSensor(Port.S3)

#Function that collects the training data
def Train(n):
    data = []
    target = []

    print(trigger_button.pressed())
    while True:
        if trigger_button.pressed():
            wait(10)
            gyro_sensor.reset_angle(0)
            ev3.speaker.beep()
            rotation_speed = 100

            for i in range(1,6,1):
                d = []
                A = 350
                while not trigger_button.pressed():
                    wait(10)
                gyro_sensor.reset_angle(0)
                while gyro_sensor.angle() <= A:
                    B.run(speed=rotation_speed)
                    C.run(speed=-rotation_speed)
                    distance = ultrasonic_sensor.distance()
                    d.append(distance)
                    wait(250)
                B.brake()
                C.brake()
                wait(10)
                data.append(d)
                target.append(n-1)
                wait(1000)

            ev3.speaker.beep(frequency=1000, duration=500)
            break
    return data, target

#collecting training data funtion
def get_training_data(zones):
    data = []
    target = []
    for n in zones:
       print('Place robot in Zone {}'.format(n))

       d, t = Train(n)
       data = data + d
       target = target + t

       print('Zone {} has been scanned'.format(n))
    return data, target

#number of zones we have
zones = [1, 2, 3, 4, 5, 6, 7, 8, 9]

#running the robot and storing the data from the zones in variables
data, target = get_training_data(zones)

print(data)
print(target)
