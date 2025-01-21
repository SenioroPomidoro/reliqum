import pygame
import pygame_gui

from scripts.game.game_level import Level


class Game:
    def __init__(self, w, h):
        pygame.init()
        self.w, self.h = self.size = w, h

    def start_game(self):
        pygame.display.set_caption("Reliqum")
        window_surface = pygame.display.set_mode(self.size)

        self.level = Level(window_surface)

        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            window_surface.fill((0, 0, 0))
            self.level.run()
            pygame.display.update()
            clock.tick(60)


if __name__ == "__main__":
    game = Game(1400, 900)
    game.start_game()
