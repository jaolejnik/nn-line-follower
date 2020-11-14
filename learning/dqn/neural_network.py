from tensorflow.keras import Model, layers

from utils.enums import Actions

number_of_actions = len([action for action in Actions])


def create_q_model():
    inputs = layers.Input(shape=(4, 1))
    hidden_layer = layers.Dense(4, activation="relu")(inputs)
    outputs = layers.Dense(number_of_actions, activation="softmax")(hidden_layer)

    return Model(inputs=inputs, outputs=outputs)
