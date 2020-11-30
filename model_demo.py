from learning.dqn.model_replay import ModelReplay
import glob

models_path = glob.glob("saved_data/interesting_models/G188_METAAAAA")
models_path = sorted(models_path, key=lambda x: int(x.split("/")[-1]))

for model_path in models_path:
    print(model_path)
    model = ModelReplay(model_path)
    model.run()
