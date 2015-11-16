# Implementation of classic arcade game Pong

# import modules
import simplegui
import random


# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600.0
HEIGHT = 400.0
BALL_RADIUS = 20.0
PAD_WIDTH = 8.0
PAD_HEIGHT = 80.0
HALF_PAD_WIDTH = PAD_WIDTH / 2.0
HALF_PAD_HEIGHT = PAD_HEIGHT / 2.0
LEFT = False
RIGHT = True
TIMESTEP = 0.01


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    # start position
    ball_pos = [WIDTH / 2.0, HEIGHT / 2.0]
    
    # start velocity
    if direction == RIGHT:
        ball_vel_x = random.randrange(120, 240)
    else:
        ball_vel_x = -random.randrange(120, 240)

    ball_vel_y = -(random.randrange(60, 180))
    ball_vel = [ball_vel_x, ball_vel_y]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2.0
    paddle2_pos = HEIGHT / 2.0
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    score1 = 0
    score2 = 0

    # spawn ball with random direction
    direction = random.choice([LEFT, RIGHT])
    spawn_ball(direction)


def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel

    # draw mid line and gutters
    c.draw_line([WIDTH / 2.0, 0.0],[WIDTH / 2.0, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0.0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0.0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += TIMESTEP * ball_vel[0]
    ball_pos[1] += TIMESTEP * ball_vel[1]
    
    # bounce off walls
    if ball_pos[1] <= BALL_RADIUS:
        ball_pos[1] = 2.0 * BALL_RADIUS - ball_pos[1] 
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_pos[1] = 2.0 * (HEIGHT - BALL_RADIUS) - ball_pos[1]
        ball_vel[1] = -ball_vel[1]

    # check for touching gutter or paddles und update score
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_pos[0] = 2.0 * (PAD_WIDTH + BALL_RADIUS) - ball_pos[0]
            ball_vel[0] = -ball_vel[0]
        else:
            score2 += 1
            spawn_ball(RIGHT)
    if ball_pos[0] >= WIDTH - (PAD_WIDTH + BALL_RADIUS):
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_pos[0] = 2.0 * (WIDTH - (PAD_WIDTH + BALL_RADIUS)) - ball_pos[0]
            ball_vel[0] = -ball_vel[0]
        else:
            score1 += 1
            spawn_ball(LEFT)
    
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')
    
    # update paddle's vertical position
    paddle1_pos += TIMESTEP * paddle1_vel
    paddle2_pos += TIMESTEP * paddle2_vel

    # keep paddles on the screen
    paddle1_pos = max(HALF_PAD_HEIGHT, min(paddle1_pos, HEIGHT - HALF_PAD_HEIGHT))
    paddle2_pos = max(HALF_PAD_HEIGHT, min(paddle2_pos, HEIGHT - HALF_PAD_HEIGHT))
    
    # draw paddles
    c.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, 'White')
    c.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH, 'White')

    # draw scores
    c.draw_text(str(score1), [WIDTH / 4.0, HEIGHT / 6.0], 50, 'White')
    c.draw_text(str(score2), [3.0 * WIDTH / 4.0, HEIGHT / 6.0], 50, 'White')


def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -200.0
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = +200.0
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -200.0
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = +200.0
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0.0
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0.0
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0.0
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0.0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)


# start frame
new_game()
frame.start()

