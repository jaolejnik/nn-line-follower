from robot.programmed_linefollower import ProgrammedLineFollower

# robot = NNLineFollower(
#     100, 0.05, "saved_data/dqn/the_best_551_2020-11-22_12-2/models/551"
# )

robot = ProgrammedLineFollower(100, 0.05)

robot.run()
