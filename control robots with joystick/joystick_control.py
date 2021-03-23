import pygame
import urx
import time
from changingtek import ZXHand

'''
functons to be used which can make this .py better

robot.translate([0.01, 0.01, 0.01], wait=0) 同时在三个方向移动的指令

robot.movej(angular_pos, acc=acc, vel=vel, wait=0 ) 关节空间的运动，angular_pos是用数组形式表示的六个关节弧度位置

rob.speedl_tool((0, 0, -v, 0, 0, 0), acc=a, min_time=3)，与它搭配的指令如下：print("moving in tool -z using speed command")

rob.speedl()
 print("Moving through several points with a radius")
        wait()
        pose[0] -= l
        p1 = pose[:]
        pose[2] -= l
        p2 = pose[:]
        rob.movels([p1, p2], vel=v, acc=a, radius=r)

attention
    this program can be used on xbox series and PS series, even all joysticks that can communicate with pygame can use this .py,
    all you need to do is give right function to different keys;
    many functions with annotations below can make this file better, but to make it work easier on Raspberry Pi, I did not use them.
    这个程序并不只是适配xbox360手柄，对于常见手柄比如xbox系列，PS系列都可以，
    甚至说，凡是pygame库能读到的手柄都可以
'''

hand = ZXHand(ip = '192.168.1.20') #connect to end effector

robot = urx.Robot("192.168.1.100") #connect computer and UR3; PC通过网线与UR通信，注意网段

r = robot
robot.set_payload(2, (0, 0, 0)) #set parameters about forse; 设置力相关，有时候通过改大一些第一个参数可以解决一些报错问题
l = 0.01  # distance m
rad = 1 # rad/s
v =0.5 # m/s
a = 0.5 # acc m/s2
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

''' 
This is a simple class that will help us print to the screen
It has nothing to do with the joysticks, just outputting the
information.
you can delete information below(line51-72) if it is not necessary for you. 下面的这个类是用来把手柄的一些信息通过一个窗口打印出来的，其实没什么用，可以删掉
'''

# class TextPrint:
#     def __init__(self):
#         self.reset()
#         self.font = pygame.font.Font(None, 27)
#
#     def print(self, screen, textString):
#         textBitmap = self.font.render(textString, True, BLACK)
#         screen.blit(textBitmap, [self.x, self.y])
#         self.y += self.line_height
#
#     def reset(self):
#         self.x = 150
#         self.y = 10
#         self.line_height = 32
#
#     def indent(self):
#         self.x += 10
#
#     def unindent(self):
#         self.x -= 10

pygame.init()

# #设置显示出来的小窗口的大小
# size = [500, 600]
#
# screen = pygame.display.set_mode(size)
#
# pygame.display.set_caption("知行机器人")# title of window
#
# # Loop until the user clicks the close button.
done = False
#
# # Used to manage how fast the screen updates
# clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
#textPrint = TextPrint()

# -------- Main Program Loop -----------
while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYSTICK AXIS MOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
    # if event.type == pygame.JOYBUTTONDOWN:
    #    print("Joystick button pressed.")
    # if event.type == pygame.JOYBUTTONUP:
    #    print("Joystick button released.")

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    #screen.fill(WHITE)
    #textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    #textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        # textPrint.print(screen, "Joystick {}".format(i) )
        # textPrint.indent()

        # Get the name from the OS for the controller/joystick
        # name = joystick.get_name()
        # textPrint.print(screen, "Joystick name: {}".format(name) )

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        
        axes = joystick.get_numaxes()
        
        # textPrint.print(screen, "Number of axes: {}".format(axes) )
        # textPrint.indent()
        
        # get input from joystick 
        for i in range(axes):
            axis = joystick.get_axis(i)
            #textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis))
            if i == 1 and axis == -1.0:
                print("end forward")
                pose = [0, 0, 0, 0, 0, 0]
                pose[1] += l #增量式赋值
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2) # 注释掉这句之后，发现顿挫感降低了，但是没法通过十字键调速了
            if i == 1 and axis > 0.3:
                print("end back")
                pose = [0, 0, 0, 0, 0, 0]
                pose[1] -= l
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2)
            if i == 0 and axis == -1:
                print("end left")
                pose = [0, 0, 0, 0, 0, 0]
                pose[0] += l
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2)
            if i == 0 and axis > 0.3:
                print("end right")
                pose = [0,0,0,0,0,0]
                pose[0] -= l
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2)
            if i == 4 and axis == -1.0:
                print("end joint rotation align X+")
                pose = [0, 0, 0, 0, 0, 0]
                pose[3] += 0.1
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2)
            if i == 4 and axis > 0.3:
                print("end joint rotation align X-")
                pose = [0, 0, 0, 0, 0, 0]
                pose[3] -= 0.1
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2)
            if i == 3 and axis == -1:
                print("end joint rotation align Y-")
                pose = [0, 0, 0, 0, 0, 0]
                pose[4] -= 0.1
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2)
            if i == 3 and axis > 0.3:
                print("end joint rotation align Y+")
                pose = [0, 0, 0, 0, 0, 0]
                pose[4] += 0.1
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2)
            if i == 2 and axis > 0.995:
                print("end down")
                pose = [0, 0, 0, 0, 0, 0]
                pose[2] += l
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2)
            if i == 2 and axis < -0.995:
                print("end up")
                pose = [0,0,0,0,0,0]
                pose[2] -= l
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2)

        #textPrint.unindent()

        buttons = joystick.get_numbuttons()
        #textPrint.print(screen, "Number of buttons: {}".format(buttons))
        #textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            #textPrint.print(screen, "Button {:>2} value: {}".format(i, button))
            if i == 2 and button == 1:
                print("locate")
                pose = robot.getl()# get position
                robot.movej([1.807986, -1.839926, -1.055226, -1.782155, 1.6023867, 0], acc=a, vel=1, wait=0)#wait=0不要改
            if i == 3 and button == 1:
                print("achieve")
                robot.movel_tool([0,0,-0.05,0,0,0], acc=a, vel=0.5, wait=0)
                time.sleep(0.5)
                robot.movej([0.813847, -1.4069, -1.85842, -0.3303, 1.556, 0], acc=a, vel=1, wait=0)
            if i == 4 and button == 1:
                print("contrarotate")
                pose = [0,0,0,0,0,0]
                pose[5] -= 0.2
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2)
            if i == 5 and button == 1:
                print("clockwise rotation")
                pose = [0,0,0,0,0,0]
                pose[5] += 0.2
                robot.movel_tool(pose, acc=a, vel=v, wait=0)
                time.sleep(0.2)
            if i == 6 and button == 1:
                print("BACK")#not used
            if i == 7 and button == 1:
                print("START")#not used
            if i == 8 and button == 1:
                print("move to a pose")
                robot.movej([0, -1.57, -1.57, -1.57, 1.57, 0], acc=a, vel=1, wait=0)

        #textPrint.unindent()

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        
        hats = joystick.get_numhats()
        #textPrint.print(screen, "Number of hats: {}".format(hats))
        #textPrint.indent()

        # setting parameters about l rad v a
        for i in range(hats):
            hat = joystick.get_hat(i)
            #textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)))
            if hat == (1, 0):
                l = l - 0.005
                step = 100 * l
                print("step=%.2fcm" %step)#减少末端移动距离并打印
                time.sleep(0.2)
            if hat == (-1, 0):
                l = l + 0.01
                step = 100 * l
                print("step=%.2fcm" %step)#增加移动距离并打印
                time.sleep(0.2)
            if hat == (0, 1):
                v = v + 0.01
                velocity = 1000 * v
                print("V = %.1fmm/s" %velocity)#增加移动速度并打印
                time.sleep(0.2)
            if hat == (0, -1):
                v = v - 0.005
                velocity = 1000 * v
                print("V = %.1fmm/s" %velocity)#减少移动速度并打印
                time.sleep(0.2)
        #textPrint.unindent()

        #textPrint.unindent()

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    #pygame.display.flip()

    # Limit to 20 frames per second
    #clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
