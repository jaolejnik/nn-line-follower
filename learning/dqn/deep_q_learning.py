import numpy as np
import tensorflow as tf
from tensorflow import keras

from simulation.sim_env import SimEnv
from utils.enums import Actions, ActiveSensors

from .neural_network import create_q_model
from .replay_buffer import ReplayBuffer

ACTION_LIST = [action for action in Actions]
NUMBER_OF_ACTIONS = len(ACTION_LIST)


class DeepQLearningClient:
    def __init__(self):
        self._init_constants()
        self._init_q_models()
        self.replay_buffer = ReplayBuffer()
        self.sim_env = SimEnv()

        self.steps_count = 0

        self.loss_function = keras.losses.Huber()
        self.optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)

    def _init_constants(self):
        self.discount_rate = 0.99
        self.greed_rate = 1.0
        self.greed_min = 0.1
        self.greed_max = 1.0
        self.batch_size = 32
        self.max_steps_per_episode = 10000

        self.random_steps = 50000
        self.greedy_steps = 100000

        self.update_after_actions = 5
        self.update_target_after_actions = 10000

    def _init_q_models(self):
        self.model = create_q_model()
        self.target_model = create_q_model()

    def _update_greed_rate(self):
        self.greed_rate -= (self.greed_max - self.greed_min) / self.greedy_steps
        self.greed_rate = max(self.greed_rate, self.greed_min)

    def learn(self):
        episode_count = 0
        running_reward = 0
        while True:
            state = self.sim_env.reset()
            episode_reward = 0
            episode_count += 1

            for timestep in range(self.max_steps_per_episode):
                self.steps_count += 0

                if (
                    self.steps_count < self.random_steps
                    or self.greed_rate > np.random.rand(1)[0]
                ):
                    action = np.random.choice([i for i in range(NUMBER_OF_ACTIONS)])
                else:
                    state_tensor = tf.convert_to_tensor(state)
                    action_probs = self.model(state_tensor, training=False)
                    action = tf.argmax(action_probs[0]).numpy()

                self._update_greed_rate()

                next_state, reward, done = self.sim_env.step(
                    ACTION_LIST[action], (episode_count, timestep)
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
                    self.steps_count % self.update_after_actions == 0
                    and self.replay_buffer.done_history_size() > self.batch_size
                ):
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
                    updated_q_values = (
                        rewards_sample
                        + self.discount_rate
                        * tf.reduce_max(tf.reduce_max(future_rewards, axis=1), axis=1)
                    )

                    updated_q_values = (
                        updated_q_values * (1 - done_sample) - done_sample
                    )

                    masks = tf.one_hot(action_sample, NUMBER_OF_ACTIONS)

                    with tf.GradientTape() as tape:
                        q_values = tf.reduce_max(self.model(state_sample), axis=1)
                        q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
                        loss = self.loss_function(updated_q_values, q_action)

                    grads = tape.gradient(loss, self.model.trainable_variables)
                    self.optimizer.apply_gradients(
                        zip(grads, self.model.trainable_variables)
                    )

                if self.steps_count % self.update_target_after_actions == 0:
                    self.target_model.set_weights(self.model.get_weights())
                    print(f"Episode {episode_count}, step {timestep}")
                    print(f"Running reward: {running_reward:.2f}", end="\n\n")

                self.replay_buffer.limit_history(
                    action=True,
                    state=True,
                    next_state=True,
                    reward=True,
                    done=True,
                )

                if done:
                    break

            self.replay_buffer.save_to_history(episode_reward=episode_reward)
            self.replay_buffer.limit_history(episode_reward=True)
            running_reward = self.replay_buffer.episode_rewards_mean()

            if running_reward > 500:
                print(f"Solved at episode {episode_count}")
                break
