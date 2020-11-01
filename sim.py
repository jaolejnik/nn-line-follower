from simulation.sim_env import SimEnv
from utils.enums import Actions

simulation = SimEnv()

for i in range(50):
    simulation.step(Actions.MOVE_FORWARD)
