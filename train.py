from learning.dqn.deep_q_learning import DeepQLearningClient
from tensorflow.keras import optimizers

q_learn = DeepQLearningClient(
    learning_rate=0.00015,
    greed_min=0.1,
    discount_rate=0.99,
    update_after_actions=1,
    visual_after_episodes=100,
    update_target_after_actions=25000,
    max_episodes=759,
    siec=(4, 16, 16, 5),
)
q_learn.run()
