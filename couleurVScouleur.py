import pygame
import pygame.midi
import random
import math
from classs.PhysicsEngine import PhysicsEngine
from classs.CircleOuvert import CircleOuvert
from classs.Ball import Ball
from classs.MusicMidi import MusicMidi
from classs.PauseMenu import PauseMenu
from classs.Colors import Colors

pygame.init()
pygame.midi.init()

# Écran
WIDTH, HEIGHT = int(540 * 0.8), int(960 * 0.8)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rouge vs Bleu")
clock = pygame.time.Clock()

# Config
BACKGROUND_COLOR = (0, 0, 0)
Ball.BALLS_RADIUS = 5
Ball.BALLS_VELOCITY = [3, 3]
Ball.BALLS_RESTITUTION = 1
Ball.BALLS_FORCE_GRAVITE = 0.0
Ball.BALLS_VITESSE_MAX = 10
Ball.BALLS_COLLISION_WITH_BALL = True

CircleOuvert.CIRCLE_OUVERT_ANGLE = 30
CircleOuvert.IS_ROTATING = True
CircleOuvert.CIRCLE_WIDTH = 3
CircleOuvert.POSITION_ANGLE_ALEATOIRE = True
CircleOuvert.RADIUS_CIRCLE = 200

# Suivi des couleurs
nbRouges = 0
nbBleus = 0

# Initialisation
engine = PhysicsEngine(1)
musicMidiCollision = MusicMidi("testSounds", 1)

def createCircleOuvert():
    CircleOuvert(center=(WIDTH // 2, HEIGHT // 2), radius=CircleOuvert.RADIUS_CIRCLE, color=(254, 32, 32), width=CircleOuvert.CIRCLE_WIDTH, angle=CircleOuvert.CIRCLE_OUVERT_ANGLE)

def createBall(couleur: str):
    global nbRouges, nbBleus
    pos = (
        WIDTH // 2,
        HEIGHT // 2
    )
    angle = random.uniform(0, 2 * math.pi)
    vel=(
        Ball.BALLS_VELOCITY[0] * math.cos(angle),
        Ball.BALLS_VELOCITY[1] * math.sin(angle)
        )
    # Couleurs modifiées : vert et jaune
    color = (0, 255, 0) if couleur == "rouge" else (255, 255, 0)
    Ball(pos, 
         color, 
         Ball.BALLS_RADIUS, 
         vel=vel, 
         restitution=Ball.BALLS_RESTITUTION, 
         velMax=Ball.BALLS_VITESSE_MAX)
    if couleur == "rouge":
        nbRouges += 1
    else:
        nbBleus += 1

createCircleOuvert()
createBall("rouge")
createBall("bleu")

# Pause Menu
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

# Boucle principale
running = True
while running:
    dt = clock.tick(60) / 16

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    resUpdate = engine.update(dt)
    allBalls = engine.getBalls()
    ballSortis = resUpdate["ballSortis"]

    for ball in ballSortis:
        if ball in Ball.allBalls:
            Ball.allBalls.remove(ball)
            # Couleur identifiée
            color = ball.color
            couleur = "rouge" if color[0] > color[2] else "bleu"
            for _ in range(2):
                createBall(couleur)

    for ball in allBalls:
        ball.augmenterMultiplicateurVel(0.0001)

    if resUpdate["rebond"] > 0:
        musicMidiCollision.jouerNote()

    # Affichage
    screen.fill(BACKGROUND_COLOR)
    # Affichage des scores avec fond coloré pour chaque équipe
    font = pygame.font.SysFont(None, 36)

    # Vert (anciennement Rouge)
    txt_rouge = font.render(f"Green: {nbRouges}", True, (255, 255, 255))
    rect_rouge = txt_rouge.get_rect(center=(WIDTH // 2 - 100, 170))
    bg_rouge = pygame.Surface((rect_rouge.width + 20, rect_rouge.height + 10))
    bg_rouge.fill((0, 180, 0))
    bg_rouge_rect = bg_rouge.get_rect(center=rect_rouge.center)
    screen.blit(bg_rouge, bg_rouge_rect)
    screen.blit(txt_rouge, rect_rouge)

    # Jaune (anciennement Bleu)
    txt_bleu = font.render(f"Yellow: {nbBleus}", True, (0, 0, 0))
    rect_bleu = txt_bleu.get_rect(center=(WIDTH // 2 + 100, 170))
    bg_bleu = pygame.Surface((rect_bleu.width + 20, rect_bleu.height + 10))
    bg_bleu.fill((220, 220, 0))
    bg_bleu_rect = bg_bleu.get_rect(center=rect_bleu.center)
    screen.blit(bg_bleu, bg_bleu_rect)
    screen.blit(txt_bleu, rect_bleu)

    engine.draw(screen)
    pygame.display.flip()


# ... (le reste du code reste inchangé)



# ...



# ...
