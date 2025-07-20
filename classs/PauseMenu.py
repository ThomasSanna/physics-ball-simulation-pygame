import pygame

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render("Pause", True, (255, 255, 255))
        self.rect = self.text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        self.isPaused = False

    def toggle(self):
        self.isPaused = not self.isPaused

    def draw(self):
        if self.isPaused:
            self.screen.blit(self.text, self.rect)