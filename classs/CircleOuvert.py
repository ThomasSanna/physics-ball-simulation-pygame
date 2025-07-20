from classs.Circle import Circle
import pygame
import math
from classs.Ball import Ball
from classs.Particle import Particle
import random


class CircleOuvert(Circle):
    
    POSITION_ANGLE_ALEATOIRE = True
    CIRCLE_OUVERT_ANGLE = 50
    IS_ROTATING = True
    
    def __init__(self, center, radius, color=(200, 200, 200), width=None, angle=None, rotating=None, decalage=0):
        super().__init__(center, radius, color, width)
        self.angle = angle if angle is not None else CircleOuvert.CIRCLE_OUVERT_ANGLE
        if CircleOuvert.POSITION_ANGLE_ALEATOIRE:
            ecart = random.uniform(0, 2 * math.pi)
            self.startAngle = math.radians(0) + ecart
            self.endAngle = math.radians(angle) + ecart
        else:
            # Positionne l'angle de départ et d'arrivée
            self.startAngle = math.radians(0) + decalage
            self.endAngle = math.radians(angle) + decalage

        self.width = width
        self.rotating = rotating if rotating is not None else CircleOuvert.IS_ROTATING

        self.ballsSorties: list[Ball] = set()
    
    def update(self, dt):
        super().update(dt)
        self.rotate(dt)
        
    def rotate(self, dt):
        """ Fait tourner la cage circulaire ouverte dans le sens antihoraire. """
        if self.rotating:
            # speedRotation = 0.001 + (1 / max(self.radius, 1))
            speedRotation = 0.03
            self.startAngle -= dt * speedRotation
            self.endAngle -= dt * speedRotation
            if self.startAngle < 0:
                self.startAngle += 2 * math.pi
            if self.endAngle < 0:
                self.endAngle += 2 * math.pi
        
    def bounce(self, ball: Ball):
        """
        Gère la collision entre une balle et la cage circulaire ouverte (pas de collision sur l'ouverture).
        """
        res = {
            "existRebond": False,
            "estSorti": False,
            "particle": {
                "exists": False,
                "position": None
            }
        }
        if ball in self.ballsSorties:
            dx = ball.pos[0] - self.center[0]
            dy = ball.pos[1] - self.center[1]
            dist = math.hypot(dx, dy)
            if dist < self.radius - self.width:
                self.ballsSorties.remove(ball)
            else:
                return res
        estOuvert = False
        angleBalleParRapportAuCentre = math.atan2(ball.pos[0] - self.center[0], ball.pos[1] - self.center[1]) - math.pi/2
        angleBalleParRapportAuCentre = angleBalleParRapportAuCentre % (2 * math.pi) 

        if self.startAngle < self.endAngle:
            if self.startAngle < angleBalleParRapportAuCentre < self.endAngle:
                estOuvert = True
        else:
            if angleBalleParRapportAuCentre > self.startAngle or angleBalleParRapportAuCentre < self.endAngle:
                estOuvert = True
        if estOuvert:
            dx = ball.pos[0] - self.center[0]
            dy = ball.pos[1] - self.center[1]
            dist = math.hypot(dx, dy)
            
            radius = self.radius - self.width - 3
            if dist + ball.radius > radius:
                pointStart, pointEnd = self.getPoints(self.startAngle), self.getPoints(self.endAngle)
                pointBalle = self.getPoints(angleBalleParRapportAuCentre)
                # Vérifie si le radius de la balle ne touche pas le point de départ ou d'arrivée
                distToStart = math.hypot(pointStart[0] - pointBalle[0], pointStart[1] - pointBalle[1])
                distToEnd = math.hypot(pointEnd[0] - pointBalle[0], pointEnd[1] - pointBalle[1])

                # Si la balle touche un des deux bords de l’ouverture, on n'autorise pas la sortie
                if distToStart <= ball.radius*0.5 or distToEnd <= ball.radius*0.5:
                    return super().bounce(ball)

                # Sinon, elle est bien sortie
                res["estSorti"] = True
                return res

        return super().bounce(ball)
        

    def draw(self, surface):
        # Dessine un arc ouvert selon l'angle d'ouverture
        if not self.enabled :
            return
        rect = pygame.Rect(
            self.center[0] - self.radius,
            self.center[1] - self.radius,
            2 * self.radius,
            2 * self.radius
        )
        if self.detruire:
            temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            c1, c2, c3 = self.colorParticles
            faded_color = (c1, c2, c3, self.alpha)
            pygame.draw.arc(temp_surface, faded_color, rect, self.endAngle, self.startAngle, self.width)
            surface.blit(temp_surface, (0, 0))

            for p in self.particles:
                alpha = int(255 * (p["life"] / 3))
                c1, c2, c3 = self.colorParticles
                color = (c1, c2, c3, alpha)
                pygame.draw.circle(surface, color, (int(p["pos"][0]), int(p["pos"][1])), 2)
        else:
            # Dessine l'arc
            pygame.draw.arc(
                surface,
                self.color,
                rect,
                self.endAngle,
                self.startAngle,
                self.width
            )
        
    def getPoints(self, angleRad):
        return (self.center[0] + self.radius * math.cos(angleRad), self.center[1] + self.radius * math.sin(angleRad))