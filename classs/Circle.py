import pygame
from classs.Entity import Entity
import math
import random
from classs.Ball import Ball

class Circle(Entity):
    
    allCircles = []
    LIFE_DESTRUCTION = 20
    GROWTH_DIV = 20
    RADIUS_CIRCLE = 100
    ECART_CIRCLE = 20
    NB_PARTICLES_DESTRUCTION = 20
    CIRCLE_WIDTH = 5
    
    
    
    def __init__(self, center, radius, color=(200,200,200), width=None):
        super().__init__()
        self.center = center
        self.radius = radius
        self.targetRadius = radius
        self.growth = 0.05
        self.color = color
        self.width = width if width is not None else Circle.CIRCLE_WIDTH
        
        Circle.allCircles.append(self)
        
        self.detruire = False
        self.lifeDestruction = Circle.LIFE_DESTRUCTION
        self.alpha = 255
        self.particles = []
        self.colorParticles = self.color
                
    def update(self, dt):
        """ Met à jour la cage circulaire. """
        if self.detruire:
            self.lifeDestruction -= dt
            self.alpha = max(0, int(255 * (self.lifeDestruction / Circle.LIFE_DESTRUCTION)))
            self.spawn_particles()
            self.update_particles(dt)
            if self.lifeDestruction <= 0:
                self.disable()
        # Update the radius
        if self.radius < self.targetRadius:
            self.radius += self.growth * dt
            if self.radius > self.targetRadius:
                self.radius = self.targetRadius
        elif self.radius > self.targetRadius:
            self.radius -= self.growth * dt
            if self.radius < self.targetRadius:
                self.radius = self.targetRadius
        if self.radius < 0:
            self.radius = 0
            
                
    def spawn_particles(self, amount=None):
        amount = Circle.NB_PARTICLES_DESTRUCTION if amount is None else amount
        for _ in range(amount):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(self.radius - self.width // 2, self.radius + self.width // 2)
            x = self.center[0] + math.cos(angle) * dist
            y = self.center[1] + math.sin(angle) * dist
            vel = [random.uniform(-1, 1), random.uniform(-1, 1)]
            self.particles.append({
                "pos": [x, y],
                "vel": vel,
                "life": random.uniform(1, 3)
            })

    def update_particles(self, dt):
        for p in self.particles:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            p["life"] -= dt
            if p["life"] <= 0:
                self.particles.remove(p)

    def start_destruction(self):
        """ Déclenche la désintégration visuelle du cercle. """
        self.detruire = True

    def reduceRadius(self, step=1, limit=0)-> dict:
        """ Réduit le rayon de la cage circulaire et renvoie un dictionnaire avec le succès de l'opération et les anciens et nouveaux rayons. """
        result = {"success": True, "newRadius": self.radius, "oldRadius": self.radius}
        self.setRadius(self.radius - step)
        if self.radius < limit:
            self.radius += step
            result["success"] = False
            return result
        result["newRadius"] = self.radius
        return result
    
    def draw(self, surface):
        if not self.enabled:
            return
        if self.detruire:
            temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            c1, c2, c3 = self.colorParticles
            faded_color = (c1, c2, c3, self.alpha)
            pygame.draw.circle(temp_surface, faded_color, self.center, self.radius, self.width)
            surface.blit(temp_surface, (0, 0))

            for p in self.particles:
                alpha = int(255 * (p["life"] / 3))
                color = (*self.color[:3], alpha)
                pygame.draw.circle(surface, color, (int(p["pos"][0]), int(p["pos"][1])), 2)
        else:
            pygame.draw.circle(surface, self.color, self.center, self.radius, self.width)

    def bounce(self, ball: Ball):
        """ Gère la collision entre une balle et la cage circulaire. """
        res = {
            "existRebond": False,
            "estSorti": False,
            "particle": {
                "exists": False,
                "position": None
            }
        }
        dx = ball.pos[0] - self.center[0]
        dy = ball.pos[1] - self.center[1]
        dist = math.hypot(dx, dy)
        radius = self.radius - self.width - 3
        if dist + ball.radius > radius :
            nx, ny = dx / dist, dy / dist
            speed = math.hypot(ball.vel[0], ball.vel[1])
            if speed > 3:
                impact_x = self.center[0] + nx * radius
                impact_y = self.center[1] + ny * radius
                res['particle']["exists"] = True
                res['particle']["position"] = (impact_x, impact_y)
            v_dot_n = ball.vel[0] * nx + ball.vel[1] * ny
            ball.vel[0] -= 2 * v_dot_n * nx * ball.restitution
            ball.vel[1] -= 2 * v_dot_n * ny * ball.restitution
            overlap = (dist + ball.radius) - radius
            ball.pos[0] -= nx * overlap
            ball.pos[1] -= ny * overlap
            res["existRebond"] = True
        return res
    
    def setRadius(self, radius):
        self.targetRadius = radius
        if self.targetRadius < 0:
            self.targetRadius = 0
        self.growth = abs(self.targetRadius - self.radius) / Circle.GROWTH_DIV
        
    def disable(self):
        """ Désactive la cage circulaire. """
        self.enabled = False
        Circle.allCircles.remove(self)
            
    @staticmethod
    def getNCercles(n=10):
        """ Renvoie une liste de n cages circulaires activées. """
        circles = Circle.allCircles[:n]
        for i, circle in enumerate(circles):
            circle.setRadius(Circle.RADIUS_CIRCLE + i * Circle.ECART_CIRCLE)
        return circles
    
    @staticmethod
    def getAll():
        """ Renvoie une liste de toutes les cages circulaires activées. """
        return Circle.allCircles