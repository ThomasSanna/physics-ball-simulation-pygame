import pygame
import math
import pygame.midi
import random
import time
import mido
import os
import colorsys
import sys

# Récupérer tous les fichiers dans le dossier "songs"
def getSoundFiles():
    sounds_dir = os.path.join(os.path.dirname(__file__), 'testSounds')
    sound_files = [os.path.join(sounds_dir, f) for f in os.listdir(sounds_dir) if os.path.isfile(os.path.join(sounds_dir, f))]
    return sound_files

# Charger un fichier MIDI aléatoire
def chargerFichierMIDI():
    sound_files = getSoundFiles()
    random.shuffle(sound_files)  # Mélange la liste des fichiers pour une sélection aléatoire
    random_sound_file = random.choice(sound_files)
    print(f"Fichier choisi : {random_sound_file}")
    midi_file = mido.MidiFile(random_sound_file)  # Remplacez par le chemin de votre fichier MIDI
    notes = []
    
    # Extraire les notes MIDI
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append(msg.note)
    return notes

def createColor():
    h = random.random()
    s = 1.0
    v = 1.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return [int(r * 255), int(g * 255), int(b * 255)]

# Initialisation
pygame.init()
pygame.midi.init()
midiOut = pygame.midi.Output(0)  # Sortie MIDI

WIDTH, HEIGHT = 540*0.8, 960*0.8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Fonction pour jouer une note MIDI
numNote = 0
lastNoteTime = 0
NOTE_DELAY = 0.1  # Délai entre les notes en secondes
def jouerNote(notes):
    global lastNoteTime, numNote
    current_time = time.time()
    if current_time - lastNoteTime >= NOTE_DELAY:
        midiOut.note_on(notes[numNote%len(notes)], 127)
        numNote = (numNote + 1) % len(notes)
        lastNoteTime = current_time

notes = chargerFichierMIDI()

# Paramètres des cages et boules
CAGE_CENTER = (WIDTH // 2, HEIGHT // 2)
CAGE_RADIUS_INIT = 150
BALL_RADIUS_INIT = 20
BALL_GROWTH = 2
BALL_SPEED = 3
GRAVITY = 0.3
CAGE_MARGIN = 10  # Marge entre la boule max et la cage

# Structure pour chaque boule/cage
class Boule:
    def __init__(self, cage_radius, color=None):
        min_angle = 0.2
        angle = random.uniform(min_angle, 2 * math.pi - min_angle)
        self.radius = min(BALL_RADIUS_INIT, cage_radius - CAGE_MARGIN-10)
        self.cage_radius = cage_radius
        self.pos = [CAGE_CENTER[0], CAGE_CENTER[1] - cage_radius]
        self.vel = [BALL_SPEED * math.cos(angle), BALL_SPEED * math.sin(angle)]
        self.lastGrowthTime = 0
        self.active = True
        if color is None:
            self.color = createColor()
        else:
            self.color = color

class Particle:
    def __init__(self, pos, color):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vel = [math.cos(angle) * speed, math.sin(angle) * speed]
        self.pos = [pos[0], pos[1]]
        self.radius = random.randint(2, 5)
        self.life = random.randint(15, 30)
        self.color = color

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[1] += 0.2  # gravité
        self.radius *= 0.95
        self.life -= 1

    def draw(self, surface):
        if self.life > 0 and self.radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), int(self.radius))

# WAITING SCREEN ---------------------------------
paused = True
font = pygame.font.SysFont(None, 72)
pause_text = font.render("Pause", True, (255, 255, 255))
pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

while paused:
    screen.fill((0, 0, 0))
    screen.blit(pause_text, pause_rect)
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = False

particles = []
boules = [Boule(CAGE_RADIUS_INIT)]
cages = [(CAGE_RADIUS_INIT, createColor())]

running = True
animationFin = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    screen.fill((0, 0, 0))

    # Dessiner les cages
    for cage_radius, cage_color in cages:
        if not animationFin:
            pygame.draw.circle(screen, cage_color, CAGE_CENTER, cage_radius, 10)
        else:
            jouerNote(notes)
            # Animation de fin : faire pulser toutes les cages
            angle = math.sin(pygame.time.get_ticks() / 200)
            
            pulse = CAGE_RADIUS_INIT * angle
            for cage_radius, cage_color in cages:
                pygame.draw.circle(
                    screen,
                    cage_color,
                    CAGE_CENTER,
                    int(cage_radius + pulse),
                    10
                )
            if angle < -1:
                animationFin = False
                boules = [Boule(CAGE_RADIUS_INIT)]
                cages = [(CAGE_RADIUS_INIT, createColor())]
                continue
            

    # Mettre à jour et dessiner les boules
    for i, boule in enumerate(boules):
        if not boule.active:
            continue
        if  (boule.active and boule.radius < 0):
            animationFin = True
            continue
                
        
        
        boule.vel[1] += GRAVITY
        boule.pos[0] += boule.vel[0]
        boule.pos[1] += boule.vel[1]

        # Collision avec la cage
        dx = boule.pos[0] - CAGE_CENTER[0]
        dy = boule.pos[1] - CAGE_CENTER[1]
        dist = math.hypot(dx, dy)
        if dist + boule.radius > boule.cage_radius-10:
            nx, ny = dx / dist, dy / dist
            v_dot_n = boule.vel[0] * nx + boule.vel[1] * ny
            boule.vel[0] -= 2 * v_dot_n * nx
            boule.vel[1] -= 2 * v_dot_n * ny
            overlap = (dist + boule.radius) - (boule.cage_radius-10)
            boule.pos[0] -= nx * overlap
            boule.pos[1] -= ny * overlap
            # Grossir la boule
            if time.time() - boule.lastGrowthTime > NOTE_DELAY:
                boule.radius += BALL_GROWTH
                boule.lastGrowthTime = time.time()
                jouerNote(notes)
            # --- Ajout de particules à l'impact ---
            for _ in range(12):
                particles.append(Particle(boule.pos, boule.color))

        # Explosion : nouvelle boule/cage
        if boule.radius > boule.cage_radius - CAGE_MARGIN and boule.active:
            boule.active = False
            new_cage_radius = boule.cage_radius - 10
            cages.append((new_cage_radius, boule.color))  # Utilise la couleur de la boule
            boules.append(Boule(new_cage_radius))

        # Dessiner la boule
        pygame.draw.circle(screen, boule.color, (int(boule.pos[0]), int(boule.pos[1])), int(boule.radius), 10)

    # Mettre à jour et dessiner les particules
    for p in particles[:]:
        p.update()
        p.draw(screen)
        if p.life <= 0 or p.radius < 1:
            particles.remove(p)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()