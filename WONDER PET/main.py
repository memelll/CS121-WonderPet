import sys
import pygame

pygame.init()

from GameFunctions import *
from GameProfile import *
from MenuWindow import MenuWindow
from TicTacToeGame import *
from SettingsButton import *
from SettingsMenu import *


def main_game(entered_player_name, background_img, min_pet_x, max_pet_x, min_pet_y, max_pet_y, event, background_index):
    global current_day, max_width, max_height, entered_pet_name

    pygame.mixer.music.play(-1)

    pet, current_day, background_index = load_pet_data(entered_player_name, entered_pet_name)

    tic_tac_toe_button = TicTacToeButton(WIDTH - 150, 100, 140, 26, DARK_BLUE, "Tic Tac Toe", "tic_tac_toe")

    settings_button = SettingsButton(WIDTH)
    settings_menu = SettingsMenu(screen, WIDTH)

    running = True
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 26)
    show_menu = False
    show_settings_menu = False

    pet_x, pet_y = WIDTH // 2 - 50, HEIGHT // 2 - 50
    pet_width, pet_height = max_width, max_height
    pet_speed = 5
    is_flipped = False
    pet_img = pygame.image.load('Images\\clover_image.png')

    game_over_font = pygame.font.Font(None, 72)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == BACKGROUND_CHANGE_EVENT:
                background_index = (background_index + 1) % len(background_images)
                save_background_index(entered_player_name, background_index)
                background_img = background_images[background_index]
            elif event.type == DAY_CHANGE_EVENT:
                current_day = update_day(current_day)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if settings_button.is_button_clicked(event.pos[0], event.pos[1]):
                    show_settings_menu = not show_settings_menu
                    if show_settings_menu:
                        settings_menu.draw_settings(settings_button)
                    
                if menu_button.rect.collidepoint(event.pos):
                    show_menu = not show_menu

                if show_menu:
                    for button in menu_window.buttons:
                        if button.rect.collidepoint(event.pos):
                            if pet.coins >= button.action:
                                item_name = button.text.split('-')[0].strip().lower()

                                if item_name == "dog food" and pet.hunger < 100:
                                    pet.coins -= button.action
                                    pet.hunger = min(100, pet.hunger + 3)
                                    pet.exp += 2
                                    display_message(f"You fed your pet.")
                                elif item_name == "treats" and pet.happiness < 100:
                                    pet.coins -= button.action
                                    pet.happiness = min(100, pet.happiness + 10)
                                    pet.exp += 3
                                    display_message(f"You gave your pet treats. It's happy!")
                                elif item_name == "meat" and pet.hunger < 100 and pet.happiness < 100:
                                    pet.coins -= button.action
                                    pet.hunger = min(100, pet.hunger + 10)
                                    pet.happiness = min(100, pet.happiness + 5)
                                    pet.exp += 5
                                    display_message(f"You treated your pet to meat. Enjoy!")
                                elif item_name == "vitamins" and pet.hunger < 100 and pet.happiness < 100:
                                    pet.coins -= button.action
                                    pet.hunger = min(100, pet.hunger + 5)
                                    pet.happiness = min(100, pet.happiness + 5)
                                    pet.exp += 3
                                    display_message(f"You gave your pet some vitamins. Stay healthy!")
                                elif item_name == "water" and pet.thirst < 100:
                                    pet.coins -= button.action
                                    pet.thirst = min(100, pet.thirst + 2)
                                    pet.exp += 2
                                    display_message(f"You hydrated your pet with water.")
                                else:
                                    display_message("Stats already at maximum!")
                            else:
                                display_message("Not enough coins!")

                if tic_tac_toe_button.rect.collidepoint(event.pos):
                    tic_tac_toe_game = TicTacToeGame(pet)
                    tic_tac_toe_game.run_game()
                    
            if current_day >= 1 and current_day <= 5:
                max_width, max_height = 120, 120
                min_pet_y, max_pet_y = 335, HEIGHT - max_height
                min_pet_x, max_pet_x = 0, WIDTH - max_width
            elif current_day >= 6 and current_day <= 10:
                max_width, max_height = 160, 160
                min_pet_y, max_pet_y = 300, HEIGHT - max_height
                min_pet_x, max_pet_x = 0, WIDTH - max_width
            else:
                max_width, max_height = 200, 200
                min_pet_y, max_pet_y = 265, HEIGHT - max_height
                min_pet_x, max_pet_x = 0, WIDTH - max_width

            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                pet.bath()
            if keys[pygame.K_x]:
                pet.play()
            if keys[pygame.K_c]:
                pet.rest()

            if keys[pygame.K_a]:
                pet_x -= pet_speed
                if is_flipped:
                    pet_img = pygame.transform.flip(pet_img, True, False)
                    is_flipped = False
            if keys[pygame.K_d]:
                pet_x += pet_speed
                if not is_flipped:
                    pet_img = pygame.transform.flip(pet_img, True, False)
                    is_flipped = True
            if keys[pygame.K_w]:
                if pet_y > min_pet_y:
                    pet_y -= pet_speed
                    pet_width = max(pet_width - 2, 50)
                    pet_height = max(pet_height - 2, 50)
            if keys[pygame.K_s]:
                pet_y += pet_speed
                pet_width = min(pet_width + 2, max_width)
                pet_height = min(pet_height + 2, max_height)

            pet_x = max(min_pet_x, min(pet_x, max_pet_x))
            pet_y = max(min_pet_y, min(pet_y, max_pet_y))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                pygame.mixer.music.set_volume(min(1.0, pygame.mixer.music.get_volume() + 0.1))
            if keys[pygame.K_DOWN]:
                pygame.mixer.music.set_volume(max(0.0, pygame.mixer.music.get_volume() - 0.1))

            pet.update_stats()
            if is_game_over(pet):
                running = False

            background_img = pygame.transform.scale(background_images[background_index], (WIDTH, HEIGHT))
            screen.blit(background_img, (0, 0))
            pet_img_scaled = pygame.transform.scale(pet_img, (pet_width, pet_height))
            screen.blit(pet_img_scaled, (pet_x, pet_y))

            day_text = font.render(f'Day {current_day}', True, WHITE)
            text_rect = day_text.get_rect()
            text_rect.topleft = (WIDTH - text_rect.width - 55, 13)
            screen.blit(day_text, text_rect)

            coins_text = font.render(f'Coins: {pet.coins}', True, BLACK)
            coins_text_rect = coins_text.get_rect()
            coins_text_rect.topleft = (WIDTH - coins_text.get_width() - 28, 75)
            screen.blit(coins_text, coins_text_rect)

            text = font.render(f'Level: {pet.level}', True, BLACK)
            screen.blit(text, (230, 10))
            exp_ratio = min(1.0, pet.exp / pet.exp_bar)
            filled_exp_width = int(200 * exp_ratio)

            pygame.draw.rect(screen, PINK, (300, 10, filled_exp_width, 20))
            pygame.draw.rect(screen, BLACK, (300, 10, 200, 20), 2)

            exp_status_text = font.render(f'EXP: {pet.exp}/{pet.exp_bar}', True, BLACK)
            exp_status_text_rect = exp_status_text.get_rect(center=(400, 20))
            screen.blit(exp_status_text, exp_status_text_rect)

            if pet.hunger < 30:
                text = font.render(f'Appetite: {pet.hunger} (Low)', True, (255, 0, 0))
                warning_sound.play()
            else:
                text = font.render(f'Appetite: {pet.hunger}', True, BLACK)
            pygame.draw.rect(screen, GREEN, (20, 10, pet.hunger * 2, 20))
            pygame.draw.rect(screen, BLACK, (20, 10, 200, 20), 2)
            text_rect = text.get_rect(center=(110, 20))
            screen.blit(text, text_rect)

            if pet.thirst < 30:
                text = font.render(f'Hydration: {pet.thirst} (Low)', True, (255, 0, 0))
                warning_sound.play()
            else:
                text = font.render(f'Hydration: {pet.thirst}', True, BLACK)
            pygame.draw.rect(screen, BLUE, (20, 40, pet.thirst * 2, 20))
            pygame.draw.rect(screen, BLACK, (20, 40, 200, 20), 2)
            text_rect = text.get_rect(center=(110, 50))
            screen.blit(text, text_rect)

            if pet.cleanliness < 30:
                text = font.render(f'Cleanliness: {pet.cleanliness} (Low)', True, (255, 0, 0))
                warning_sound.play()
            else:
                text = font.render(f'Cleanliness: {pet.cleanliness}', True, BLACK)
            pygame.draw.rect(screen, YELLOW, (20, 70, pet.cleanliness * 2, 20))
            pygame.draw.rect(screen, BLACK, (20, 70, 200, 20), 2)
            text_rect = text.get_rect(center=(110, 80))
            screen.blit(text, text_rect)

            if pet.happiness < 30:
                text = font.render(f'Mood: {pet.happiness} (Low)', True, (255, 0, 0))
                warning_sound.play()
            else:
                text = font.render(f'Mood: {pet.happiness}', True, BLACK)
            pygame.draw.rect(screen, PURPLE, (20, 100, pet.happiness * 2, 20))
            pygame.draw.rect(screen, BLACK, (20, 100, 200, 20), 2)
            text_rect = text.get_rect(center=(110, 110))
            screen.blit(text, text_rect)

            if pet.energy < 30:
                text = font.render(f'Energy: {pet.energy} (Low)', True, (255, 0, 0))
                warning_sound.play()
            else:
                text = font.render(f'Energy: {pet.energy}', True, BLACK)
            pygame.draw.rect(screen, ORANGE, (20, 130, pet.energy * 2, 20))
            pygame.draw.rect(screen, BLACK, (20, 130, 200, 20), 2)
            text_rect = text.get_rect(center=(110, 140))
            screen.blit(text, text_rect)

            pygame.draw.rect(screen, BLACK, (300, 10, 200, 20), 2)

            menu_button_width, menu_button_height = 100, 25
            menu_button = Button(WIDTH - menu_button_width - 10, 40, menu_button_width, menu_button_height, PEACH,
                                 "MENU")

            menu_window_width, menu_window_height = 300, 260
            menu_window = MenuWindow(WIDTH // 2 - menu_window_width // 2, HEIGHT // 2 - menu_window_height // 2,
                                     menu_window_width, menu_window_height, WHITE, menu_items)

            menu_button.draw()
            if show_menu:
                menu_window.draw()

            tic_tac_toe_button.draw()
            
            settings_button.draw_button(screen)
            if show_settings_menu:
                settings_menu.draw_settings(settings_button)

            save_pet_data(entered_player_name, pet, current_day, entered_pet_name, background_index)
            save_background_index(entered_player_name, background_index)
            pygame.display.flip()
            clock.tick(30)

    if is_game_over(pet):
        game_over_font = pygame.font.Font(None, 36)
        game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, game_over_text_rect)
        game_over_sound.play()
        pygame.display.flip()

    pygame.time.delay(3000)

if __name__ == "__main__":
    background_login = pygame.image.load("Images\\welcome.png")
    background_welcome = pygame.image.load("Images\\welcome.png")
    background_login = pygame.transform.scale(background_login, (WIDTH, HEIGHT))
    background_welcome = pygame.transform.scale(background_welcome, (WIDTH, HEIGHT))

    input_font = pygame.font.Font(None, 36)

    show_entered_pet_name = False
    login_complete = False

    play_button_rect = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
    quit_button_rect = pygame.Rect(WIDTH // 2 - 100, 360, 200, 50)

    current_input = "entered_player_name"

    def login_screen():
        screen.blit(background_login, (0, 0))
        draw_text("LOGIN", 36, WIDTH // 2, 168, (3, 152, 158))
        draw_text("Name", 30, WIDTH // 2 - 145, 230, (3, 152, 158))

        if current_input == "entered_player_name":
            cursor_x_player = WIDTH // 2 - input_font.size(entered_player_name)[0] // 2
            draw_text(entered_player_name + "_", 30, WIDTH // 2, 272, (3, 152, 158))
            draw_text("Pet's Name", 30, WIDTH // 2 - 115, 330, (3, 152, 158))
            if show_entered_pet_name:
                cursor_x_pet = WIDTH // 2 - input_font.size(entered_pet_name)[0] // 2
                draw_text(entered_pet_name + "_", 30, WIDTH // 2, 375, (3, 152, 158))
        else:
            draw_text(entered_player_name, 30, WIDTH // 2, 272, (3, 152, 158))
            draw_text("Pet's Name", 30, WIDTH // 2 - 115, 330, (3, 152, 158))
            if show_entered_pet_name:
                cursor_x_pet = WIDTH // 2 + input_font.size(entered_pet_name)[0] - 10
                draw_text(entered_pet_name + "_", 30, WIDTH // 2, 375, (3, 152, 158))

        pygame.display.update()

    def welcome_screen():
        screen.blit(background_welcome, (0, 0))
        draw_text(f"Welcome to Wonder Pet, {entered_player_name}!", 30, WIDTH // 2, 250, (3, 152, 158))
        pygame.draw.rect(screen, (70, 150, 70), play_button_rect)
        pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)
        draw_text("Play", 20, WIDTH // 2, 325, (255, 255, 255))
        draw_text("Quit", 20, WIDTH // 2, 385, (255, 255, 255))
        pygame.display.update()


    def draw_text(text, size, x, y, color=(255, 255, 255)):
        text_surface = input_font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)

    logging_in = True
    running = True
    names_entered = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if logging_in:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if current_input == "entered_player_name":
                            current_input = "entered_pet_name"
                            show_entered_pet_name = True
                        elif current_input == "entered_pet_name" and len(entered_player_name) > 0 and len(
                                entered_pet_name) > 0:
                            entered_player_name = entered_player_name
                            entered_pet_name = entered_pet_name
                            names_entered = True
                            logging_in = False
                            welcome_screen()

                    elif event.key == pygame.K_BACKSPACE:
                        if current_input == "entered_player_name":
                            entered_player_name = entered_player_name[:-1]
                        elif current_input == "entered_pet_name":
                            entered_pet_name = entered_pet_name[:-1]

                    elif event.key == pygame.K_TAB:
                        current_input = "entered_pet_name" if current_input == "entered_player_name" else "player_name"

                    else:
                        if len(entered_player_name) < 15 and current_input == "entered_player_name":
                            entered_player_name += event.unicode
                        elif len(entered_pet_name) < 15 and current_input == "entered_pet_name":
                            entered_pet_name += event.unicode

                login_screen()
            else:
                if names_entered:
                    welcome_screen()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if play_button_rect.collidepoint(event.pos):
                            event = pygame.event.Event(pygame.USEREVENT)
                            main_game(entered_player_name, background_images[background_index],
                                      min_pet_x, max_pet_x, min_pet_y, max_pet_y, event, background_index)
                        elif quit_button_rect.collidepoint(event.pos):
                            running = False
                else:
                    text = font.render("Please enter both the player's name and the pet's name.", True, BLACK)
                    screen.blit(text, (10, 10))

        pygame.display.update()

    pygame.display.update()

    pygame.quit()
    sys.exit()