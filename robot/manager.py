import json

from robot.basic_movement import Movement


class MovementManager:
    def __init__(self):
        self.data = {"actions": []}

    def save_actions(self):
        with open("movement_actions.json", "w") as action_file:
            action_file.write(json.dumps(self.data))

    def add_action(self, action, **kwargs):
        action_type = action.__name__
        action_args = kwargs
        action_dict = {"type": action_type, "args": action_args}

        self.data["actions"].append(action_dict)

    def load_actions(self, filename):
        with open("movement_actions.json") as action_file:
            self.data = json.load(action_file)

    def reverse_actions(self):
        for action in self.data["actions"]:
            if action["type"] == "rotate":
                action["args"]["direction_x"] = not action["args"]["direction_x"]
            else:
                action["args"]["direction_y"] = not action["args"]["direction_y"]
        self.data["actions"].reverse()

    def perform_action(self, action, **kwargs):
        action_type = action if type(action) == str else action.__name__
        arg_string = ", ".join([f"{key}={value}" for key, value in kwargs.items()])
        command = f"Movement.{action_type}({arg_string})"
        eval(command)

    def perform_saved_actions(self):
        for action in self.data["actions"]:
            self.perform_action(action["type"], **action["args"])

    def add_and_save_action(self, action, **kwargs):
        self.add_action(action, **kwargs)
        self.perform_action(action, **kwargs)
