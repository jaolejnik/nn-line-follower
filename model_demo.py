from learning.dqn.model_replay import ModelReplay
from simulation.sim_env import SimEnv
import glob

models_paths = glob.glob("saved_data/interesting_models/G188_METAAAAA")
# models_paths = sorted(models_paths, key=lambda x: int(x.split("/")[-1]))

tracks_paths = glob.glob("simulation/assets/track_finish_5*")
print(tracks_paths)
tracks_names = [x.split("/")[-1] for x in tracks_paths]

print(tracks_names)

for model_path in models_paths:
    for track_path in tracks_names:
        model = ModelReplay(model_path, track_path)
        model.run()
