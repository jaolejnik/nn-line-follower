from robot.basic_movement import Movement
from robot.sensors import LineSensors

while LineSensors.right_sensor() or LineSensors.left_sensor():
    if not LineSensors.left_sensor():
        Movement.turn("RIGHT", "FORWARD", 50, 0.5, 0.2)
    if not LineSensors.right_sensor():
        Movement.turn("LEFT", "FORWARD", 50, 0.5, 0.2)

    if LineSensors.right_sensor() and LineSensors.left_sensor():
        Movement.move("FORWARD", 50, 0.2)
