import tensorflow as tf
from tensorflow.keras.models import load_model

from simulation.sim_env import SimEnv
from utils.enums import ACTION_LIST, Actions, ActiveSensors


class ModelReplay:
    def __init__(self, model_path):
        self.sim_env = SimEnv()
        self.model = load_model(model_path)

    def run(self, max_steps=0):
        i = 0
        max_steps = max_steps if max_steps else 1
        state = self.sim_env.reset()
        while i <= max_steps:
            if max_steps:
                i += 1
            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, axis=0)
            action_probs_matrix = self.model(state_tensor)
            action_probs = tf.reshape(action_probs_matrix[0], (5,))
            action = tf.argmax(action_probs)

            state, reward, done = self.sim_env.step(ACTION_LIST[action])

            if done:
                return True
