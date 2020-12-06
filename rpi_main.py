# from robot.programmed_linefollower import ProgrammedLineFollower

from robot.nn_linefollower import NNLineFollower
import RPi.GPIO as GPIO

robot = NNLineFollower(100, 0.01, "/home/pi/nn-line-follower/converted_model.tflite")
# robot = ProgrammedLineFollower(100, 0.01)

try:
    robot.run()
except KeyboardInterrupt:
    GPIO.cleanup()
