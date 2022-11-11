#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Create your objects here.
ev3 = EV3Brick()

# Initialize motors
B = Motor(Port.B)
C = Motor(Port.C)

# Initialise sensors
ultrasonic_sensor = UltrasonicSensor(Port.S4)
trigger_button = TouchSensor(Port.S1)
gyro_sensor = GyroSensor(Port.S3)

#Function that will collect the data for predicting the zone.
def Predict():
    data_p = []

    print(trigger_button.pressed())
    while True:
        if trigger_button.pressed():
            wait(10)
            gyro_sensor.reset_angle(0)
            ev3.speaker.beep()
            rotation_speed = 100
            log_interval = 100

            for i in range(1,3,1):
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
                wait(1)
                data_p.append(d)
                wait(1000)

            ev3.speaker.beep(frequency=1000, duration=500)
            break
    return data_p

#collecting the prediction data.
def get_prediction_data():
    data_p = []
    print('Place robot in a Random Zone')

    d = Predict()
    data_p = data_p + d

    print('Zone has been scanned!')
    return data_p

#running the robot and storing the environment data in a variable.
data_p = get_prediction_data()

print(data_p)