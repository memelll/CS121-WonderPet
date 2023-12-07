import pygame

WIDTH = 800
HEIGHT = 600
BACKGROUND_CHANGE_EVENT = pygame.USEREVENT + 2
DAY_CHANGE_EVENT = pygame.USEREVENT + 3
background_index = 0
max_width, max_height = 120, 120

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
PINK = (255, 192, 203)
BLACK = (0, 0, 0)
PEACH = (255, 229, 180)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (3, 152, 158)
GOLD = (255, 215, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Wonder Pet')

background_images = [
    pygame.image.load('Images\\day.png'),
    pygame.image.load('Images\\afternoon.png'),
    pygame.image.load('Images\\night.png')
]

pygame.mixer.init()

pygame.mixer.music.load('Sounds\\background-music.mp3')
pygame.mixer.music.set_volume(0.5)

warning_sound = pygame.mixer.Sound('Sounds\\warning.mp3')
pygame.mixer.music.set_volume(0.2)

game_over_sound = pygame.mixer.Sound('Sounds\\game_over.mp3')
pygame.mixer.music.set_volume(0.6)