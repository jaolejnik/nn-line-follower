from learning.dqn.deep_q_learning import DeepQLearningClient

q_learn = DeepQLearningClient(
    learning_rate=0.00025,
    update_after_actions=1,
    visual_after_episodes=10,
    update_target_after_actions=10000,
)
q_learn.run()
