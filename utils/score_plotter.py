import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class ScorePlotter:
    def __init__(self, model_name, scores_filepath):
        self.scores_filepath = scores_filepath
        self.plots_filepath = os.path.join(
            os.path.dirname(self.scores_filepath), "plots"
        )
        self.model_name = model_name
        if not os.path.exists(self.plots_filepath):
            os.makedirs(self.plots_filepath)

    def load_scores(self):
        self.data = pd.read_csv(self.scores_filepath)

    def _base_plot(
        self, x_keys, y_keys, x_label, y_label, name_prefix, colors=["blue"]
    ):
        fig, ax = plt.subplots(1, 1)
        for x_key, y_key, color in zip(x_keys, y_keys, colors):
            ax.plot(self.data[x_key], self.data[y_key], color=color)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid()
        fig.savefig(
            os.path.join(self.plots_filepath, f"{name_prefix}_{self.model_name}")
        )

    def plot_episode_reward(self):
        self._base_plot(
            ["Episode"],
            ["Episode reward"],
            "Epizod",
            "Nagroda za epizod",
            "episode_reward",
        )

    def plot_running_reward(self):
        self._base_plot(
            ["Episode"],
            ["Running reward"],
            "Epizod",
            "Średnia nagroda z zapisanej pamięci",
            "running_reward",
            ["orange"],
        )

    def plot_actions(self):
        self._base_plot(
            ["Episode"] * 3,
            ["Total actions", "Exploration actions", "Exploitation actions"],
            "Epizod",
            "Podjęte akcje",
            "actions",
            ["blue", "orange", "green"],
        )

    def plot_greed_rate(self):
        self._base_plot(
            ["Episode"],
            ["Greed rate"],
            "Epizod",
            "Współczynnik chciwości",
            "greed_rate",
            ["red"],
        )

    def plot_all(self):
        self.plot_episode_reward()
        self.plot_running_reward()
        self.plot_actions()
        self.plot_greed_rate()
