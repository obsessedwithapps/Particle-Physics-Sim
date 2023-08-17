import pygame, pymunk
from random import randint
import math
import numpy as np

class Particle():
    
    def __init__(self, x, y):
        self.r = randint(1,3)
        self.mass = self.r**2
        angle = randint(0,359)
        self.body = pymunk.Body(self.mass)
        self.color = (randint(1,255), randint(1, 255), randint(1,255))
        self.body.position = (x,y)
        self.body.velocity = ((750/self.mass)*math.cos(angle*np.pi/180), (750/self.mass)*math.sin(angle*np.pi/180))
        self.shape = pymunk.Circle(self.body, self.r)
        self.shape.collision_type = 1
        self.kinetic_energy = self.calc_KE()
        self.shape.elasticity = 1
        self.shape.density = 1
        s.add(self.body, self.shape)
    
    #Draws the particle to the screen
    def draw(self):
        x = int(self.body.position.x)
        y = int(self.body.position.y)
        
        pygame.draw.circle(screen, self.color, (x,y), self.r)
    
    #Calculates Kinetic Energy 
    def calc_KE(self):
        return 0.5*self.mass*abs(self.body.velocity)*2
        
        

#Takes in 3 arguments: a pymunk arbiter, space, and data
def collision(arbiter, space, data):
    
    return True

#Makes borders
def borderfunc(c1, c2):
    b_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    b_seg = pymunk.Segment(b_body,c1,c2, 10)
    b_seg.elasticity = 1
    s.add(b_body, b_seg)

#Sets up the host environment
pygame.init()
screen = pygame.display.set_mode((1500,1500))
pygame.display.set_caption("Particle Collision Simulation")
time = pygame.time.Clock()
s = pymunk.Space()

#Constants
FPS = 60
BLACK = (0,0,0)

dt = 1/FPS

#Particles
particles=[Particle(randint(0, 1500), randint(0, 1500)) for i in range(550)]

#Border
tl=(0,0)
tr=(1500, 0)
bl=(0, 1500)
br=(1500, 1500)
s1 = borderfunc(tl, tr)
s2 = borderfunc(tr, br)
s3 = borderfunc(br, bl)
s4 = borderfunc(bl, tl)

#Collision handler
c_handler = s.add_collision_handler(1,1)
c_handler.begin = collision

#Run pygame
step = 0
running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0,0,0))
    [particle.draw() for particle in particles]
    
    
    average_KE = 0
    total_KE = 0
    step += 1
    for particle in particles:
        total_KE += particle.kinetic_energy
        average_KE = total_KE / len(particles)
        
            
    pygame.draw.line(screen, BLACK, tl, tr, 1)
    pygame.draw.line(screen, BLACK, tr, br, 1)
    pygame.draw.line(screen, BLACK, br, bl, 1)
    pygame.draw.line(screen, BLACK, bl, tl, 1)
    
    font = pygame.font.SysFont(None, 24)
    text1 = font.render(f"Average KE: {average_KE} J", True, (255, 255, 255))
    screen.blit(text1, (10, 10))
    text2 = font.render(f"Step: {step}", True, (255, 255, 255))
    screen.blit(text2, (30, 30))
    
    pygame.display.flip()
    time.tick(FPS)
    s.step(dt)
        
pygame.quit()