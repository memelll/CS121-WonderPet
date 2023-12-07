import pygame

SETTINGS_TEXT_COLOR = (255, 255, 255)
SETTINGS_BACKGROUND_COLOR = (200, 200, 200)

class SettingsMenu:
    def __init__(self, screen, width):
        self.screen = screen
        self.width = width
        self.settings_content = [
            "Bath: Z",
            "Play: X",
            "Rest: C",
            "Up: W",
            "Left: A",
            "Down: S",
            "Right: D",
            "Volume Up: Arrow Up",
            "Volume Down: Arrow Down"
        ]

    def draw_settings(self, button):
        settings_font = pygame.font.Font(None, 28)
        settings_y = button.button_y + button.button_radius * 2 + 20
        settings_background_rect_height = len(self.settings_content) * 20 + 20
        settings_background_rect_width = min(self.width - 40, max([settings_font.size(line)[0] for line in self.settings_content]) + 20)
        settings_background_rect = pygame.Rect(
            (self.width - settings_background_rect_width) // 2,
            settings_y - 10,
            settings_background_rect_width,
            settings_background_rect_height
        )
        pygame.draw.rect(self.screen, SETTINGS_BACKGROUND_COLOR, settings_background_rect)
        for line in self.settings_content:
            settings_text = settings_font.render(line, True, SETTINGS_TEXT_COLOR)
            self.screen.blit(settings_text, ((self.width - settings_text.get_width()) // 2, settings_y))
            settings_y += settings_text.get_height()