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


MOTORS = {
    "RIGHT": {"+": motor_a_positive, "-": motor_a_negative, "PWM": pwm_a},
    "LEFT": {"+": motor_b_positive, "-": motor_b_negative, "PWM": pwm_b},
}


def run_motor(motor_id, direction, speed):
    GPIO.output(22, GPIO.HIGH)
    if direction == "FORWARD":
        MOTORS[motor_id]["+"](GPIO.HIGH)
        MOTORS[motor_id]["-"](GPIO.LOW)
    elif direction == "REVERSE":
        MOTORS[motor_id]["+"](GPIO.LOW)
        MOTORS[motor_id]["-"](GPIO.HIGH)
    MOTORS[motor_id]["PWM"].ChangeDutyCycle(speed)


# ----- MOVEMENT METHODS -----
class Movement:
    """
    Basic movement methods.
    """

    @staticmethod
    def move(direction, speed, time):
        for motor_id in MOTORS_IDS:
            run_motor(motor_id, direction, speed)
        sleep(time)
        stop_motors()

    @staticmethod
    def turn(direction_x, direction_y, speed, sharpness, time):
        if direction_x == "RIGHT":
            run_motor("LEFT", direction_y, speed * sharpness)
            run_motor("RIGHT", direction_y, speed)
        elif direction_x == "LEFT":
            run_motor("LEFT", direction_y, speed)
            run_motor("RIGHT", direction_y, speed * sharpness)
        sleep(time)
        stop_motors()

    @staticmethod
    def rotate(direction, speed, time):
        if direction == "RIGHT":
            run_motor("LEFT", "REVERSE", speed)
            run_motor("RIGHT", "FORWARD", speed)
        elif direction == "LEFT":
            run_motor("LEFT", "FORWARD", speed)
            run_motor("RIGHT", "REVERSE", speed)
        sleep(time)
        stop_motors()


if __name__ == "__main__":
    turn("RIGHT", "FORWARD", 50, 0.5, 2)
    sleep(0.3)
    move("FORWARD", 50, 2)
    sleep(0.3)
    rotate("RIGHT", 50, 5)

    GPIO.cleanup()
