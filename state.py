import pygame
import core
class State:
    """
    状态基类
    进行状态转移、处理
    """

    def __init__(self):
        pass

    def enter(self):
        pass

    def update(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.on_quit()

    def exit(self):
        pass

    def on_quit(self):
        core.get_app().quit()
