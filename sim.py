from learning.q_learning import QLearningClient
from utils.enums import Actions

q_learn = QLearningClient()

q_learn.learn(1000, 1000000)
