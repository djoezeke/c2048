"""Game Options"""

import os
import pygame


def get_resource(filename):
    "Get Assets"
    asset = os.path.join("c2048", "assets", filename)
    return asset


def get_sound(filename: str):
    "Get Sound"
    sound = os.path.join(get_resource("sounds"), filename)
    return sound


VERSION: str = "1.0.0"
DEBUG: bool = True

HEIGHT: int = 500  # Game Window height
WIDTH: int = 400  # Game Window Width
SCREEN: dict = (WIDTH, HEIGHT)  # Game Screen

FPS: int = 60

WINDOW: pygame.Surface = pygame.display.set_mode(SCREEN)

# clock info
clock: pygame.Clock = pygame.time.Clock()

# Fonts
pygame.font.init()  # initialize pygame font

font: pygame.Font = pygame.font.Font(None, 40)

# Sounds
pygame.mixer.init()  # initialize pygame mixer
volume: float = 0.3  # music volume

music: pygame.Sound = pygame.mixer.Sound(get_sound("music.wav"))
