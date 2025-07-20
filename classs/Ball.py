import math
import pygame
from classs.Entity import Entity
from classs.Particle import Particle
import random

class Ball(Entity):
    NB_MIN_PARTICLES = 3
    NB_MAX_PARTICLES = 10
    NB_TRAIL = 3
    BALLS_FORCE_GRAVITE = 0.2
    BALLS_MASS = 1
    BALLS_RESTITUTION = 1
    BALLS_RADIUS = 20
    BALLS_VELOCITY = [5, 3]
    BALLS_VITESSE_MAX = 10
    BALLS_COLLISION_WITH_BALL = True
    
    
    allBalls: list["Ball"] = []
    
    def __init__(self, pos, color, radius=None, outlineColor=None, vel=None, restitution=None, mass=None, outlineWidth=5, velMax=None, forceGravite=None, collisionEnabled=None, text=None, sound=None, equipeId=None):
        super().__init__()
        self.logPosition = []
        self.cerclesSorties: list["Circle"] = set()
        self.pos = list(pos)
        self.color = color
        self.radius = radius if radius is not None else Ball.BALLS_RADIUS
        self.outlineColor = outlineColor
        self.outlineWidth = outlineWidth
        self.vel = list(vel) if vel is not None else Ball.BALLS_VELOCITY
        self.mass = mass if mass is not None else Ball.BALLS_MASS
        self.restitution = restitution if restitution is not None else Ball.BALLS_RESTITUTION
        self.forceGravite = forceGravite if forceGravite is not None else Ball.BALLS_FORCE_GRAVITE
        
        self.velMax = velMax if velMax is not None else Ball.BALLS_VITESSE_MAX
        
        self.multiplicateurVel = 1
        Ball.allBalls.append(self)
        
        self.collisionEnabled = collisionEnabled if collisionEnabled is not None else Ball.BALLS_COLLISION_WITH_BALL
        
        self.text = text
        self.sound = sound
        self.equipeId = equipeId
        
    def creerParticles(self, pos):
        particles = []
        for _ in range(random.randint(Ball.NB_MIN_PARTICLES, Ball.NB_MAX_PARTICLES)):
            particles.append(Particle(pos, self.getColor(), self.radius))
        return particles
        
    def stockPosition(self, pos):
        self.logPosition.append(list(pos))
        if len(self.logPosition) > self.NB_TRAIL:
            self.logPosition.pop(0)

    def update(self, dt):
        self.stockPosition(list(self.pos))
        # Gravity
        self.vel[1] += self.forceGravite * dt # 0.3 est la force de gravité
        self.pos[0] += self.vel[0] * dt * self.multiplicateurVel
        self.pos[1] += self.vel[1] * dt * self.multiplicateurVel
        if self.pos[1] > 1000:
            self.disable()
        if self.getVitesse() > self.velMax:
            self.vel[0] *= 0.98
            self.vel[1] *= 0.98
        
    def putTrail(self, screen):
        n = len(self.logPosition)
        if n < 2:
            return
        for i in range(n):
            # L'opacité commence à 1 (255) pour le plus ancien, finit à 0 pour le plus récent
            alpha = (int(255 * (i / (n - 1)))) if n > 1 else 255
            # Ici, on ne fait pas 255 - alpha, donc le plus ancien est opaque, le plus récent est transparent
            color = self.color if self.outlineColor is None else self.outlineColor
            color_with_alpha = (*color, max(min(alpha, 255), 0))
            # Inverser le calcul du radius pour que le premier soit grand et le dernier petit
            if n > 1:
                trail_radius = int(self.radius * (i / (n - 1)) + 1 * (1 - i / (n - 1)))
            else:
                trail_radius = self.radius
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, color_with_alpha, (self.radius, self.radius), max(int(trail_radius), 1))
            screen.blit(s, (self.logPosition[i][0] - self.radius, self.logPosition[i][1] - self.radius))

    def getColor(self):
        return self.color if self.outlineColor is None else self.outlineColor

    def augmenterMultiplicateurVel(self, step=0.001):
        self.multiplicateurVel += step
    def diminuerMultiplicateurVel(self, step=0.001):
        self.multiplicateurVel -= step
        if self.multiplicateurVel < 0:
            self.multiplicateurVel = 0
    def augmenterVelMax(self, step=0.1):
        self.velMax += step

    def draw(self, screen):
        self.putTrail(screen)
        if self.outlineColor is not None:
            pygame.draw.circle(screen, self.outlineColor, (int(self.pos[0]), int(self.pos[1])), int(self.radius))
            pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), int(self.radius - self.outlineWidth))
        else:
            pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), int(self.radius))
        if self.text is not None: # crée un texte au centre de la balle. Le font s'adapte selon le radius.
            font = pygame.font.SysFont(None, int(self.radius-5))
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.pos[0], self.pos[1]))
            screen.blit(text_surface, text_rect)
          
            
    def bounce(self, ball2: "Ball"):
        res = {
            "rebond": False,
            "particleBall": {
                "exists": False,
                "position": None
            },
            "particleBall2": {
                "exists": False,
                "position": None
            }
        }
        if not self.collisionEnabled or not ball2.collisionEnabled:
            return res
        dx = ball2.pos[0] - self.pos[0]
        dy = ball2.pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        min_dist = self.radius + ball2.radius
        m1, m2 = self.mass, ball2.mass
        if dist < min_dist and dist != 0:
            res["rebond"] = True
            # Normal vector
            nx, ny = dx / dist, dy / dist
            # Point d'impact sur la surface de la première balle
            speed = math.hypot(self.vel[0], self.vel[1])
            if speed > 2:
                impact_x = self.pos[0] + nx * self.radius
                impact_y = self.pos[1] + ny * self.radius
                res["particleBall"]["exists"] = True
                res["particleBall"]["position"] = (impact_x, impact_y)
                # Point d'impact sur la surface de la deuxième balle
                impact_x2 = ball2.pos[0] - nx * ball2.radius
                impact_y2 = ball2.pos[1] - ny * ball2.radius
                res["particleBall2"]["exists"] = True
                res["particleBall2"]["position"] = (impact_x2, impact_y2)
            # Relative velocity
            dvx = ball2.vel[0] - self.vel[0]
            dvy = ball2.vel[1] - self.vel[1]
            v_rel = dvx * nx + dvy * ny
            if v_rel < 0:
                # Compute impulse scalar
                e = min(self.restitution, ball2.restitution)
                m1, m2 = self.mass, ball2.mass
                j = -(1 + e) * v_rel
                j /= (1 / m1 + 1 / m2)
                # Apply impulse
                self.vel[0] -= (j / m1) * nx
                self.vel[1] -= (j / m1) * ny
                ball2.vel[0] += (j / m2) * nx
                ball2.vel[1] += (j / m2) * ny
            # Separate balls to avoid overlap
            overlap = min_dist - dist
            self.pos[0] -= nx * (overlap * m2 / (m1 + m2))
            self.pos[1] -= ny * (overlap * m2 / (m1 + m2))
            ball2.pos[0] += nx * (overlap * m1 / (m1 + m2))
            ball2.pos[1] += ny * (overlap * m1 / (m1 + m2))
        return res
    
    def getVitesse(self):
        return math.hypot(self.vel[0], self.vel[1])