import pygame
import core


class State:
    """
    状态基类
    进行状态转移、处理
    """

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


class DisplayState(State):
    """
    显示注册的可视对象
    """
    def __init__(self):
        super().__init__()
        self.screen = core.get_app().screen
        self.display_os = []

    def display_all(self):
        rects = []
        for display_o in self.display_os:
            rects.extend(display_o.display(self.screen))
        pygame.display.update(rects)

    def register_display(self, display_o):
        assert issubclass(type(display_o), core.DisplayObject)
        self.display_os.append(display_o)

    def remove_display(self, display_o):
        if display_o in self.display_os:
            self.display_os.remove(display_o)

class UpdateState(State):
    """
    update注册的对象
    """
    def __init__(self):
        super().__init__()
        self.update_os = []

    def update_all(self, events):
        for update_o in self.update_os:
            update_o.update(events)

    def register_update(self, update_o):
        assert issubclass(type(update_o), core.UpdateObject)
        self.update_os.append(update_o)

    def remove_update(self, update_o):
        if update_o in self.update_os:
            self.update_os.remove(update_o)

class Scene(DisplayState, UpdateState):
    """
    场景
    """
    def __init__(self):
        DisplayState.__init__(self)
        UpdateState.__init__(self)

    def update(self, events):
        super(Scene, self).update(events)
        self.update_all(events)
        self.display_all()