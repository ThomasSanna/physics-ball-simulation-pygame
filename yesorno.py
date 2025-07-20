import pygame
import pygame.midi
import pygame.mixer
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

allSounds = ["assets/sounds/yes.mp3", "assets/sounds/no.mp3"]
channels = [pygame.mixer.Channel(i) for i in range(len(allSounds))]
allColor = [(8, 255, 119), (250, 27, 53)]
allText = ["Yes", "No"]

# Paramètre Ecran
BACKGROUND_COLOR = (0, 0, 0)
TEMPS_MAX = 40
TEMPS_FIN_TO_DEBUT = True

# Paramètres Balls -- 
NB_BALLS = 2
Ball.BALLS_RADIUS = 35
Ball.BALLS_VELOCITY = [5, 5]
MARGE_SPAWN = 10
Ball.BALLS_RESTITUTION = 1.05
Ball.NB_MIN_PARTICLES = 4
Ball.NB_MAX_PARTICLES = 8
Ball.NB_TRAIL = 12
Ball.BALLS_MASS = Ball.BALLS_RADIUS * Ball.BALLS_RADIUS * math.pi 
Ball.BALLS_FORCE_GRAVITE = 0.1
Ball.BALLS_VITESSE_MAX = 10

nbBalls = 0
 
# Paramètres Circles --
NB_CIRCLES = 1000
NB_MAX_TABLEAU_CIRCLES = 1000
NB_CIRCLES_AFFICHES = 30
DIVISEUR_COULEUR = 3
Circle.CIRCLE_WIDTH = 3
Circle.RADIUS_CIRCLE = 160
Circle.ECART_CIRCLE = 8
Circle.LIFE_DESTRUCTION = 5
Circle.GROWTH_DIV = 2
Circle.NB_PARTICLES_DESTRUCTION = 10
CircleOuvert.POSITION_ANGLE_ALEATOIRE = False
CircleOuvert.CIRCLE_OUVERT_ANGLE = 50 
CircleOuvert.IS_ROTATING = True
CIRCLE_DECALAGE = 2

nbCircles = 0
circlesSortis = set()

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
        color=Colors.random_nuance(nbCircles, DIVISEUR_COULEUR), 
        width=Circle.CIRCLE_WIDTH, angle=CircleOuvert.CIRCLE_OUVERT_ANGLE,
        decalage=(CIRCLE_DECALAGE*nbCircles*math.pi)/180,
    )
    nbCircles += 1
    
def createBall():
    """ Crée une balle. """
    global nbBalls
    pos = (
        random.randint(WIDTH // 2 - MARGE_SPAWN, WIDTH // 2 + MARGE_SPAWN),
        random.randint(HEIGHT // 2 - MARGE_SPAWN, HEIGHT // 2 + MARGE_SPAWN)
    )
    color = BACKGROUND_COLOR
    vel = [Ball.BALLS_VELOCITY[0], Ball.BALLS_VELOCITY[1]]
    Ball(
        pos, 
        color, 
        Ball.BALLS_RADIUS, 
        outlineColor=allColor[nbBalls % len(allColor)], 
        vel=vel, 
        restitution=Ball.BALLS_RESTITUTION, 
        velMax=Ball.BALLS_VITESSE_MAX,
        text=allText[nbBalls % len(allText)],
        sound=pygame.mixer.Sound(allSounds[nbBalls % len(allSounds)]),
        equipeId=nbBalls%len(allSounds),
    )
    nbBalls += 1
    

# -- Ajout des murs --
for _ in range(NB_MAX_TABLEAU_CIRCLES):
    if nbCircles >= NB_CIRCLES:
        break
    createCircleOuvert()
    
# -- Ajout Boules --
for _ in range(NB_BALLS):
    createBall()

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
    
    


# -- Boucle principale ----------------------------------------
running = True
clock = pygame.time.Clock()
clock.tick(60)
timeSpent = 0 # temps écoulé en secondes
timeSpaceSound = 0

while running:
    dt = clock.tick(90) / 16  # Normalise le dt pour la physique
    timeSpent += (dt * 16)/1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update
    resUpdate = engine.update(dt)
    nbRebond = resUpdate["rebond"]
    ballsSortis: list[Ball] = resUpdate["ballSortis"]
    circleSortis: list[Circle] = resUpdate["circleSortis"]
    
    
    allBalls = engine.getBalls()
    allCircles = engine.getCircles()
    allAllCircles = engine.getAllCircles()
    
    while len(allAllCircles) < NB_MAX_TABLEAU_CIRCLES:
        if nbCircles >= NB_CIRCLES:
            break
        createCircleOuvert()
        
    for ball in ballsSortis:
        for circle in ball.cerclesSorties:
            if circle not in circlesSortis:
                if (timeSpent - timeSpaceSound) > 0.1:
                    timeSpaceSound = timeSpent
                    ball.sound.play()
            if not circle.detruire:
                circle.colorParticles = ball.getColor()

    for circle in circleSortis:
        if circle in circlesSortis:
            continue
        circlesSortis.add(circle)
        circle.start_destruction()
        

    if resUpdate["rebond"] > 0:
        musicMidiCollision.jouerNote()
        
    
    # Draw
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.SysFont(None, 48)
    text = font.render(str(), True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    engine.draw(screen)
    
    # Affichage des scores des balls en haut de l'écran, format : ball.text: score
    score_font = pygame.font.SysFont(None, 40)
    scores = [len(ball.cerclesSorties) for ball in allBalls]
    score_surfs = []
    padding = 20
    for i, ball in enumerate(allBalls):
        score_text = f"{ball.text}: {scores[i]}"
        text_surf = score_font.render(score_text, True, (255, 255, 255))
        # Fond de la couleur de la boule (outlineColor)
        bg_surf = pygame.Surface((text_surf.get_width() + padding, text_surf.get_height() + 10), pygame.SRCALPHA)
        bg_color = ball.outlineColor if hasattr(ball, "outlineColor") else (128, 128, 128)
        bg_surf.fill(bg_color + (220,))
        score_surfs.append((bg_surf, text_surf))

    # Calcul de la largeur totale pour centrer
    total_width = sum(bg.get_width() for bg, _ in score_surfs) + (len(score_surfs) - 1) * 30
    start_x = (WIDTH - total_width) // 2
    y = 170  # Position en haut de l'écran

    x = start_x
    for bg_surf, text_surf in score_surfs:
        rect = bg_surf.get_rect(topleft=(x, y))
        screen.blit(bg_surf, rect)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
        x += bg_surf.get_width() + 30
    
    # Affichage du temps écoulé en bas de l'écran
    timeAffiche = round(timeSpent, 2)
    time_font = pygame.font.SysFont(None, 36)
    if TEMPS_FIN_TO_DEBUT:
        time_text = time_font.render(f"Time : {max(round(TEMPS_MAX-timeAffiche, 1), 0)}s", True, (255, 255, 255))
    else:
        time_text = time_font.render(f"Time : {round(timeAffiche, 1)}s", True, (255, 255, 255))
    time_rect = time_text.get_rect(center=(WIDTH // 2, 240))

    # Création d'un fond noir semi-transparent
    bg_surf = pygame.Surface((time_rect.width + 20, time_rect.height + 10), pygame.SRCALPHA)
    bg_surf.fill((0, 0, 0, 180))  # Noir avec alpha 100
    bg_rect = bg_surf.get_rect(center=time_rect.center)
    screen.blit(bg_surf, bg_rect)

    screen.blit(time_text, time_rect)

    
    pygame.display.flip()
