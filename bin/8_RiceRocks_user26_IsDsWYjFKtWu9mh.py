# Spaceship program by Dennis van den Berg



### load modules ###

import simplegui
import math
import random



### globals ###

# default parameters for user interface, Ship, Missile and Rock objects
CANVAS_SIZE = (800, 600)
FRICTION_COEF = 0.01
ACCEL_COEF = 0.2
ANGLE_VEL_INCREMENT = 0.08
MISSILE_VEL = 3
MAX_NUMBER_OF_ROCKS = 12
MIN_RELATIVE_SPAWN_DISTANCE = 2
DIFFICULTY_INCREMENT = 0.5
MAX_LIVES = 3


## classes ##

# ImageInfo class
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        # initialisation
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        # coefficients that determine friction, acceleration, change of angle velocity and relative missile velocity
        self.friction_coef = FRICTION_COEF
        self.accel_coef = ACCEL_COEF
        self.angle_vel_increment = ANGLE_VEL_INCREMENT
        self.missile_vel = MISSILE_VEL

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        # draw spaceship (2 different versions based on value of self.thrust)
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # acceleration
        if self.thrust:
            for dim in range(len(self.pos)):
                self.vel[dim] += angle_to_vector(self.angle)[dim] * self.accel_coef
        
        # include friction
        for dim in range(len(self.pos)):
            self.vel[dim] *= (1 - self.friction_coef)

        # position
        for dim in range(len(self.pos)):
            self.pos[dim] = (self.pos[dim] + self.vel[dim]) % CANVAS_SIZE[dim]

        # angle
        self.angle += self.angle_vel

    def turn(self, direction):
        # increment angular velocity
        self.angle_vel += direction * self.angle_vel_increment

    def thrust_on(self, thrust):
        # set self.thrust to True or False
        self.thrust = thrust
        if self.thrust == True:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()

    def shoot(self):
        global missile_group
        a_missile = Sprite(
                           [self.pos[0] + angle_to_vector(self.angle)[0] * self.radius, self.pos[1] + angle_to_vector(self.angle)[1] * self.radius], 
                           [self.vel[0] + angle_to_vector(self.angle)[0] * self.missile_vel, self.vel[1] + angle_to_vector(self.angle)[1] * self.missile_vel], 
                           0, 
                           0, 
                           missile_image, 
                           missile_info, missile_sound
                           )
        missile_group.add(a_missile)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self, canvas):
        if self.animated:
            offset = self.age * self.image_size[0]
        else:
            offset = 0
        canvas.draw_image(self.image, [self.image_center[0] + offset, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # position
        for dim in range(len(self.pos)):
            self.pos[dim] = (self.pos[dim] + self.vel[dim]) % CANVAS_SIZE[dim]
        # angle
        self.angle += self.angle_vel
        # age
        self.age += 1
        # return True if expired
        return not (self.age < self.lifespan)

    def collide(self, other_object):
        # return True in case of overlap
        return dist(self.get_position(), other_object.get_position()) < self.get_radius() + other_object.get_radius()
        

    
## helper functions ##

# load images and sounds
def load_resources():
    global debris_info, debris_image, nebula_info, nebula_image, splash_info, splash_image, ship_info, ship_image, missile_info, missile_image, asteroid_info, asteroid_image, explosion_info, explosion_image, soundtrack, missile_sound, ship_thrust_sound, explosion_sound
    
    # art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
    # debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
    #                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
    debris_info = ImageInfo([320, 240], [640, 480])
    debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
    
    # nebula images - nebula_brown.png, nebula_blue.png
    nebula_info = ImageInfo([400, 300], [800, 600])
    nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")
    
    # splash image
    splash_info = ImageInfo([200, 150], [400, 300])
    splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
    
    # ship image
    ship_info = ImageInfo([45, 45], [90, 90], 35)
    ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
    
    # missile image - shot1.png, shot2.png, shot3.png
    missile_info = ImageInfo([5,5], [10, 10], 3, 50)
    missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
    
    # asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
    asteroid_info = ImageInfo([45, 45], [90, 90], 40)
    asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
    
    # animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
    explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
    explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
    
    # sound assets purchased from sounddogs.com, please do not redistribute
    soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
    missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
    missile_sound.set_volume(.5)
    ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
    explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# reset game
def reset_game():
    global timer, started, score, lives, time, rock_group, missile_group, explosion_group, my_ship
    timer.stop()
    started = False
    rock_group = set([])
    missile_group = set([])
    explosion_group = set([])
    my_ship = Ship([CANVAS_SIZE[0] / 2, CANVAS_SIZE[1] / 2], [0, 0], 0, ship_image, ship_info)

# initial game
def initial_game():
    global time, score, lives
    reset_game()
    time = 0.5
    score = 0
    lives = MAX_LIVES

# start game
def start_game():
    global timer, started, score, lives
    timer.start()
    started = True
    score = 0
    lives = MAX_LIVES
    soundtrack.rewind()
    soundtrack.play()
    
# convert angle to vector
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

# calculate distance between 2D points
def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# helper function to draw/update sprites in sprite_group
def process_sprite_group(sprite_group, canvas):
    for sprite in set(sprite_group):
        sprite.draw(canvas)
        # update and remove sprite if expired
        if sprite.update():
            sprite_group.remove(sprite)

# check for collisions between sprites in sprite_group and other_object
def group_collide(sprite_group, other_object):
    collision = False
    for sprite in set(sprite_group):
        if sprite.collide(other_object):
            sprite_group.remove(sprite)
            an_explosion = Sprite(other_object.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
            collision = True
    return collision

# check for collisions between sprites in sprite_group_1 and sprite_group_2
def group_group_collide(sprite_group_1, sprite_group_2):
    number_of_collisions = 0
    for sprite_1 in set(sprite_group_1):
        if group_collide(sprite_group_2, sprite_1):
            sprite_group_1.discard(sprite_1)
            number_of_collisions += 1
    return number_of_collisions

# function to increase difficulty with increasing score
def spawn_speed_function(score):
    return math.sqrt(DIFFICULTY_INCREMENT * score + 1)



## handler functions ##

# draw handler (including updates)
def draw(canvas):
    global time, lives, score
    
    # animate background
    time += 1
    wtime = (time / 4) % CANVAS_SIZE[0]
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [CANVAS_SIZE[0] / 2, CANVAS_SIZE[1] / 2], [CANVAS_SIZE[0], CANVAS_SIZE[1]])
    canvas.draw_image(debris_image, center, size, (wtime - CANVAS_SIZE[0] / 2, CANVAS_SIZE[1] / 2), (CANVAS_SIZE[0], CANVAS_SIZE[1]))
    canvas.draw_image(debris_image, center, size, (wtime + CANVAS_SIZE[0] / 2, CANVAS_SIZE[1] / 2), (CANVAS_SIZE[0], CANVAS_SIZE[1]))

    # draw/update ship
    my_ship.draw(canvas)
    my_ship.update()

    # draw/update rocks in rock_group
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)

    # handle collision between rocks in rock_group and my_ship
    if group_collide(rock_group, my_ship):
        lives -= 1

    # handle collisions between rocks and missiles
    score += group_group_collide(rock_group, missile_group)

    # draw lives and score
    canvas.draw_text("Lives: " + str(lives), (40, 50), 25, 'White')
    canvas.draw_text("Score: " + str(score), (CANVAS_SIZE[0] - 120, 50), 25, 'White')

    # check for game over
    if lives <= 0 and started:
        reset_game()

    # draw splash screen if not yet started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [CANVAS_SIZE[0] / 2, CANVAS_SIZE[1] / 2], [CANVAS_SIZE[0], CANVAS_SIZE[1]])

# key handlers
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.turn(-1)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.turn(1)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust_on(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
    
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.turn(1)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.turn(-1)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust_on(False)

# mouseclickhandler to start game
def mouseclick(position):
    if not started:
        start_game()

# timer handler that spawns a rock with random parameters
def rock_spawner():
    global rock_group
    if len(rock_group) < MAX_NUMBER_OF_ROCKS:
        max_spawn_speed = spawn_speed_function(score)
        a_rock = Sprite(
                        [random.random() * CANVAS_SIZE[0], random.random() * CANVAS_SIZE[1]],
                        [max_spawn_speed * random.random() - 1, max_spawn_speed * random.random() - 1],
                        random.random() * 2 * math.pi,
                        (2 * random.random() - 1) * 0.05,
                        asteroid_image,
                        asteroid_info
                       )
        if dist(a_rock.get_position(), my_ship.get_position()) > MIN_RELATIVE_SPAWN_DISTANCE * (a_rock.get_radius() + my_ship.get_radius()):
            rock_group.add(a_rock)



## load resources, initialize frame, register handlers, initialize game ##

# load images and sounds
load_resources()

# initialize frame
frame = simplegui.create_frame("Asteroids", CANVAS_SIZE[0], CANVAS_SIZE[1])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouseclick)
timer = simplegui.create_timer(1000.0, rock_spawner)

# initialize game parameters
initial_game()



## start frame ##

frame.start()
