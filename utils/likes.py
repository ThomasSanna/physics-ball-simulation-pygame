import pygame
import string
import random

# Couleurs
RED = (244, 79, 82)
WHITE = (255, 255, 255)

likes = 0 


SUFFIXES = ['', 'K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp']

# Charger l'image du cœur
try:
    heart_img = pygame.image.load("assets/icons/heart.png")
    heart_img = pygame.transform.scale(heart_img, (30, 30))  # Redimensionner si nécessaire
except:
    print("Erreur: Impossible de charger l'image heart.png")
    pygame.quit()

def draw_notification(surface, likes_count, width, height, y, scale=1.0):
  # Taille et position du rectangle avec coins arrondis
  rect_width, rect_height = int(100 * scale), int(60 * scale)
  rect_x = (width - rect_width) // 2
  rect_y = y
  radius = int(15 * scale)

  # Dessiner le rectangle rouge arrondi
  pygame.draw.rect(surface, RED, (rect_x, rect_y, rect_width, rect_height), border_radius=radius)

  # Dessiner l'image du cœur (redimensionnée selon le scale)
  heart_size = int(30 * scale)
  heart_scaled = pygame.transform.smoothscale(heart_img, (heart_size, heart_size))
  heart_pos = (rect_x + int(15 * scale), rect_y + int(15 * scale))
  surface.blit(heart_scaled, heart_pos)

  # Dessiner le texte du nombre
  long = len(str(likes_count))
  if long < 5:
    font_size = int(25 * scale)
  elif long < 6:
    font_size = int(20 * scale)
  elif long < 8:
    font_size = int(17 * scale)
  else:
    font_size = int(12 * scale)
  font = pygame.font.SysFont('Arial', max(font_size, 1), bold=True)
  text = font.render(str(likes_count), True, WHITE)
  text_rect = text.get_rect()
  text_rect.left = heart_pos[0] + int(50 * scale) - (text.get_width() // 3)
  text_rect.centery = heart_pos[1] + heart_size // 2
  surface.blit(text, text_rect)
  
def formatNombres(nombre):
  if nombre < 1000:
    return str(int(nombre))
  index = 0
  while nombre >= 1000 and index < len(SUFFIXES) - 1:
    nombre /= 1000.0
    index += 1
  # Affiche un chiffre après la virgule si nécessaire
  if nombre % 1 == 0:
    return f"{int(nombre)}{SUFFIXES[index]}"
  else:
    return f"{nombre:.1f}{SUFFIXES[index]}"
