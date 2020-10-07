from basic_movement import Movement
from sensors import LineSensors

while True:
    if not LineSensors.left_sensor():
        Movement.turn("RIGHT", "FORWARD", 50, 0.5, 0.2)
    elif not LineSensors.right_sensor():
        Movement.turn("LEFT", "FORWARD", 50, 0.5, 0.2)
    else:
        Movement.move("FORWARD", 50, 0.2)