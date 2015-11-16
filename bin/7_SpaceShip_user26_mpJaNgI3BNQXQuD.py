# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
CANVAS_SIZE = (800, 600)
score = 0
lives = 3
time = 0.5
# default parameters for Ship objects
FRICTION_COEF = 0.01
ACCEL_COEF = 0.2
ANGLE_VEL_INCREMENT = 0.05
MISSILE_VEL = 3

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


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


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
        global a_missile
        a_missile = Sprite(
                           [self.pos[0] + angle_to_vector(self.angle)[0] * self.radius, self.pos[1] + angle_to_vector(self.angle)[1] * self.radius], 
                           [self.vel[0] + angle_to_vector(self.angle)[0] * self.missile_vel, self.vel[1] + angle_to_vector(self.angle)[1] * self.missile_vel], 
                           0, 
                           0, 
                           missile_image, 
                           missile_info, missile_sound
                           )

        
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
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # position
        for dim in range(len(self.pos)):
            self.pos[dim] = (self.pos[dim] + self.vel[dim]) % CANVAS_SIZE[dim]

        # angle
        self.angle += self.angle_vel

           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % CANVAS_SIZE[0]
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [CANVAS_SIZE[0] / 2, CANVAS_SIZE[1] / 2], [CANVAS_SIZE[0], CANVAS_SIZE[1]])
    canvas.draw_image(debris_image, center, size, (wtime - CANVAS_SIZE[0] / 2, CANVAS_SIZE[1] / 2), (CANVAS_SIZE[0], CANVAS_SIZE[1]))
    canvas.draw_image(debris_image, center, size, (wtime + CANVAS_SIZE[0] / 2, CANVAS_SIZE[1] / 2), (CANVAS_SIZE[0], CANVAS_SIZE[1]))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # draw lives and score
    canvas.draw_text("Lives: " + str(lives), (40, 50), 20, 'Red')
    canvas.draw_text("Score: " + str(score), (CANVAS_SIZE[0] - 120, 50), 20, 'Red')

    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
            

# timer handler that spawns a rock with random parameters
def rock_spawner():
    global a_rock
    a_rock = Sprite(
                    [random.random() * CANVAS_SIZE[0], random.random() * CANVAS_SIZE[1]],
                    [2 * random.random() - 1, 2 * random.random() - 1],
                    random.random() * 2 * math.pi,
                    (2 * random.random() - 1) * 0.05,
                    asteroid_image,
                    asteroid_info
                    )


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


# initialize frame
frame = simplegui.create_frame("Asteroids", CANVAS_SIZE[0], CANVAS_SIZE[1])

# initialize ship and two sprites
my_ship = Ship([CANVAS_SIZE[0] / 2, CANVAS_SIZE[1] / 2], [0, 0], 0, ship_image, ship_info)
rock_spawner()
my_ship.shoot()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
