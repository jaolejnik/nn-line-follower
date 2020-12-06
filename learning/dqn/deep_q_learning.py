import os
import sys
from datetime import datetime
from time import sleep

import numpy as np
import tensorflow as tf
from tensorflow import keras

from simulation.sim_env import SimEnv
from utils.enums import ACTION_LIST, Actions
from utils.score_logger import ScoreLogger
from utils.score_plotter import ScorePlotter

from .neural_network import create_q_model
from .replay_buffer import ReplayBuffer

HOME_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
NUMBER_OF_ACTIONS = len(ACTION_LIST)
MODEL_NAME = f"{datetime.now().date()}_{datetime.now().hour}-{datetime.now().minute}"


class DeepQLearningClient:
    def __init__(self, **kwargs):
        self.greed_rate = kwargs.get("greed_rate", 1.0)
        self.greed_min = kwargs.get("greed_min", 0.1)
        self.greed_max = self.greed_rate
        self.discount_rate = kwargs.get("discount_rate", 0.99)
        self.batch_size = kwargs.get("batch_size", 32)
        self.max_episodes = kwargs.get("max_episodes", 10000)
        self.max_steps_per_episode = 3000

        self.random_steps = kwargs.get("random_steps", 10000)
        self.greedy_steps = kwargs.get("greedy_steps", 100000)

        self.running_reward = 0
        self.highest_running_reward = kwargs.get("highest_running_reward", 0)
        self.winning_reward = kwargs.get("winning_reward", 3000)

        self.update_after_actions = kwargs.get("update_after_actions", 1)
        self.update_target_after_actions = kwargs.get(
            "update_target_after_actions", 10000
        )
        self.visual_after_episodes = kwargs.get("visual_after_episodes", 0)
        self.optimizer = kwargs.get("optimizer", keras.optimizers.Adam)(
            learning_rate=kwargs.get("learning_rate", 0.01), clipnorm=1.0
        )
        self.loss_function = keras.losses.Huber()

        self.model = create_q_model()
        self.target_model = create_q_model()

        self.model_dir = os.path.join(HOME_DIR, "saved_data", "dqn", MODEL_NAME)
        self._save_config_txt(kwargs)

        self.replay_buffer = ReplayBuffer()
        self.logger = ScoreLogger(MODEL_NAME, self.model_dir)
        self.plotter = ScorePlotter(MODEL_NAME, self.logger.filepath)
        self.sim_env = SimEnv()

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

        return loss.numpy()

    def _update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def _choose_action(
        self, steps_count, state, explore_actions, exploit_actions, model_check
    ):
        if (
            steps_count < self.random_steps or self.greed_rate > np.random.rand(1)[0]
        ) and not model_check:
            action = np.random.choice([i for i in range(NUMBER_OF_ACTIONS)])
            explore_actions += 1
        else:
            exploit_actions += 1
            input_state = np.array(state).astype(int)
            state_tensor = tf.convert_to_tensor(input_state)
            # state_tensor = tf.reshape(state_tensor, (1, 4))
            state_tensor = tf.expand_dims(state_tensor, axis=0)
            action_probs_matrix = self.model(state_tensor)

            action_probs = tf.reshape(action_probs_matrix[0], (5,))
            action = tf.argmax(action_probs)

        return action, explore_actions, exploit_actions

    def _save_config_txt(self, config_dict):
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
        config_file = os.path.join(self.model_dir, "config.txt")
        with open(config_file, "w") as f:
            for key, value in config_dict.items():
                f.write(f"{key} = {value}\n")

    def _save_model(self):
        print("SAVING MODEL")
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
        self.model.save(
            os.path.join(self.model_dir, "models", str(int(self.running_reward)))
        )

    def _create_plots(self):
        self.plotter.load_scores()
        self.plotter.plot_all()

    def _learn(self):
        steps_count = 0

        for episode in range(1, self.max_episodes + 1):
            state = self.sim_env.reset()
            episode_reward = 0
            explore_actions = 0
            exploit_actions = 0
            loss_list = []

            visual = not episode % self.visual_after_episodes
            model_check = False  # not episode % 0
            save = not episode % 50

            for timestep in range(self.max_steps_per_episode):
                steps_count += 1

                action, explore_actions, exploit_actions = self._choose_action(
                    steps_count, state, explore_actions, exploit_actions, model_check
                )

                if not model_check:
                    self._update_greed_rate()

                next_state, reward, done = self.sim_env.step(
                    ACTION_LIST[action],
                    (episode, timestep, episode_reward),
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
                    loss = self._update_model()
                    loss_list.append(loss)

                if steps_count % self.update_target_after_actions == 0:
                    self._update_target_model()
                    print(
                        f"UPDATED TARGET MODEL! Running reward: {self.running_reward}"
                    )

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

            if model_check:
                print("MODEL CHECK!")
            print(
                "Exploration count:",
                explore_actions,
                "Exploitation:",
                exploit_actions,
            )
            print("Episode:", episode, "Reward:", episode_reward)

            self.replay_buffer.save_to_history(episode_reward=episode_reward)
            if self.replay_buffer.episode_rewards_history_size() > 100:
                self.replay_buffer.limit_history(episode_reward=True)

            self.running_reward = self.replay_buffer.episode_rewards_mean()

            self.logger.save_scores(
                (
                    episode,
                    episode_reward,
                    self.running_reward,
                    steps_count,
                    explore_actions,
                    exploit_actions,
                    self.greed_rate,
                    np.mean(loss_list),
                )
            )

            if (
                model_check or save
            ) and self.running_reward > self.highest_running_reward:
                self._save_model()
                self.highest_running_reward = self.running_reward

            if self.running_reward > self.winning_reward:
                print(f"Solved at episode {episode}")
                print("Saving model...")
                self._save_model()
                print("creating plots...")
                self._create_plots()
                break

    def run(self):
        try:
            self._learn()
        except KeyboardInterrupt:
            sleep(1)
            print("\n\n\n")
            print("Saving model...")
            self._save_model()
            print("Creating plots...")
            self._create_plots()
            sys.exit()
