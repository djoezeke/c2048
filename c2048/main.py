"""MAin Game"""

import sys
import pygame

from c2048.game import config

from c2048.game.colors import Colors
from c2048.game.board import Board


class Game:
    """Game"""

    def __init__(self):
        self.board = Board()
        self.game_over = False
        self.score = 0
        self.high_score = 0
        self.spawn_new = True
        self.count = 0
        self.direct = ""

    def update_score(self):
        """update_score"""
        if self.high_score < self.score:
            self.high_score += self.score

    def draw_over(self, screen):
        """draw_over"""

        pygame.draw.rect(screen, "black", [40, 100, 350, 100], 0, 10)
        over_text1 = config.font.render("GAME OVER!", True, Colors.white)
        over_text2 = config.font.render("Press Escape to Restart", True, Colors.white)

        screen.blit(over_text1, (120, 100))
        screen.blit(over_text2, (50, 140))

    def reset(self):
        """reset"""

        self.board.reset()
        self.score = 0
        self.count = 0
        self.direct = ""
        self.spawn_new = True
        self.game_over = False

    def draw(self, screen: pygame.Surface):
        """draw"""

        self.board.draw_board(screen)
        self.board.draw_pieces(screen)
        score_text = config.font.render(f"Score: {self.score}", True, Colors.white)
        high_score_text = config.font.render(
            f"High Score: {self.high_score}", True, Colors.white
        )

        screen.blit(score_text, (10, 410))
        screen.blit(high_score_text, (10, 450))

    def direction(self):
        """direction"""

        if self.spawn_new is True or self.count < 2:
            self.game_over = self.board.new_pieces()
            self.spawn_new = False
            self.count += 1

        if self.direct != "":
            self.take_turn(self.direct)
            self.spawn_new = True
            self.direct = ""

    def turn_up(self, merged):
        """turn_up"""
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if self.board.values[q][j] == 0:
                            shift += 1
                if shift > 0:
                    self.board.values[i - shift][j] = self.board.values[i][j]
                    self.board.values[i][j] = 0
                if (
                    self.board.values[i - shift - 1][j]
                    == self.board.values[i - shift][j]
                    and not merged[i - shift - 1][j]
                    and not merged[i - shift][j]
                ):
                    self.board.values[i - shift - 1][j] *= 2
                    self.score += self.board.values[i - shift - 1][j]
                    self.board.values[i - shift][j] = 0
                    merged[i - shift][j] = True

    def turn_down(self, merged):
        """turn_up"""
        # TODO : Fix

        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if self.board.values[3 - q][j] == 0:
                        shift += 1

                if shift > 0:
                    self.board.values[2 - i + shift][j] = self.board.values[2 - i][j]
                    self.board.values[2 - i][j] = 0

                if 3 - i + shift <= 3:
                    if (
                        self.board.values[2 - i + shift][j]
                        == self.board.values[3 - i + shift][j]
                        and not merged[2 - i + shift][j]
                        and not merged[3 - i + shift][j]
                    ):
                        self.board.values[3 - i + shift][j] *= 2
                        self.score += self.board.values[3 - i + shift][j]
                        self.board.values[2 - i + shift] = 0
                        merged[3 - i + shift] = True

    def turn_right(self, merged):
        """turn_up"""
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if self.board.values[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    self.board.values[i][3 - j - shift] = self.board.values[i][3 - j]
                    self.board.values[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if (
                        self.board.values[i][4 - j + shift]
                        == self.board.values[i][3 - j - shift]
                        and not merged[i][3 - j - shift]
                        and not merged[i][4 - j - shift]
                    ):
                        self.board.values[i][4 - j - shift] *= 2
                        self.score += self.board.values[i][4 - j - shift]
                        self.board.values[i][3 - j - shift] = 0
                        merged[i][4 - j - shift] = True

    def turn_left(self, merged):
        """turn_left"""
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if self.board.values[i][q] == 0:
                        shift += 1
                if shift > 0:
                    self.board.values[i][j - shift] = self.board.values[i][j]
                    self.board.values[i][j] = 0

                if (
                    self.board.values[i][j - shift]
                    == self.board.values[i][j - shift - 1]
                    and not merged[i][j - shift - 1]
                    and not merged[i][j - shift]
                ):
                    self.board.values[i][j - shift - 1] *= 2
                    self.score += self.board.values[i][j - shift - 1]
                    self.board.values[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    def take_turn(self, direct):
        """take_turn"""
        merged = [
            [False for _ in range(self.board.num_row)]
            for _ in range(self.board.num_col)
        ]

        if direct == "UP":
            self.turn_up(merged)

        if direct == "DOWN":
            self.turn_down(merged)

        if direct == "LEFT":
            self.turn_left(merged)

        if direct == "RIGHT":
            self.turn_right(merged)


game = Game()


def c2048(args: list):
    """c2048"""

    pygame.display.set_caption("c2048")

    config.music.set_volume(config.volume)
    config.music.play(loops=-1)

    if "--nosound" in args:
        config.music.set_volume(0)
        config.music.stop()

    run: bool = True

    config.clock = pygame.time.Clock()

    # main game loop
    while run:
        config.clock.tick(config.FPS)
        config.WINDOW.fill("gray")
        game.draw(config.WINDOW)

        if game.game_over is True:
            game.update_score()
            game.draw_over(config.WINDOW)

        pygame.display.update()
        game.direction()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:

                if game.game_over is True:
                    if event.key == pygame.K_ESCAPE:
                        game.reset()

                if event.key == pygame.K_LEFT and game.game_over is False:
                    game.direct = "LEFT"
                if event.key == pygame.K_RIGHT and game.game_over is False:
                    game.direct = "RIGHT"
                if event.key == pygame.K_DOWN and game.game_over is False:
                    game.direct = "DOWN"
                if event.key == pygame.K_UP and game.game_over is False:
                    game.direct = "UP"

    pygame.quit()
    sys.exit()


def main(args):
    """Main"""
    try:
        c2048(args)
    except KeyboardInterrupt:
        print("Keyboard Interrupt...")
        print("Exiting")


if __name__ == "__main__":
    main(sys.argv)
