# Implementation of classic arcade game Pong

import tkinter
from tkinter import *
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [1.0, 1.0]
paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left


def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [1.0, 1.0]
    
    random_horizon = random.randrange (120, 240) / 60
    random_vertical = random.randrange (60, 180) / 60
    
    if direction == RIGHT:
        ball_vel = [random_horizon, - random_vertical] 
    elif direction == LEFT:
        ball_vel = [-random_horizon, - random_vertical]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(LEFT)
    score1 = 0
    score2 = 0
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [1.0, 1.0]
    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    canvas.delete('all')
        
    # draw mid line and gutters
    canvas.create_line(WIDTH / 2, 0,WIDTH / 2, HEIGHT, width=1, fill="White")
    canvas.create_line(PAD_WIDTH, 0,PAD_WIDTH, HEIGHT, width=1, fill="White")
    canvas.create_line(WIDTH - PAD_WIDTH, 0,WIDTH - PAD_WIDTH, HEIGHT, width=1, fill="White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]     
    
    
    if ball_pos[1] <= BALL_RADIUS: 
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
   

    # draw ball
    canvas.create_oval(ball_pos[0]-BALL_RADIUS,ball_pos[1]-BALL_RADIUS, ball_pos[0]+BALL_RADIUS,ball_pos[1]+BALL_RADIUS, width=2, fill="Blue", outline="White")

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= 0 and paddle1_pos + paddle1_vel <= 400-PAD_HEIGHT:
        paddle1_pos += paddle1_vel
        
    if paddle2_pos + paddle2_vel >= 0 and  paddle2_pos + paddle2_vel<= 400-PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.create_line(PAD_WIDTH/2, paddle1_pos, PAD_WIDTH/2, paddle1_pos +PAD_HEIGHT, width=PAD_WIDTH, fill='Red')
    canvas.create_line(WIDTH - PAD_WIDTH/2, paddle2_pos, WIDTH - PAD_WIDTH/2, paddle2_pos+PAD_HEIGHT, width=PAD_WIDTH, fill='Red')
    
    # determine whether paddle and ball collide    
    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH: 
        if (paddle1_pos + PAD_HEIGHT) >= ball_pos[1] >= paddle1_pos:
            ball_vel[0] = - ball_vel[0] * 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
        
    elif ball_pos[0] >= (WIDTH - (BALL_RADIUS + PAD_WIDTH)):
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= (paddle2_pos + PAD_HEIGHT): 
            ball_vel[0] = - ball_vel[0] * 1.1
        else:
            score1 +=1
            spawn_ball(LEFT)
    
    # draw scores
    
    
    canvas.create_text ((WIDTH/ 2) -80,40,text=str(score1),width=25, fill='White')
    canvas.create_text ((WIDTH/ 2) +80,40,text=str(score2), width=25, fill='White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    velocity = 5
    
    if key.keysym == "s":
        paddle1_vel = velocity
    elif key.keysym == "w":
        paddle1_vel = -velocity
        
    elif key.keysym == "Down":
        paddle2_vel = velocity
    elif key.keysym == "Up":
        paddle2_vel = -velocity
    else:
        paddle1_vel = 0
        paddle2_vel = 0
                
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key.keysym == "s":
        paddle1_vel = 0
    elif key.keysym == "w":
        paddle1_vel = 0
        
    elif key.keysym == "Down":
        paddle2_vel = 0
    elif key.keysym == "Up":
        paddle2_vel = 0
    else:
        paddle1_vel = 0
        paddle2_vel = 0

def restart():
    new_game()
    
def redraw():
    draw(canvas)
    root.after(20,redraw)
# create frame
#frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
root = Tk()
root.title("Pong")
root.geometry("{0}x{1}".format(WIDTH,HEIGHT+100))
frame = Frame(root,width=WIDTH,height=HEIGHT)
frame.bind("<KeyPress>",keydown)
frame.bind("<KeyRelease>",keyup)
frame.pack()
frame.focus_set()
#frame.set_draw_handler(draw)
canvas = Canvas(frame, width=WIDTH, height=HEIGHT, bg='black')
canvas.pack()
#button1 = frame.add_button('Restart', restart)
button1 = Button(root, text="Restart", command=restart)
button1.pack()
#frame.set_keydown_handler(keydown)
#frame.set_keyup_handler(keyup)
#

# start frame
new_game()
#frame.start()
root.after(20,redraw)
root.mainloop()
