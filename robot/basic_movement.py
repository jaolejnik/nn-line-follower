import json
from enum import Enum
from time import sleep

import RPi.GPIO as GPIO

# ----- CONSTANTS -----
PWM_FREQ = 100
MOTORS_IDS = ("RIGHT", "LEFT")


# ----- SETUP BOARD -----
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


# ----- MOTOR FUNCTIONS -----
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


# ----- ENUMS -----
class DirectionX(Enum):
    LEFT = 0
    RIGHT = 1


class DirectionY(Enum):
    REVERSE = 0
    FORWARD = 1


# ----- MOTORS METHODS -----
class Motors:
    right = {"+": motor_a_positive, "-": motor_a_negative, "PWM": pwm_a}
    left = {"+": motor_b_positive, "-": motor_b_negative, "PWM": pwm_b}

    @staticmethod
    def motor_switch(motor_id):
        motor_dict = {"RIGHT": right, "LEFT": left}
        return motor_dict.get(motor_id)

    @staticmethod
    def run(motor_id, direction_y, speed):
        GPIO.output(22, GPIO.HIGH)
        if direction_y == DirectionY.FORWARD:
            motor_switch(motor_id)["+"](GPIO.HIGH)
            motor_switch(motor_id)["-"](GPIO.LOW)
        elif direction == DirectionY.REVERSE:
            motor_switch(motor_id)["+"](GPIO.LOW)
            motor_switch(motor_id)["-"](GPIO.HIGH)
        motor_switch(motor_id)["PWM"].ChangeDutyCycle(speed)


# ----- MOVEMENT METHODS -----
class Movement:
    """
    Basic movement methods.
    """

    @staticmethod
    def move(direction_y, speed, time):
        def __str__():
            return "move"

        for motor_id in MOTORS_IDS:
            Motors.run, (motor_id, direction_y, speed)
        sleep(time)
        stop_motors()

    @staticmethod
    def turn(direction_x, direction_y, speed, sharpness, time):
        if direction_x == DirectionX.RIGHT:
            Motors.run("LEFT", direction_y, speed * sharpness)
            Motors.run("RIGHT", direction_y, speed)
        elif direction_x == DirectionX.LEFT:
            Motors.run("LEFT", direction_y, speed)
            Motors.run("RIGHT", direction_y, speed * sharpness)
        sleep(time)
        stop_motors()

    @staticmethod
    def rotate(direction_x, speed, time):
        if direction == DirectionX.RIGHT:
            Motors.run("LEFT", DirectionY.REVERSE, speed)
            Motors.run("RIGHT", DirectionY.FORWARD, speed)
        elif direction == DirectionX.LEFT:
            Motors.run("LEFT", DirectionY.FORWARD, speed)
            Motors.run("RIGHT", DirectionY.REVERSE, speed)
        sleep(time)
        stop_motors()


class MovementManager:
    def __init__(self):
        self.data = {"actions": []}
        self.robot_is_running = True

    def save_action(self, action, **kwargs):
        action_type = action.__name__
        action_args = kwargs
        action_dict = {"type": action_type, "args": action_args}

        self.data["actions"].append(action_dict)

        if not self.robot_is_running:
            with open("movement_actions.json", "w") as action_file:
                json.dump(self.data)

    def load_actions(self, filename):
        with open("movement_actions.json") as action_file:
            self.data = json.load(action_file)

    def reverse_actions(self, action):
        for action in self.data["actions"]:
            if action["type"] == "move":
                action["args"]["direction_y"] = not action["args"]["direction_y"]
            if action["type"] == "turn":
                action["args"]["direction_y"] = not action["args"]["direction_y"]
                action["args"]["direction_x"] = not action["args"]["direction_x"]
            if action["type"] == "rotate":
                action["args"]["direction_x"] = not action["args"]["direction_x"]

    def perform_action(self, action, **kwargs):
        action_type = action if type(action) == str else action.__name__
        arg_string = [f"{key}={value}" for key, value in kwargs.items()].join(", ")
        command = f"{action_type}({arg_string})"
        eval(comand)

    def perform_saved_actions(self):
        for action in self.data["actions"]:
            self.perform_action(action["type"], action["args"])


if __name__ == "__main__":
    turn("RIGHT", "FORWARD", 50, 0.5, 2)
    sleep(0.3)
    move("FORWARD", 50, 2)
    sleep(0.3)
    rotate("RIGHT", 50, 5)

    GPIO.cleanup()
