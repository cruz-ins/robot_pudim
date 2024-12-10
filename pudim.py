from bluedot import BlueDot
from gpiozero import Robot
from signal import pause

robot = Robot(left=(22, 23), right=(27, 24))
    
def move(pos):
    if pos.top:
        robot.forward()
        print("top")
    elif pos.bottom:
        robot.backward()
        print("bottom")
    elif pos.left:
        robot.left()
        print("left")
    elif pos.right:
        robot.right()
        print("right")

def stop():
    robot.stop()

bd = BlueDot()

bd.when_pressed = move
bd.when_moved = move
bd.when_released = stop
pause()    
