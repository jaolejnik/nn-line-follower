from time import sleep

import RPi.GPIO as GPIO

from utils.enums import DirectionX, DirectionY

PWM_FREQ = 100
MOTORS_IDS = ("RIGHT", "LEFT")


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Setup Pins for the motor controller (I'm using TB6612FNG H-Bridge)
GPIO.setup(12, GPIO.OUT)  # PWMA
GPIO.setup(16, GPIO.OUT)  # AIN1
GPIO.setup(18, GPIO.OUT)  # AIN2
GPIO.setup(22, GPIO.OUT)  # STBY
GPIO.setup(13, GPIO.OUT)  # BIN2
GPIO.setup(15, GPIO.OUT)  # BIN1
GPIO.setup(11, GPIO.OUT)  # PWMB

pwm_a = GPIO.PWM(12, PWM_FREQ)  # pin 18 to PWM
pwm_b = GPIO.PWM(11, PWM_FREQ)  # pin 13 to PWM
pwm_a.start(100)
pwm_b.start(100)


def motor_a_positive(signal):
    GPIO.output(16, signal)


def motor_a_negative(signal):
    GPIO.output(18, signal)


def motor_b_positive(signal):
    GPIO.output(13, signal)


def motor_b_negative(signal):
    GPIO.output(15, signal)


def stop_motors():
    GPIO.output(22, GPIO.LOW)


class Motors:
    right = {"+": motor_a_positive, "-": motor_a_negative, "PWM": pwm_a}
    left = {"+": motor_b_positive, "-": motor_b_negative, "PWM": pwm_b}

    @staticmethod
    def motor_switch(motor_id):
        motor_dict = {"RIGHT": Motors.right, "LEFT": Motors.left}
        return motor_dict.get(motor_id)

    @staticmethod
    def run(motor_id, direction_y, speed):
        GPIO.output(22, GPIO.HIGH)
        if direction_y == DirectionY.FORWARD:
            Motors.motor_switch(motor_id)["+"](GPIO.HIGH)
            Motors.motor_switch(motor_id)["-"](GPIO.LOW)
        elif direction_y == DirectionY.REVERSE:
            Motors.motor_switch(motor_id)["+"](GPIO.LOW)
            Motors.motor_switch(motor_id)["-"](GPIO.HIGH)
        Motors.motor_switch(motor_id)["PWM"].ChangeDutyCycle(speed)


class Movement:
    """
    Basic movement methods.
    """

    @staticmethod
    def move(direction_y, speed, time):
        for motor_id in MOTORS_IDS:
            Motors.run(motor_id, direction_y, speed)
        sleep(time)
        stop_motors()

    @staticmethod
    def turn(direction_x, direction_y, speed, sharpness, time):
        if direction_x == DirectionX.RIGHT:
            Motors.run("LEFT", direction_y, speed * (1 - sharpness))
            Motors.run("RIGHT", direction_y, speed)
        elif direction_x == DirectionX.LEFT:
            Motors.run("LEFT", direction_y, speed)
            Motors.run("RIGHT", direction_y, speed * (1 - sharpness))
        sleep(time)
        stop_motors()

    @staticmethod
    def rotate(direction_x, speed, time):
        if direction_x == DirectionX.RIGHT:
            Motors.run("LEFT", DirectionY.REVERSE, speed)
            Motors.run("RIGHT", DirectionY.FORWARD, speed)
        elif direction_x == DirectionX.LEFT:
            Motors.run("LEFT", DirectionY.FORWARD, speed)
            Motors.run("RIGHT", DirectionY.REVERSE, speed)
        sleep(time)
        stop_motors()
