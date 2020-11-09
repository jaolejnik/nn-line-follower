import random
from os import system

import numpy as np
import pandas as pd

from simulation.sim_env import SimEnv
from utils.enums import Actions, ActiveSensors


class QLearningClient:
    def __init__(self):
        self.init_q_table()
        self.env = SimEnv()

        self.rewards_all_episodes = []

        self.learning_rate = 0.1
        self.discount_rate = 0.1
        self.exploration_rate = 1
        self.max_exploration_rate = 1
        self.min_exploration_rate = 0.1
        self.exploration_decay_rate = 0.01

    def init_q_table(self):
        self.q_table = {}
        for state in ActiveSensors:
            self.q_table[state.value] = {}
            for action in Actions:
                self.q_table[state.value][action] = 0

    def max_q_action_for_state(self, state):
        return max(self.q_table[state], key=self.q_table[state].get)

    def max_q_value_for_state(self, state):
        action_key = self.max_q_action_for_state(state)
        return self.q_table[state][action_key]

    def print_q_table(self):
        print(pd.DataFrame.from_dict(self.q_table))
        print()

    def learn(self, num_episodes, max_steps_per_episode):
        for episode in range(num_episodes):
            state = self.env.reset()
            done = False
            rewards_current_episode = 0

            for step in range(max_steps_per_episode):
                exploration_rate_threshold = np.random.uniform(0, 1)
                if exploration_rate_threshold > self.exploration_rate:
                    action = self.max_q_action_for_state(state)
                    print("EXECUTION", self.exploration_rate)
                else:
                    print(
                        "EPLORATION", self.exploration_rate, exploration_rate_threshold
                    )
                    action = random.choice([action for action in Actions])

                new_state, reward, done = self.env.step(action, (episode, step))

                self.q_table[state][action] = self.q_table[state][action] * (
                    1 - self.learning_rate
                ) + self.learning_rate * (
                    reward + self.discount_rate * self.max_q_value_for_state(new_state)
                )

                self.print_q_table()
                state = new_state
                rewards_current_episode += reward

                if done:
                    break

            self.exploration_rate = self.min_exploration_rate + (
                self.max_exploration_rate - self.min_exploration_rate
            ) * np.exp(-self.exploration_decay_rate * episode)

            self.rewards_all_episodes.append(rewards_current_episode)
