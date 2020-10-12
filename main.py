from time import sleep

from robot.basic_movement import DirectionX, DirectionY, Movement, MovementManager
from robot.sensors import LineSensors

manager = MovementManager()

while LineSensors.right_sensor() or LineSensors.left_sensor():
    while not LineSensors.left_sensor():
        manager.add_action(
            Movement.turn,
            direction_x=DirectionX.RIGHT,
            direction_y=DirectionY.FORWARD,
            speed=100,
            sharpness=0.25,
            time=0.1,
        )
        manager.perform_action(
            Movement.turn,
            direction_x=DirectionX.RIGHT,
            direction_y=DirectionY.FORWARD,
            speed=100,
            sharpness=0.25,
            time=0.1,
        )
    while not LineSensors.right_sensor():
        manager.add_action(
            Movement.turn,
            direction_x=DirectionX.LEFT,
            direction_y=DirectionY.FORWARD,
            speed=100,
            sharpness=0.25,
            time=0.1,
        )
        manager.perform_action(
            Movement.turn,
            direction_x=DirectionX.LEFT,
            direction_y=DirectionY.FORWARD,
            speed=100,
            sharpness=0.25,
            time=0.1,
        )
    while LineSensors.right_sensor() and LineSensors.left_sensor():
        manager.add_action(
            Movement.move,
            direction_y=DirectionY.FORWARD,
            speed=100,
            time=0.1,
        )
        manager.perform_action(
            Movement.move,
            direction_y=DirectionY.FORWARD,
            speed=100,
            time=0.1,
        )

manager.save_actions()
sleep(1)
manager.reverse_actions()
manager.perform_saved_actions()
