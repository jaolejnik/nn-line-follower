from tensorflow.keras import optimizers

from learning.dqn.deep_q_learning import DeepQLearningClient
from learning.dqn.model_replay import ModelReplay

# test = ModelReplay("saved_data/dqn/2020-11-22_12-2/models/551")
# test.run()

q_learn = DeepQLearningClient(
    learning_rate=0.01,
    update_after_actions=5,
)
q_learn.run()
