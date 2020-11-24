from robot.nn_linefollower import NNLineFollower

robot = NNLineFollower(
    100, 0.05, "saved_data/dqn/the_best_551_2020-11-22_12-2/models/551"
)

robot.run()
