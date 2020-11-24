from time import sleep, time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# ----- CONSTANTS -----
FRONT_TRIGGER = 31
FRONT_ECHO = 32
FAR_LEFT_LINE = 35
FAR_RIGHT_LINE = 36
LEFT_LINE = 37
RIGHT_LINE = 38

# ----- DISTANCE SENSORS PINS -----
GPIO.setup(FRONT_TRIGGER, GPIO.OUT)
GPIO.setup(FRONT_ECHO, GPIO.IN)

# ----- LINE SENSORS PINS -----
GPIO.setup(LEFT_LINE, GPIO.IN)
GPIO.setup(FAR_LEFT_LINE, GPIO.IN)
GPIO.setup(RIGHT_LINE, GPIO.IN)
GPIO.setup(FAR_RIGHT_LINE, GPIO.IN)


class LineSensors:
    @staticmethod
    def left():
        return GPIO.input(LEFT_LINE)

    @staticmethod
    def right():
        return GPIO.input(RIGHT_LINE)

    @staticmethod
    def far_left():
        return GPIO.input(FAR_LEFT_LINE)

    @staticmethod
    def far_right():
        return GPIO.input(FAR_RIGHT_LINE)

    @staticmethod
    def state():
        return (
            LineSensors.far_left(),
            LineSensors.left(),
            LineSensors.right(),
            LineSensors.far_right(),
        )

    @staticmethod
    def only_left_active():
        return (
            LineSensors.left()
            and not LineSensors.right()
            and not LineSensors.far_left()
            and not LineSensors.far_right()
        )

    @staticmethod
    def only_left_of_main_active():
        return LineSensors.left() and not LineSensors.right()

    @staticmethod
    def only_far_left_active():
        return (
            LineSensors.far_left()
            and not LineSensors.left()
            and not LineSensors.right()
            and not LineSensors.far_right()
        )

    @staticmethod
    def only_right_active():
        return (
            LineSensors.right()
            and not LineSensors.left()
            and not LineSensors.far_left()
            and not LineSensors.far_right()
        )

    @staticmethod
    def only_right_of_main_active():
        return LineSensors.right() and not LineSensors.left()

    @staticmethod
    def only_far_right_active():
        return (
            LineSensors.far_right()
            and not LineSensors.left()
            and not LineSensors.right()
            and not LineSensors.far_left()
        )

    @staticmethod
    def one_or_more_active():
        return (
            LineSensors.far_left()
            or LineSensors.left()
            or LineSensors.right()
            or LineSensors.far_right()
        )

    @staticmethod
    def one_of_main_active():
        return LineSensors.left() or LineSensors.right()

    @staticmethod
    def both_main_active():
        return LineSensors.left() and LineSensors.right()


class CollisionSensors:
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
        time_elapsed = stop - start
        distance = (time_elapsed * 34300) / 2

        return distance


if __name__ == "__main__":
    while True:
        print(
            "FAR_LEFT: ",
            LineSensors.far_left(),
            "| LEFT: ",
            LineSensors.left(),
            "| RIGHT: ",
            LineSensors.right(),
            "| FAR RIGHT: ",
            LineSensors.far_right(),
            "| FRONT DISTANCE:",
            CollisionSensors.front_distance(),
            end="\r",
        )
        sleep(0.1)
