from time import sleep

from robot.basic_movement import DirectionX, DirectionY, Movement, MovementManager
from robot.sensors import CollisionSensors, LineSensors

manager = MovementManager()

while LineSensors.right_sensor() or LineSensors.left_sensor():
    if CollisionSensors.front_distance() < 5:
        break
    while not LineSensors.left_sensor():
        manager.add_action(
            Movement.turn,
            direction_x=DirectionX.RIGHT,
            direction_y=DirectionY.FORWARD,
            speed=75,
            sharpness=0.05,
            time=0.05,
        )
        manager.perform_action(
            Movement.turn,
            direction_x=DirectionX.RIGHT,
            direction_y=DirectionY.FORWARD,
            speed=75,
            sharpness=0.05,
            time=0.05,
        )
    while not LineSensors.right_sensor():
        manager.add_action(
            Movement.turn,
            direction_x=DirectionX.LEFT,
            direction_y=DirectionY.FORWARD,
            speed=75,
            sharpness=0.05,
            time=0.05,
        )
        manager.perform_action(
            Movement.turn,
            direction_x=DirectionX.LEFT,
            direction_y=DirectionY.FORWARD,
            speed=75,
            sharpness=0.05,
            time=0.05,
        )
    while LineSensors.right_sensor() and LineSensors.left_sensor():
        manager.add_action(
            Movement.move,
            direction_y=DirectionY.FORWARD,
            speed=75,
            time=0.05,
        )
        manager.perform_action(
            Movement.move,
            direction_y=DirectionY.FORWARD,
            speed=75,
            time=0.05,
        )

manager.save_actions()
sleep(1)
manager.reverse_actions()
manager.perform_saved_actions()
