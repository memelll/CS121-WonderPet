import pygame
import pickle
import os

from GameProfile import BACKGROUND_CHANGE_EVENT, DAY_CHANGE_EVENT, HEIGHT, WIDTH, screen

pygame.font.init()
font = pygame.font.Font(None, 26)

current_day = 1

def update_day(current_day):
    return current_day + 1

pygame.time.set_timer(BACKGROUND_CHANGE_EVENT, 3 * 60 * 1000)
pygame.time.set_timer(DAY_CHANGE_EVENT, 9 * 60 * 1000)

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

pet_img = pygame.image.load('Images\\clover_image.png')
pet_img = pygame.transform.scale(pet_img, (max_width, max_height))

entered_player_name = ""
entered_pet_name = ""


def display_message(message):
    font = pygame.font.Font(None, 25)
    text = font.render(message, True, (255, 255, 255))
    background = pygame.Surface((text.get_width() + 20, text.get_height() + 20))
    background.fill((128, 128, 128))
    screen.blit(background, (WIDTH - background.get_width() - 10, HEIGHT - background.get_height() - 10))
    screen.blit(text, (WIDTH - background.get_width() - 10 + 10, HEIGHT - background.get_height() - 10 + 10))
    pygame.display.flip()
    pygame.time.delay(500)


menu_items = {"Dog Food": 2, "Water": 2, "Vitamins": 5, "Treats": 10, "Meat": 15}


def is_game_over(pet):
    return pet.hunger <= 0 or pet.cleanliness <= 0 or pet.happiness <= 0 or pet.thirst <= 0 or pet.energy <= 0


def save_pet_data(entered_player_name, pet, current_day, entered_pet_name, background_index):
    save_data = {
        'entered_player_name': entered_player_name,
        'entered_pet_name': entered_pet_name,
        'pet': pet,
        'current_day': current_day,
        'background_index': background_index
    }
    with open(f'{entered_player_name}_{entered_pet_name}_pet_data.dat', 'wb') as file:
        pickle.dump(save_data, file)


def load_pet_data(entered_player_name, entered_pet_name):
    file_name = f'{entered_player_name}_{entered_pet_name}_pet_data.dat'
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            save_data = pickle.load(file)
            return save_data['pet'], save_data['current_day'], save_data['background_index']
    else:
        from VirtualPet import VirtualPet
        return VirtualPet(), 1, 0


def save_background_index(entered_player_name, background_index):
    with open(f'{entered_player_name}_background_index.dat', 'wb') as file:
        pickle.dump(background_index, file)


def load_background_index(entered_player_name):
    file_name = f'{entered_player_name}_background_index.dat'
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            background_index = pickle.load(file)
            return background_index
    else:
        return 0


pet, current_day, background_index = load_pet_data(entered_player_name, entered_pet_name)

background_index = load_background_index(entered_player_name)
