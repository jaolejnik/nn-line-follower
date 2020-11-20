from tensorflow.keras import optimizers

from learning.dqn.deep_q_learning import DeepQLearningClient

OPT = [optimizers.Adam, optimizers.RMSprop]
LR = [0.1, 0.01]

for optimizer in OPT:
    for learning_rate in LR:
        q_learn_adam = DeepQLearningClient(
            optimizer=optimizer, learning_rate=learning_rate
        )
        q_learn_adam.run()
