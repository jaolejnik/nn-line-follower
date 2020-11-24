from learning.dqn.deep_q_learning import DeepQLearningClient

q_learn = DeepQLearningClient(
    learning_rate=0.01,
    update_after_actions=5,
)
q_learn.run()
