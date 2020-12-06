from tensorflow.keras import Model, layers

from utils.enums import Actions

number_of_actions = len([action for action in Actions])


def create_q_model():
    inputs = layers.Input(shape=(4,))
    hidden_layer_1 = layers.Dense(16, activation="relu")(inputs)
    hidden_layer_2 = layers.Dense(16, activation="relu")(hidden_layer_1)
    outputs = layers.Dense(number_of_actions, activation="linear")(hidden_layer_2)

    return Model(inputs=inputs, outputs=outputs)
