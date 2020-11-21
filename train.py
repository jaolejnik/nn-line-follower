from tensorflow.keras import optimizers

from learning.dqn.deep_q_learning import DeepQLearningClient
from learning.dqn.model_replay import ModelReplay

test = ModelReplay(
    "saved_data/dqn/good_2020-11-19_14-1/models/petla_odwrotnie_3827.455"
)
test.run()

# q_learn = DeepQLearningClient(
#     learning_rate=0.01,
#     update_after_actions=5,
# )
# q_learn.run()
