import pygame, sys, random
from math import sqrt
import numpy as np

class MovingObj:
    def __init__(self, x, y, vx, vy):
        self.startpoint = self.x, self.y = x, y
        self.vx, self.vy = vx, vy

    def add_velocity(self, randomx=0, randomy=0):
        xrandom = random.uniform(-randomx, randomx)
        yrandom = random.uniform(-randomy, randomy)
        self.x, self.y = self.x + self.vx + xrandom, self.y + self.vy + yrandom

    def sub(self, stepx, stepy, randomx=0, randomy=0):
        xrandom = random.uniform(-randomx, randomx)
        yrandom = random.uniform(-randomy, randomy)
        self.diffx, self.diffy = stepx + xrandom - self.x, stepy + yrandom - self.y

    def find_direction(self, targetx, targety):  # normalize: determines the direction of a vector
        self.sub(targetx, targety)
        if self.diffx != 0:
            self.dx = self.diffx // abs(self.diffx)
        else:
            self.dx = 0
        if self.diffy != 0:
            self.dy = self.diffy // abs(self.diffy)
        else:
            self.dy = 0

    def magnitude(self, targetx, targety):  # distance between two points
        self.sub(targetx, targety)
        self.distance = sqrt((self.diffx ** 2) + (self.diffy ** 2))

    def out_of_borders(self, screenw, screenh, sink_list=None):
        if sink_list is not None:
            for sink in sink_list:
                self.magnitude(sink.x, sink.y)
                if self.distance < sink.mass:
                    self.x, self.y = self.startpoint
                    return True
        if 0 > self.x > screenw:
            self.vx = -self.vx
            return True
        if 0 > self.y > screenh:
            self.vy = -self.vy
            return True
        return False

    def limit(self, num):
        pass

class Emitter(MovingObj):
    def __init__(self, x, y, particle_amount, dx=1, dy=1, vx=0.0001, vy=0.0001):
        super().__init__(x, y, vx, vy)
        self.dx, self.dy = dx, dy
        self.amount = particle_amount


    def emit(self):
        particles = []
        for i in range(self.amount):
            xrandom = random.uniform(-1, 1)
            yrandom = random.uniform(-1, 1)
            particles.append(Particle(self.x, self.y, self.dx + xrandom, self.dy + yrandom))
        return particles


class Particle(MovingObj):
    def __init__(self, x, y, vx=0, vy=0):
        super().__init__(x, y, vx, vy)



class Sink(MovingObj):
    def __init__(self, x, y, mass, vx=0.0001, vy=0.0001):
        super().__init__(x, y, vx, vy)
        self.mass = mass


pygame.init()
clock = pygame.time.Clock()
size = width, height = 640, 480
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)

screen = pygame.display.set_mode(size)

emitters = []
particle_pool = []
sinks = []

emitters.append(Emitter(100, 100, 10, vx=0.1, vy=0.1))

sinks.append(Sink(100, 300, 20, 0.1, -0.1))
sinks.append(Sink(300, 100, 20, -0.2, 0.2))
sinks.append(Sink(300, 300, 10, -0.15, -0.15))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(WHITE)

    for emitter in emitters:
        new_particles = emitter.emit()
        particle_pool += new_particles
        pygame.draw.circle(screen, BLACK, (int(emitter.x), int(emitter.y)), emitter.amount, 1)
        pygame.draw.line(screen, BLACK, (emitter.x, emitter.y), (emitter.x + (emitter.dx * 5), emitter.y + (emitter.dy * 5)), 2)
        emitter.add_velocity()
        emitter.out_of_borders(width, height, sinks)

    for sink in sinks:
        for particle in particle_pool:
            particle.magnitude(sink.x, sink.y)
            force = 10.0 * (sink.mass / particle.distance ** 2.0)
            particle.find_direction(sink.x, sink.y)
            particle.vx += particle.dx * force
            particle.vy += particle.dy * force

    for particle in particle_pool:
        if particle.out_of_borders(width, height, sinks):
            particle_pool.remove(particle)
            continue
        pygame.draw.line(screen, BLACK, (particle.x, particle.y), (particle.x + (particle.vx * 5), particle.y + (particle.vy * 5)), 2)
        particle.add_velocity()

    for sink in sinks:
        pygame.draw.circle(screen, RED, (int(sink.x), int(sink.y)), sink.mass, 1)
        sink.add_velocity()
        sink.out_of_borders(width, height)


    pygame.display.update()