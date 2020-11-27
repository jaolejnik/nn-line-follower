from learning.dqn.model_replay import ModelReplay
import glob

models_path = glob.glob(
    "saved_data/dqn/spoko_ale_za_nagrody_dla_dodatkowych_stanow_2020-11-27_16-22/models/*"
)


models_path = sorted(models_path, key=lambda x: int(x.split("/")[-1]))
print(models_path)

for model_path in models_path:
    model = ModelReplay(model_path)
    model.run(1000)
