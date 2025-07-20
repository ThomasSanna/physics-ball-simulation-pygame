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
BACKGROUND_COLOR = (20, 40, 30)
TEMPS_MAX = 40
TEMPS_FIN_TO_DEBUT = True

# Paramètres Balls -- 
NB_BALLS = 2
Ball.BALLS_RADIUS = 20
Ball.BALLS_VELOCITY = [10, 10]
MARGE_SPAWN = 50
Ball.BALLS_RESTITUTION = 1
Ball.NB_MIN_PARTICLES = 15
Ball.NB_MAX_PARTICLES = 25
Ball.NB_TRAIL = 8
Ball.BALLS_MASS = Ball.BALLS_RADIUS * Ball.BALLS_RADIUS * math.pi 
Ball.BALLS_FORCE_GRAVITE = 0.1
Ball.BALLS_VITESSE_MAX = 13
Ball.BALLS_COLLISION_WITH_BALL = True

# Paramètres Circles --
NB_CIRCLES = 200
NB_MAX_TABLEAU_CIRCLES = 200
NB_CIRCLES_AFFICHES = 80
DIVISEUR_COULEUR = 3.0
Circle.CIRCLE_WIDTH = 3
Circle.RADIUS_CIRCLE = 50
Circle.ECART_CIRCLE = 20
Circle.LIFE_DESTRUCTION = 14
Circle.GROWTH_DIV = 20
Circle.NB_PARTICLES_DESTRUCTION = 40
CircleOuvert.POSITION_ANGLE_ALEATOIRE = False
CircleOuvert.CIRCLE_OUVERT_ANGLE = 90
CIRCLE_DECALAGE = 20

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
        color=Colors.nuances_jaune(nbCircles, DIVISEUR_COULEUR), 
        width=Circle.CIRCLE_WIDTH, angle=CircleOuvert.CIRCLE_OUVERT_ANGLE,
        decalage=(CIRCLE_DECALAGE*nbCircles*math.pi)/180
    )
    nbCircles += 1
    
def createBall():
    """ Crée une balle. """
    pos = (
        random.randint(WIDTH // 2 - MARGE_SPAWN, WIDTH // 2 + MARGE_SPAWN),
        random.randint(HEIGHT // 2 - MARGE_SPAWN, HEIGHT // 2 + MARGE_SPAWN)
    )
    outlineColor = Colors.random_saturated()
    color = BACKGROUND_COLOR
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
    if nbCircles >= NB_CIRCLES:
        break
    createCircleOuvert()
    
# -- Ajout Boules --
for _ in range(NB_BALLS):
    pos = (
        random.randint(WIDTH // 2 - MARGE_SPAWN, WIDTH // 2 + MARGE_SPAWN),
        random.randint(HEIGHT // 2 - MARGE_SPAWN, HEIGHT // 2 + MARGE_SPAWN)
    )
    outlineColor = Colors.random_saturated()
    color = BACKGROUND_COLOR
    vel = [Ball.BALLS_VELOCITY[0], Ball.BALLS_VELOCITY[1]]
    Ball(pos, 
         color, 
         Ball.BALLS_RADIUS, 
         outlineColor=outlineColor, 
         vel=vel, 
         restitution=Ball.BALLS_RESTITUTION, 
         velMax=Ball.BALLS_VITESSE_MAX
         )

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
    
    while len(allAllCircles) < NB_MAX_TABLEAU_CIRCLES:
        if nbCircles >= NB_CIRCLES:
            break
        createCircleOuvert()
        
    
    circleSortis: list[Circle] = resUpdate["circleSortis"]
    for circle in circleSortis:
        if circle in nbCirclesSortis:
            continue
        nbCirclesSortis.add(circle)
        circle.start_destruction()
        
    for ball in allBalls:
        ball.augmenterMultiplicateurVel(0.0001)
        

    if resUpdate["rebond"] > 0:
        musicMidiCollision.jouerNote()
        
    
    # Draw
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.SysFont(None, 48)
    text = font.render(str(NB_CIRCLES - len(nbCirclesSortis)), True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    engine.draw(screen)
    
    # Affichage du temps écoulé en bas de l'écran
    time_font = pygame.font.SysFont(None, 36)
    if TEMPS_FIN_TO_DEBUT:
        time_text = time_font.render(f"Time : {max(round(TEMPS_MAX-timeSpend, 1), 0)}s", True, (255, 255, 255))
    else:
        time_text = time_font.render(f"Time : {round(timeSpend, 1)}s", True, (255, 255, 255))
    time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT - 120))

    # Création d'un fond noir semi-transparent
    bg_surf = pygame.Surface((time_rect.width + 20, time_rect.height + 10), pygame.SRCALPHA)
    bg_surf.fill((0, 0, 0, 180))  # Noir avec alpha 100
    bg_rect = bg_surf.get_rect(center=time_rect.center)
    screen.blit(bg_surf, bg_rect)

    screen.blit(time_text, time_rect)

    
    pygame.display.flip()
