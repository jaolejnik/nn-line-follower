import numpy as np
import tensorflow as tf

from utils.enums import Actions


class ReplayBuffer:
    def __init__(self):
        self.action_history = []
        self.state_history = []
        self.next_state_history = []
        self.rewards_history = []
        self.done_history = []
        self.episode_rewards_history = []

        self.max_memory_length = 100000
        self.VALID_KEYS = (
            "action",
            "state",
            "next_state",
            "reward",
            "episode_reward",
            "done",
        )

    def _are_valid_keys(self, keys):
        for key in keys():
            assert key in self.VALID_KEYS, "Invalid key for saving a value to history."

    def save_to_history(self, **kwargs):
        self._are_valid_keys(kwargs.keys())

        if "action" in kwargs.keys():
            self.action_history.append(kwargs["action"])

        if "state" in kwargs.keys():
            self.state_history.append(kwargs["state"])

        if "next_state" in kwargs.keys():
            self.next_state_history.append(kwargs["next_state"])

        if "reward" in kwargs.keys():
            self.rewards_history.append(kwargs["reward"])

        if "episode_reward" in kwargs.keys():
            self.episode_rewards_history.append(kwargs["episode_reward"])

        if "done" in kwargs.keys():
            self.done_history.append(kwargs["done"])

    def get_samples(self, indices):
        states = np.array([self.state_history[i] for i in indices])
        next_states = np.array([self.next_state_history[i] for i in indices])
        rewards = [self.rewards_history[i] for i in indices]
        actions = [self.action_history[i] for i in indices]
        dones = tf.convert_to_tensor([float(self.done_history[i]) for i in indices])

        return states, next_states, rewards, actions, dones

    def limit_history(self, **kwargs):
        self._are_valid_keys(kwargs.keys())

        if self.rewards_history_size() <= self.max_memory_length:
            return

        if kwargs["action"]:
            del self.action_history[:1]

        if kwargs["state"]:
            del self.state_history[:1]

        if kwargs["next_state"]:
            del self.state_next_history[:1]

        if kwargs["reward"]:
            del self.rewards_history[:1]

        if kwargs["episode_reward"]():
            del self.episode_rewards_history[:1]

        if kwargs["done"]:
            del self.done_history[:1]

    def episode_rewards_mean(self):
        return np.mean(self.episode_rewards_history)

    def action_history_size(self):
        return len(self.action_history)

    def state_history_size(self):
        return len(self.state_history)

    def next_state_history_size(self):
        return len(self.next_state_history)

    def done_history_size(self):
        return len(self.done_history)

    def rewards_history_size(self):
        return len(self.rewards_history)

    def episode_rewards_history_size(self):
        return len(self.episode_rewards_history)
