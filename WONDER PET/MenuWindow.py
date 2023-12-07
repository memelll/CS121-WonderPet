import pygame
from Button import Button
from GameProfile import screen, GREEN


class MenuWindow:
    def __init__(self, x, y, width, height, color, items):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.items = items
        self.buttons = []

        button_height = 40

        for i, (item, price) in enumerate(self.items.items()):
            button_y = self.rect.y + 10 + i * (button_height + 10)
            text = f"{item} - {price}"
            self.buttons.append(Button(self.rect.x + 10, button_y, width - 20, button_height, GREEN, text, price))

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        for button in self.buttons:
            button.draw()