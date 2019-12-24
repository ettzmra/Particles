import pygame, sys, random
from math import sqrt

class MovingObj:
    def __init__(self, x, y, vx=0, vy=0):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy

    def add(self, stepx, stepy, randomx=0, randomy=0):
        xrandom = random.uniform(-randomx, randomx)
        yrandom = random.uniform(-randomy, randomy)
        self.newx, self.newy = self.x + stepx + xrandom, self.y + stepy + yrandom

    def sub(self, stepx, stepy, randomx=0, randomy=0):
        xrandom = random.uniform(-randomx, randomx)
        yrandom = random.uniform(-randomy, randomy)
        self.diffx, self.diffy = stepx + xrandom - self.x, stepy + yrandom - self.y

    def direction(self, targetx, targety):  # determines the direction of a vector
        self.sub(targetx, targety)
        if self.x != 0:
            direction_x = self.diffx // abs(self.diffx)
        else:
            direction_x = 0
        if self.y != 0:
            direction_y = self.diffy // abs(self.diffy)
        else:
            direction_y = 0
        return direction_x, direction_y

    # def multiply(self, num):
    #     self.x, self.y = self.x * num, self.y * num

    def magnitude(self, targetx, targety):  # distance between two points
        self.sub(targetx, targety)
        self.distance = sqrt((self.diffx ** 2) + (self.diffy ** 2))

    def check_edges(self, sink_list, screenw, screenh):
        for sink in sink_list:
            self.magnitude(sink.x, sink.y)
            if self.distance < sink.mass:
                return self
        if (0 > self.x > screenw) or (0 > self.y > screenh):
            return self

    def limit(self, num):
        pass

class Emitter(MovingObj):
    def __init__(self, x, y, particle_amount, vx=0, vy=0):
        super().__init__(x, y, vx, vy)
        self.amount = particle_amount


    def emit(self):  # dx, dy, randomx=0, randomy=0):
        particles = []
        for i in range(self.amount):
            #xrandom = random.uniform(-randomx, randomx)
            #yrandom = random.uniform(-randomy, randomy)
            particles.append(Particle(self.x, self.y)) # dx+xrandom, dy+yrandom))
        return particles


class Particle(MovingObj):
    def __init__(self, x, y):
        super().__init__(x, y)
        #self.start_point = self.x, self.y = x, y


class Sink(MovingObj):
    def __init__(self, x, y, mass):
        super().__init__(x, y)
        self.x, self.y, self.mass = x, y, mass

pygame.init()
clock = pygame.time.Clock()
size = width, height = 640, 480
BLACK, WHITE  = (0, 0, 0), (255, 255, 255)

screen = pygame.display.set_mode(size)
pygame.font.init()
font = pygame.font.SysFont('Courier New', 30)

emitters = []
particle_pool = []
sinks = []

emitters.append(Emitter(100, 100, 10))

sinks.append(Sink(100, 300, 20))
sinks.append(Sink(300, 100, 20))
sinks.append(Sink(300, 300, 10))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(WHITE)

    for emitter in emitters:
        new_particles = emitter.emit()
        particle_pool.append(new_particles)
        # emove = Mover(0.1, 0.1, 0.0001, 0.0001)
        # check_edges(emitter, sinks, width, height)

    pmove = 1
