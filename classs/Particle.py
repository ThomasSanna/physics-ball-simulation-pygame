import pygame
import math
import random
from classs.Entity import Entity

class Particle(Entity):
  
    allParticles = []
    def __init__(self, pos, color, radius):
        super().__init__()
        if len(Particle.allParticles) > 1000:
            Particle.allParticles.pop(0)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        self.vel = [math.cos(angle) * speed, math.sin(angle) * speed]
        self.pos = list(pos)
        self.radius = random.randint(radius//3, radius//1.5)
        self.life = random.randint(15, 30)
        self.color = color
        Particle.allParticles.append(self)

    def update(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.vel[1] += 0.2 * dt
        self.radius *= 0.97
        self.life -= 1
        if self.life <= 0:
            self.disable()

    def draw(self, surface):
        if self.life > 0 and self.radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), int(self.radius))
  
    @staticmethod
    def getParticlesAlive():
        return [p for p in Particle.allParticles if p.life > 0 and p.radius > 0]
