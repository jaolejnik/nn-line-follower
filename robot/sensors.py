from time import sleep

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(37, GPIO.IN)
GPIO.setup(38, GPIO.IN)


class LineSensors:
    """
    Infrared sensors for line detection.
    """

    @staticmethod
    def left_sensor():
        return GPIO.input(37)

    @staticmethod
    def right_sensor():
        return GPIO.input(38)


if __name__ == "__main__":
    while True:
        print("LEFT: ", GPIO.input(37), "| RIGHT: ", GPIO.input(38))
        sleep(0.1)
