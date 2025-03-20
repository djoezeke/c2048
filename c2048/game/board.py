"""Board"""

import random
import pygame
from c2048.game.colors import Colors


class Board:
    """Board"""

    def __init__(self):
        self.num_row = 4
        self.num_col = 4
        self.values = self.generate_values()

    def reset(self):
        """reset"""
        self.values = self.generate_values()

    def generate_values(self):
        """generate_values"""
        values = [[0 for _ in range(self.num_row)] for _ in range(self.num_col)]
        return values

    def draw_board(self, screen):
        """draw_board"""
        pygame.draw.rect(screen, Colors.background, [0, 0, 400, 400], 0, 10)

    def new_pieces(self):
        """new_pieces"""
        full = False
        count = 0
        while any(0 in row for row in self.values) and count < 1:
            row = random.randint(0, 3)
            col = random.randint(0, 3)

            if self.values[row][col] == 0:
                count += 1
                if random.randint(1, 10) == 10:
                    self.values[row][col] = 4
                else:
                    self.values[row][col] = 2
        if count < 1:
            full = True

        return full

    def draw_pieces(self, screen):
        """draw_pieces"""
        for i in range(self.num_row):
            for j in range(self.num_col):
                value = self.values[i][j]
                if value > 8:
                    value_color = Colors.light_text
                else:
                    value_color = Colors.dark_text
                if value <= 2048:
                    color = Colors.get_color(value)
                else:
                    color = Colors.other
                pygame.draw.rect(
                    screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5
                )

                if value > 0:
                    value_len = len(str(value))
                    font: pygame.Font = pygame.font.Font(None, 48 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                    screen.blit(value_text, text_rect)
                    pygame.draw.rect(
                        screen, "black", [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5
                    )
