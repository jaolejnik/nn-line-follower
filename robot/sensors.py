from time import sleep, time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# ----- CONSTANTS -----
FRONT_TRIGGER = 35
FRONT_ECHO = 36
LEFT_LINE = 37
RIGHT_LINE = 38

# ----- DISTANCE SENSORS PINS -----
GPIO.setup(35, GPIO.OUT)
GPIO.setup(36, GPIO.IN)

# ----- LINE SENSORS PINS -----
GPIO.setup(LEFT_LINE, GPIO.IN)
GPIO.setup(RIGHT_LINE, GPIO.IN)


class LineSensors:
    """
    Infrared sensors for line detection.
    """

    @staticmethod
    def left():
        return GPIO.input(LEFT_LINE)

    @staticmethod
    def right():
        return GPIO.input(RIGHT_LINE)

    @staticmethod
    def one_or_more_active():
        return GPIO.input(LEFT_LINE) or GPIO.input(RIGHT_LINE)

    @staticmethod
    def both_active():
        return GPIO.input(LEFT_LINE) and GPIO.input(RIGHT_LINE)


class CollisionSensors:
    """
    Ultrasound sensors for detection of incoming objects.
    """

    @staticmethod
    def front_distance():
        GPIO.output(FRONT_TRIGGER, GPIO.HIGH)
        sleep(0.00001)
        GPIO.output(FRONT_TRIGGER, False)
        start = time()
        stop = time()
        while GPIO.input(FRONT_ECHO) == 0:
            start = time()
        while GPIO.input(FRONT_ECHO) == 1:
            stop = time()
        TimeElapsed = stop - start
        distance = (TimeElapsed * 34300) / 2
        return distance


if __name__ == "__main__":
    while True:
        print(
            "LEFT: ",
            LineSensors.left_sensor(),
            "| RIGHT: ",
            LineSensors.right_sensor(),
            "| FRONT DISTANCE:",
            CollisionSensors.front_distance(),
            end="\r",
        )
        sleep(0.1)
