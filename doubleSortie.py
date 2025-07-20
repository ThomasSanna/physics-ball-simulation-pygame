import pygame
import pygame.midi
import random
import math
from classs.PhysicsEngine import PhysicsEngine
from classs.Circle import Circle
from classs.Ball import Ball
from classs.Particle import Particle
from classs.Wall import Wall
from classs.MusicMidi import MusicMidi
from classs.CircleOuvert import CircleOuvert
from classs.PauseMenu import PauseMenu
from classs.Colors import Colors
pygame.init()
pygame.midi.init()

# Paramètre Ecran
BACKGROUND_COLOR = (0, 0, 0)
TEMPS_MAX = 30

# Paramètres Balls -- 
NB_BALLS = 1
Ball.BALLS_RADIUS = 5
Ball.BALLS_VELOCITY = [5, 5]
MARGE_SPAWN = 30
Ball.BALLS_RESTITUTION = 1
Ball.NB_MIN_PARTICLES = 0
Ball.NB_MAX_PARTICLES = 0
Ball.NB_TRAIL = 0
Ball.BALLS_MASS = Ball.BALLS_RADIUS * Ball.BALLS_RADIUS * math.pi * 100
Ball.BALLS_FORCE_GRAVITE = 0.2
Ball.BALLS_VITESSE_MAX = 10
Ball.BALLS_COLLISION_WITH_BALL = False

nbBalls = 0
nbBallsSorties = 0
 
# Paramètres Circles --
NB_CIRCLES = 1
NB_MAX_TABLEAU_CIRCLES = 1
NB_CIRCLES_AFFICHES = 1 
DIVISEUR_COULEUR = 1
Circle.CIRCLE_WIDTH = 3
Circle.RADIUS_CIRCLE = 200
Circle.ECART_CIRCLE = 10
Circle.LIFE_DESTRUCTION = 20
Circle.GROWTH_DIV = 10
Circle.NB_PARTICLES_DESTRUCTION = 20
CircleOuvert.POSITION_ANGLE_ALEATOIRE = True
CircleOuvert.CIRCLE_OUVERT_ANGLE = 50
CircleOuvert.IS_ROTATING = True

nbCircles = 0
nbCirclesSortis = set()

WIDTH, HEIGHT = 540*0.8, 960*0.8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Follow Piece of Chill")
clock = pygame.time.Clock()
clock.tick()



# Création du moteur physique
engine = PhysicsEngine(NB_CIRCLES_AFFICHES)

def createCircleOuvert():
    """ Crée une cage circulaire ouverte. """
    global nbCircles
    CircleOuvert(
        center=(WIDTH // 2, HEIGHT // 2), 
        radius=Circle.RADIUS_CIRCLE+(nbCircles+1)*200, 
        color=Colors.nuances_noir(nbCircles, NB_CIRCLES//DIVISEUR_COULEUR), 
        width=Circle.CIRCLE_WIDTH, angle=CircleOuvert.CIRCLE_OUVERT_ANGLE
    )
    nbCircles += 1
    
def createBall():
    """ Crée une balle. """
    pos = (
        random.randint(WIDTH // 2 - MARGE_SPAWN, WIDTH // 2 + MARGE_SPAWN),
        random.randint(HEIGHT // 2 - MARGE_SPAWN, HEIGHT // 2 + MARGE_SPAWN)
    )
    outlineColor = None
    color = Colors.random_saturated()
    vel = [Ball.BALLS_VELOCITY[0], Ball.BALLS_VELOCITY[1]]
    Ball(pos, 
         color, 
         Ball.BALLS_RADIUS, 
         outlineColor=outlineColor, 
         vel=vel, 
         restitution=Ball.BALLS_RESTITUTION, 
         velMax=Ball.BALLS_VITESSE_MAX
         )


# -- Ajout des murs --
for _ in range(NB_MAX_TABLEAU_CIRCLES):
    if nbCircles > NB_CIRCLES:
        break
    createCircleOuvert()
    nbCircles += 1
    
# -- Ajout Boules --
for _ in range(NB_BALLS):
    createBall()
    nbBalls += 1

# musicMidiCollision = MusicMidi("testSounds", 1)
musicMidiCollision = MusicMidi("testSounds", 1)


# -- Pause Menu --
pause = PauseMenu(screen)
pause.isPaused = True
while pause.isPaused:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pause.isPaused = False
    pause.draw()


# -- Boucle principale --
running = True
clock = pygame.time.Clock()
clock.tick(60)
timeSpent = 0 # temps écoulé en secondes

while running:
    dt = clock.tick(60) / 16  # Normalise le dt pour la physique
    timeSpent += (dt * 16)/1000
    timeSpend = round(timeSpent, 2)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update
    resUpdate = engine.update(dt)
    allBalls = engine.getBalls()
    allCircles = engine.getCircles()
    allAllCircles = engine.getAllCircles()
    
    circleSortis: list[Circle] = resUpdate["circleSortis"]
    ballSortis: list[Ball] = resUpdate["ballSortis"]
    if len(ballSortis) > 0:
        for ball in ballSortis:
            if ball in allBalls:
                Ball.allBalls.remove(ball)
                nbBallsSorties += 1
                for i in range(2):
                    createBall()
                    nbBalls += 1
            
        
    for ball in allBalls:
        ball.augmenterMultiplicateurVel(0.0001)
        

    if resUpdate["rebond"] > 0:
        musicMidiCollision.jouerNote()
        
    
    # Draw
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.SysFont(None, 30)
    textIn = font.render("Total: " + str(nbBalls), True, (255, 255, 255))
    text_rectIn = textIn.get_rect(center=(WIDTH // 2, 10 + (HEIGHT // 2)))
    screen.blit(textIn, text_rectIn)
    
    
    font = pygame.font.SysFont(None, 30)
    text = font.render("In: " + str(nbBalls - nbBallsSorties), True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, -10 + (HEIGHT // 2)))
    screen.blit(text, text_rect)
    
    engine.draw(screen)
    
    # Affichage du temps écoulé en bas de l'écran
    time_font = pygame.font.SysFont(None, 36)
    time_text = time_font.render(f"Time : {max(round(TEMPS_MAX-timeSpend, 1), 0)}s", True, (255, 255, 255))
    time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT - 120))

    # Création d'un fond noir semi-transparent
    bg_surf = pygame.Surface((time_rect.width + 20, time_rect.height + 10), pygame.SRCALPHA)
    bg_surf.fill((0, 0, 0, 180))  # Noir avec alpha 100
    bg_rect = bg_surf.get_rect(center=time_rect.center)
    screen.blit(bg_surf, bg_rect)

    screen.blit(time_text, time_rect)

    
    pygame.display.flip()
