import sys
import pygame
import core
from state import State

class Board:
    def __init__(self, size, space=20, bgcolor=(255, 255, 255), line_color=(0, 0, 0)):
        self.size = size
        self.space = space
        self.bgcolor = bgcolor
        self.line_color = line_color
        self.screen = pygame.Surface(size)
        self.screen.fill(bgcolor)
        self.rect = self.screen.get_rect()
        self.row_cnt = self.size[1] // self.space
        self.col_cnt = self.size[0] // self.space
        for i in range(self.row_cnt):
            pygame.draw.line(self.screen, line_color, (0, i * self.space), (self.size[0], i * self.space))
        for i in range(self.col_cnt):
            pygame.draw.line(self.screen, line_color, (i * self.space, 0), (i * self.space, self.size[1]))

    def render(self, screen):
        screen.blit(self.screen, self.rect)
class GameScene(State):
    def __init__(self):
        self.board = Board(core.get_config().board_size)
        self.screen = pygame.Surface(core.get_config().screen_size)
        self.rect = self.screen.get_rect()

    def update(self, events):
        super(GameScene, self).update(events)
        self.render(core.get_app().screen)
        pygame.display.flip()

    def render(self, screen):
        self.board.render(self.screen)
        screen.blit(self.screen, self.rect)

if __name__ == '__main__':
    app = core.App(
        config={'board_size': (700, 600)}
    )
    scene = GameScene()
    sys.exit(app.run_with_state(scene))