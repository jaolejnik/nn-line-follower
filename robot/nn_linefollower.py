import tensorflow as tf
from tensorflow.keras.models import load_model

from utils.enums import Actions, ActiveSensors, DirectionX, DirectionY

from .linefollower import BaseLineFollower


class NNLineFollower(BaseLineFollower):
    def __init__(self, base_speed, action_time, model_path):
        super.__init__(base_speed, action_time)

        self.model = load_model(model_path)

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
        while self.collision_sensors.front_distance() > 5.0 and not self.lost:
            state = self.line_sensors.state()

            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.reshape(state_tensor, (1, 4))
            action_probs_matrix = self.model(state_tensor)
            action_probs = tf.reshape(action_probs_matrix[0], (5,))
            action = tf.argmax(action_probs)

            self.perform_action(action)

            if state == ActiveSensors.NONE:
                self.lost = self.timer.countdown_to(3)
