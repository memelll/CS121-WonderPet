import pygame
import random
from Button import Button


class TicTacToeGame:
    def __init__(self, pet):
        self.WIDTH, self.HEIGHT = 800, 600
        self.LINE_WIDTH = 5
        self.WHITE = (255, 255, 255)
        self.LINE_COLOR = (0, 0, 0)
        self.BOARD_SIZE = 3

        self.RECTANGLE_WIDTH, self.RECTANGLE_HEIGHT = 500, 500
        self.RECTANGLE_X, self.RECTANGLE_Y = (self.WIDTH - self.RECTANGLE_WIDTH) // 2, (
                    self.HEIGHT - self.RECTANGLE_HEIGHT) // 2

        self.SQUARE_SIZE = min(self.RECTANGLE_WIDTH // self.BOARD_SIZE, self.RECTANGLE_HEIGHT // self.BOARD_SIZE)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")

        self.pet = pet

        self.dog_image = pygame.image.load("Images\\clover_image.png")
        self.dog_image = pygame.transform.scale(self.dog_image, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.board = [['' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]

        self.font = pygame.font.Font(None, 26)

    def draw_grid(self):
        pygame.draw.rect(self.screen, self.LINE_COLOR, (
        self.RECTANGLE_X - self.LINE_WIDTH, self.RECTANGLE_Y - self.LINE_WIDTH,
        self.RECTANGLE_WIDTH + 2 * self.LINE_WIDTH, self.RECTANGLE_HEIGHT + 2 * self.LINE_WIDTH), self.LINE_WIDTH)

        for i in range(1, self.BOARD_SIZE):
            pygame.draw.line(self.screen, self.LINE_COLOR, (self.RECTANGLE_X, self.RECTANGLE_Y + i * self.SQUARE_SIZE),
                             (self.RECTANGLE_X + self.RECTANGLE_WIDTH, self.RECTANGLE_Y + i * self.SQUARE_SIZE),
                             self.LINE_WIDTH)

            pygame.draw.line(self.screen, self.LINE_COLOR, (self.RECTANGLE_X + i * self.SQUARE_SIZE, self.RECTANGLE_Y),
                             (self.RECTANGLE_X + i * self.SQUARE_SIZE, self.RECTANGLE_Y + self.RECTANGLE_HEIGHT),
                             self.LINE_WIDTH)

    def draw_symbols(self):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == 'X':
                    x = self.RECTANGLE_X + col * self.SQUARE_SIZE
                    y = self.RECTANGLE_Y + row * self.SQUARE_SIZE
                    pygame.draw.line(self.screen, self.LINE_COLOR, (x, y), (x + self.SQUARE_SIZE, y + self.SQUARE_SIZE),
                                     self.LINE_WIDTH)
                    pygame.draw.line(self.screen, self.LINE_COLOR, (x + self.SQUARE_SIZE, y), (x, y + self.SQUARE_SIZE),
                                     self.LINE_WIDTH)
                elif self.board[row][col] == 'O':
                    x = self.RECTANGLE_X + col * self.SQUARE_SIZE
                    y = self.RECTANGLE_Y + row * self.SQUARE_SIZE
                    self.screen.blit(self.dog_image, (x, y))

    def display_text(self, text, color):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(midbottom=(self.WIDTH // 2, self.HEIGHT - 10))
        self.screen.blit(text_surface, text_rect)

    def check_winner(self):
        for i in range(self.BOARD_SIZE):
            if all(self.board[i][j] == 'X' for j in range(self.BOARD_SIZE)) or \
                    all(self.board[j][i] == 'X' for j in range(self.BOARD_SIZE)):
                return 'X'
            elif all(self.board[i][j] == 'O' for j in range(self.BOARD_SIZE)) or \
                    all(self.board[j][i] == 'O' for j in range(self.BOARD_SIZE)):
                return 'O'

        if all(self.board[i][i] == 'X' for i in range(self.BOARD_SIZE)) or \
                all(self.board[i][self.BOARD_SIZE - i - 1] == 'X' for i in range(self.BOARD_SIZE)):
            return 'X'
        elif all(self.board[i][i] == 'O' for i in range(self.BOARD_SIZE)) or \
                all(self.board[i][self.BOARD_SIZE - i - 1] == 'O' for i in range(self.BOARD_SIZE)):
            return 'O'

        return None

    def computer_move(self):
        empty_cells = [(i, j) for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE) if self.board[i][j] == '']
        if empty_cells:
            return random.choice(empty_cells)
        return None

    def is_game_over(self):
        winner = self.check_winner()
        if winner:
            return True

        if all(self.board[i][j] != '' for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE)):
            return True

        return False

    def run_game(self):
        player_turn = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'

                if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    clicked_col = (mouseX - self.RECTANGLE_X) // self.SQUARE_SIZE
                    clicked_row = (mouseY - self.RECTANGLE_Y) // self.SQUARE_SIZE

                    if 0 <= clicked_row < self.BOARD_SIZE and 0 <= clicked_col < self.BOARD_SIZE:
                        if self.board[clicked_row][clicked_col] == '':
                            self.board[clicked_row][clicked_col] = 'O'
                            player_turn = False

            if not player_turn:
                computer_move_result = self.computer_move()
                if computer_move_result:
                    computer_row, computer_col = computer_move_result
                    self.board[computer_row][computer_col] = 'X'
                    player_turn = True

            self.screen.fill(self.WHITE)
            self.draw_grid()
            self.draw_symbols()

            winner = self.check_winner()
            if winner:
                if winner == 'O':
                    self.pet.coins += 50
                    self.display_text(f"Player {winner} wins! Earned 50 coins.", (0, 128, 0))
                else:
                    self.display_text("Computer wins!", (255, 0, 0))
                pygame.display.flip()
                pygame.time.delay(3000)
                return 'game_over'

            if all(self.board[i][j] != '' for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE)):
                self.display_text("It's a draw!", (0, 0, 255))
                pygame.display.flip()
                pygame.time.delay(3000)
                return 'game_over_draw'

            pygame.display.flip()

class TicTacToeButton(Button):
    def __init__(self, x, y, width, height, color, text, action):
        super().__init__(x, y, width, height, color, text, action)