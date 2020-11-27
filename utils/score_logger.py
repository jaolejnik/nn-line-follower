import os

VALUES_TO_LOG = (
    "Episode",
    "Episode reward",
    "Running reward",
    "Total actions",
    "Exploration actions",
    "Exploitation actions",
    "Greed rate",
    "Loss",
)


class ScoreLogger:
    def __init__(self, name, path=""):
        self.filepath = os.path.join(path, f"score_{name}.csv")
        self.header = ",".join(VALUES_TO_LOG)
        self._init_file(path)

    def _init_file(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(self.filepath, "w") as f:
            f.write(self.header + "\n")

    def save_scores(self, values_tuple):
        string_values = tuple(map(str, values_tuple))
        row = ",".join(string_values)
        with open(self.filepath, "a") as f:
            f.write(row + "\n")
