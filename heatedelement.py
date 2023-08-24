import pygame
import pymunk
from random import randint
from random import choice
from random import uniform
import math
import sys

class Particle():
    
    def __init__(self, x, y):
        self.r = 5
        self.mass = 10**-24
        self.body = pymunk.Body(self.mass)
        self.body.position = (x,y)
        self.body.velocity = (randint(-20,20),randint(-20,20))
        self.temperature = (2/3)*(6.022*10**23/8.314)*self.calculate_KE()
        self.shape = pymunk.Circle(self.body, self.r)
        self.shape.collision_type = 1
        self.shape.elasticity = 1
        self.shape.density = 1
        s.add(self.body, self.shape)
    
    
    def draw(self):
        x = int(self.body.position.x)
        y = int(self.body.position.y)     

        pygame.draw.circle(screen, (255,0,0), (x,y), self.r)

    #Calculates the kinetic energy of the particle
    def calculate_KE(self):
        
        return 0.5*self.mass*(self.body.velocity[0]**2 + self.body.velocity[1]**2)


pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Heat Simulation")
time = pygame.time.Clock()
s = pymunk.Space()
dt = 1/60

#Sets the borders
def borderfunc(c1, c2):
    b_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    b_seg = pymunk.Segment(b_body,c1,c2, 15)
    b_seg.elasticity = 1
    s.add(b_body, b_seg)


    
tl=(0,0)
tr=(1000, 0)
bl=(0, 1000)
br=(1000, 1000)
s1 = borderfunc(tl, tr)
s2 = borderfunc(tr, br)
s3 = borderfunc(br, bl)
s4 = borderfunc(bl, tl)


# Create particles
particles = [Particle(randint(0,1000), randint(0,1000)) for i in range(500)]

#Collision function paired with the collision handler
def collision(arbiter, space, data):

    return True

c_handler = s.add_collision_handler(1,1)
c_handler.begin = collision

average_temperature = 0
SIMULATION_STEPS = 1000

for step in range(SIMULATION_STEPS):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #This section of code is supposed to calculate the average temperatures and kinetic energies of the system and the particles
    total_temperature = 0
    total_KE = 0
    for particle in particles:
        total_temperature += particle.temperature
        total_KE += particle.calculate_KE()
        for other_particle in particles:
            if particle != other_particle:
                if collision:
                    avg_temperature = (particle.temperature + other_particle.temperature) / 2
                    particle.temperature = avg_temperature
                    other_particle.temperature = avg_temperature
                    average_temperature = total_temperature / len(particles)
                    average_KE = total_KE / len(particles)    
                            

    heating_rate = 0.01
    
    #This section of code adjusts the temperature of the particles due to the heating rate to add the heating effect
    for particle in particles:
        particle.body.velocity = (
            (1 + heating_rate) * particle.body.velocity[0],
            (1 + heating_rate) * particle.body.velocity[1]
        )
        
        particle.temperature = (2/3)*(6.022*10**23/8.314)*particle.calculate_KE()


    screen.fill((0, 0, 0))

    for particle in particles:
        particle.draw()
    
    font = pygame.font.SysFont(None, 24)
    text1 = font.render(f"Average Temperature: {average_temperature:07f} K", True, (255, 255, 255))
    screen.blit(text1, (10, 10))    
    text2 = font.render(f"Particle Count: {len(particles)}", True, (255, 255, 255))
    screen.blit(text2, (30, 30))
    text3 = font.render(f"Average KE: {average_KE} J", True, (255, 255, 255))
    screen.blit(text3, (50, 50))
    text4 = font.render(f"Heating Rate: {heating_rate}", True, (255, 255, 255))
    screen.blit(text4, (70, 70))
    text6 = font.render(f"Step: {step}", True, (255, 255, 255))
    screen.blit(text6, (110, 110))        
    

    pygame.display.update()
    time.tick(60)
    s.step(dt)
    

pygame.quit()







