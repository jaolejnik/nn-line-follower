# from robot.linefollower import LineFollower

# robot = LineFollower(100, 0.05)

# robot.run()
# robot.action_manager.reverse_actions()
# robot.action_manager.perform_saved_actions()

from learning.q_learning import QLearningClient

test = QLearningClient()
print(test.q_table)
