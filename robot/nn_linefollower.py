import tensorflow as tf
import RPi.GPIO as GPIO

from time import sleep
from utils.enums import Actions, ActiveSensors, DirectionX, DirectionY, ACTION_LIST

from .base_linefollower import BaseLineFollower


class NNLineFollower(BaseLineFollower):
    def __init__(self, base_speed, action_time, model_path):
        super().__init__(base_speed, action_time)

        self.model_interpreter = tf.lite.Interpreter(model_path=model_path)
        self.model_interpreter.allocate_tensors()
        self.model_input_details = self.model_interpreter.get_input_details()
        self.model_output_details = self.model_interpreter.get_output_details()

    def pass_to_model(self, input_data):
        self.model_interpreter.set_tensor(
            self.model_input_details[0]["index"], input_data
        )

        self.model_interpreter.invoke()
        return self.model_interpreter.get_tensor(self.model_output_details[0]["index"])

    def perform_action(self, action):
        if action == Actions.MOVE_FORWARD:
            self.move(DirectionY.FORWARD)

        elif action == Actions.TURN_LEFT:
            self.turn(DirectionX.LEFT)

        elif action == Actions.TURN_RIGHT:
            self.turn(DirectionX.RIGHT)

        elif action == Actions.ROTATE_LEFT:
            self.rotate(DirectionX.LEFT)

        elif action == Actions.ROTATE_RIGHT:
            self.rotate(DirectionX.RIGHT)

    def run(self):
        while self.collision_sensors.front_distance() > 5.0:
            state = self.line_sensors.state()

            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, axis=0)
            state_tensor = tf.cast(state_tensor, dtype=tf.float32)
            action_probs_matrix = self.pass_to_model(state_tensor)
            action_probs = tf.reshape(action_probs_matrix[0], (5,))
            action = tf.argmax(action_probs)

            print(state, ACTION_LIST[action])
            self.perform_action(ACTION_LIST[action])
