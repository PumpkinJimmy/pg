import state

import sys
import pygame
import core
import utils


class Board(core.Node):
    def __init__(self, size, space=20, bgcolor=(255, 255, 255), line_color=(0, 0, 0)):
        super(Board, self).__init__()
        self.size = size
        self.space = space
        self.bgcolor = bgcolor
        self.line_color = line_color
        self.image = pygame.Surface(size)
        self.image.fill(bgcolor)
        self.rect = self.image.get_rect()
        self.row_cnt = self.size[1] // self.space
        self.col_cnt = self.size[0] // self.space
        for i in range(self.row_cnt + 1):
            pygame.draw.line(self.image, line_color, (0, i * self.space), (self.size[0], i * self.space))
        for i in range(self.col_cnt + 1):
            pygame.draw.line(self.image, line_color, (i * self.space, 0), (i * self.space, self.size[1]))
    @staticmethod
    def get_cpos(pos):
        return (int(pos[0] / 20 + 0.5) * 20, int(pos[1] / 20 + 0.5) * 20)
    def update(self, events):
        super(Board, self).update(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    if self.rect.collidepoint(pos):
                        pygame.draw.circle(self.image, utils.colors.black,
                                           Board.get_cpos(pos), self.space // 2)


class GameScene(state.Scene):
    def __init__(self):
        super(GameScene, self).__init__()
        self.board = Board(core.get_config().board_size)
        self.register_display(self.board)
        self.register_update(self.board)

if __name__ == '__main__':
    app = core.App(
        config={'board_size': (710, 600)}
    )
    scene = GameScene()
    sys.exit(app.run_with_state(scene))
