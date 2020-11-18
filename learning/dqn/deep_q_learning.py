import os
from datetime import datetime

import numpy as np
import tensorflow as tf
from tensorflow import keras

from simulation.sim_env import SimEnv
from utils.enums import Actions, ActiveSensors
from utils.score_logger import ScoreLogger

from .neural_network import create_q_model
from .replay_buffer import ReplayBuffer

CURRENT_DIR = os.path.dirname(__file__)
ACTION_LIST = [action for action in Actions]
NUMBER_OF_ACTIONS = len(ACTION_LIST)
MODEL_NAME = (
    "dqn_model_"
    + f"{datetime.now().date()}_{datetime.now().hour}-{datetime.now().minute}"
)


class DeepQLearningClient:
    def __init__(self):
        self._init_constants()
        self._init_q_models()
        self.replay_buffer = ReplayBuffer()
        self.score_logger = ScoreLogger(MODEL_NAME, os.path.join(CURRENT_DIR, "scores"))
        self.sim_env = SimEnv()

        self.loss_function = keras.losses.Huber()
        self.optimizer = keras.optimizers.Adam(learning_rate=0.01, clipnorm=1.0)

    def _init_constants(self):
        self.discount_rate = 0.99
        self.greed_rate = 1.0
        self.greed_min = 0.1
        self.greed_max = 1.0
        self.batch_size = 32
        self.max_steps_per_episode = 10000

        self.random_steps = 5000
        self.greedy_steps = 100000

        self.update_after_actions = 5
        self.update_target_after_actions = 10000

    def _init_q_models(self):
        self.model = create_q_model()
        self.target_model = create_q_model()

    def _update_greed_rate(self):
        self.greed_rate -= (self.greed_max - self.greed_min) / self.greedy_steps
        self.greed_rate = max(self.greed_rate, self.greed_min)

    def _update_model(self):
        indices = np.random.choice(
            range(self.replay_buffer.done_history_size()),
            size=self.batch_size,
        )

        (
            state_sample,
            next_state_sample,
            rewards_sample,
            action_sample,
            done_sample,
        ) = self.replay_buffer.get_samples(indices)

        future_rewards = self.target_model.predict(next_state_sample)
        updated_q_values = rewards_sample + self.discount_rate * tf.reduce_max(
            future_rewards, axis=1
        )

        updated_q_values = updated_q_values * (1 - done_sample) - done_sample

        masks = tf.one_hot(action_sample, NUMBER_OF_ACTIONS)

        with tf.GradientTape() as tape:
            q_values = self.model(state_sample)
            q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
            loss = self.loss_function(updated_q_values, q_action)

        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

    def _update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def _save_model(self, running_reward):
        model_dir = os.path.join(CURRENT_DIR, "saved_models", MODEL_NAME)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        self.model.save(os.path.join(model_dir, str(running_reward)))

    def learn(self):
        steps_count = 0
        episode_count = 0
        running_reward = 0

        while True:
            episode_count += 1

            visual = not episode_count % 100
            save = not episode_count % 1000

            state = self.sim_env.reset()
            episode_reward = 0
            exploration_actions = 0
            exploitation_actions = 0

            for timestep in range(self.max_steps_per_episode):
                steps_count += 1

                if (
                    steps_count < self.random_steps
                    or self.greed_rate > np.random.rand(1)[0]
                ):
                    action = np.random.choice([i for i in range(NUMBER_OF_ACTIONS)])
                    exploration_actions += 1
                else:
                    exploitation_actions += 1
                    state_tensor = tf.convert_to_tensor(state)
                    state_tensor = tf.reshape(state_tensor, (1, 4))
                    action_probs_matrix = self.model(state_tensor, training=False)
                    action_probs = tf.reshape(action_probs_matrix[0], (5,))
                    action = tf.argmax(action_probs)

                self._update_greed_rate()

                next_state, reward, done = self.sim_env.step(
                    ACTION_LIST[action],
                    (episode_count, timestep, episode_reward),
                    visual=visual,
                )

                episode_reward += reward

                self.replay_buffer.save_to_history(
                    action=action,
                    state=state,
                    next_state=next_state,
                    reward=reward,
                    done=done,
                )

                state = next_state

                if (
                    steps_count % self.update_after_actions == 0
                    and self.replay_buffer.done_history_size() > self.batch_size
                ):
                    self._update_model()

                if steps_count % self.update_target_after_actions == 0:
                    self._update_target_model()
                    print(f"UPDATED TARGET MODEL! Running reward: {running_reward:.2f}")

                if (
                    self.replay_buffer.rewards_history_size()
                    > self.replay_buffer.max_memory_length
                ):
                    self.replay_buffer.limit_history(
                        action=True,
                        state=True,
                        next_state=True,
                        reward=True,
                        done=True,
                    )

                if done:
                    break
            print(
                "Exploration count:",
                exploration_actions,
                "Exploitation:",
                exploitation_actions,
            )
            print("Episode:", episode_count, "Reward:", episode_reward)

            self.replay_buffer.save_to_history(episode_reward=episode_reward)
            if (
                self.replay_buffer.episode_rewards_history_size()
                > self.replay_buffer.max_memory_length
            ):
                self.replay_buffer.limit_history(episode_reward=True)

            running_reward = self.replay_buffer.episode_rewards_mean()

            self.score_logger.save_scores(
                (
                    episode_count,
                    episode_reward,
                    running_reward,
                    steps_count,
                    exploration_actions,
                    exploitation_actions,
                    self.greed_rate,
                )
            )
            if save:
                self._save_model(running_reward)
                if running_reward > 9000:
                    print(f"Solved at episode {episode_count}")
                    break
