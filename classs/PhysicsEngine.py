import pygame
import math
import random
from classs.Entity import Entity
from classs.Ball import Ball
from classs.Wall import Wall
from classs.Circle import Circle
from classs.CircleOuvert import CircleOuvert
from classs.Particle import Particle

class PhysicsEngine:
    def __init__(self, nbCirclesAffiches=1):
        self.num = 0
        self.nbCirclesAffiches = nbCirclesAffiches
        
    def update(self, dt):
        for e in Entity.allEntities:
            if e.enabled:
                e.update(dt)
        resCollisions = self.handle_collisions()
        return resCollisions

    def handle_collisions(self):
        rebond = 0
        ballRebond = set()
        circleRebond = set()
        circleSortis = set()
        ballSortis = set()
        # Ball-ball collisions
        for i, ball in enumerate(Ball.allBalls):
            for j in range(i + 1, len(Ball.allBalls)):
                ball2 = Ball.allBalls[j]
                res = ball.bounce(ball2)
                if res["rebond"]:
                    ballRebond.add(ball)
                    ballRebond.add(ball2)
                    rebond += 1
                    if res["particleBall"]["exists"]:
                        self.createParticle(res["particleBall"]["position"], ball)
                    if res["particleBall2"]["exists"]:
                        self.createParticle(res["particleBall2"]["position"], ball2)
    
        # Ball-wall and ball-circle collisions (déjà présent)
        for ball in Ball.allBalls:
            for circle in self.getCircles()[:20]:
                res = circle.bounce(ball)
                if res["estSorti"]:
                    ballSortis.add(ball)
                    circleSortis.add(circle)
                    ball.cerclesSorties.add(circle)
                    if isinstance(circle, CircleOuvert):
                        circle.ballsSorties.add(ball)
                elif res["existRebond"]:
                    ballRebond.add(ball)
                    circleRebond.add(circle)
                    rebond += 1
                    if res["particle"]["exists"]:
                        self.createParticle(res["particle"]["position"], ball)
                        
        return {
            "rebond": rebond, # nombre de rebonds
            "ballRebond": ballRebond, # ball rebondies
            "circleRebond": circleRebond, # circle rebondies
            "circleSortis": circleSortis, # circles sortis
            "ballSortis": ballSortis, # balls qui sortent
            "allBalls": Ball.allBalls,
            "allCircles": self.getCircles(),
        }
        
    def createParticle(self, pos, ball: Ball):
        ball.creerParticles(pos)
            
    def getBalls(self)-> list[Ball]:
        return Ball.allBalls
    
    def getCircles(self)-> list[Circle]:
        return Circle.getNCercles(self.nbCirclesAffiches)
    
    def draw(self, surface):
        for e in Entity.allEntities:
            if(isinstance(e, Circle) or not e.enabled):
                continue
            else: e.draw(surface)
        for circle in self.getCircles():
            circle.draw(surface)
            
    def getAllCircles(self):
        return Circle.allCircles