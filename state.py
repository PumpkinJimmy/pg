import pygame
from core import App
class State:
    """
    状态
    处理，事件与渲染
    可以进行状态转移
    管理下属对象
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
        App.instance().quit()