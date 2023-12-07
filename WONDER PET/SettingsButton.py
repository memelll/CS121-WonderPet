import pygame

SETTINGS_TEXT_COLOR = (255, 255, 255)
SETTINGS_BACKGROUND_COLOR = (128, 128, 128)

class SettingsButton:
    def __init__(self, width):
        self.button_radius = 15
        self.button_x, self.button_y = width - self.button_radius - 30, 5
        self.show_settings = False
        self.load_button_image()
        self.create_rect()

    def load_button_image(self):
        button_image = pygame.image.load("Images\\settings.png")
        self.button_image = pygame.transform.scale(button_image, (self.button_radius * 2, self.button_radius * 2))

    def create_rect(self):
        self.rect = pygame.Rect(self.button_x, self.button_y, self.button_radius * 2, self.button_radius * 2)

    def draw_button(self, screen):
        screen.blit(self.button_image, (self.button_x, self.button_y))

    def is_button_clicked(self, mouse_x, mouse_y):
        return self.rect.collidepoint(mouse_x, mouse_y)