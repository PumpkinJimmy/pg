import sys
import pygame
from utils import ConfigDict

default_config = ConfigDict({
    'tick': 60,
    'screen_size': (800, 600),
    'bgcolor': (255, 255, 255),
    'caption': "App",
})

gconfig = default_config.copy()


class App:
    """
    应用程序类
    维护主设置及主循环
    单例，但由用户创建
    """

    class QuitApp(Exception):
        pass

    class AppException(Exception):
        pass

    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is not None:
            return cls.__instance
        else:
            raise cls.AppException("No instance yet")

    def __getattr__(self, item):
        try:
            value = self.config[item]
        except KeyError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, item))
        else:
            return value

    def __init__(self, startup_state=None, config=None):
        if App.__instance is not None:
            raise App.AppException("Double application instance.")
        App.__instance = self
        pygame.init()
        pygame.font.init()
        self.config = gconfig
        if config is None:
            config = ConfigDict()
        self.config.update(config)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.rect = self.screen.get_rect()
        pygame.display.set_caption(self.caption)
        self.screen.fill(self.bgcolor)
        pygame.display.flip()
        self.__state = None
        self.__next_state = startup_state

    def update_config(self, config):
        self.config.update(config)

    def set_config(self, **kwargs):
        self.update_config(kwargs)

    def startup(self):
        self.__next_state.enter()
        self.__state = self.__next_state

    def update(self):
        events = pygame.event.get()
        self.__state.update(events)
        if self.__next_state != self.__state:
            self.__state.exit()
            self.__next_state.enter()
            self.__state = self.__next_state

    def replace(self, state):
        self.__next_state = state

    def quit(self):
        self.__state.exit()
        raise self.QuitApp()

    def run(self):
        self.startup()
        try:
            while 1:
                self.clock.tick(self.tick)
                self.update()
        except self.QuitApp:
            return 0

    def run_with_state(self, state):
        self.__next_state = state
        return self.run()


def get_app():
    return App.instance()


def get_config():
    return gconfig


class DisplayObject:
    """
    可视对象
    """

    def __init__(self):
        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect((0, 0, 0, 0))

    def display(self, screen):
        return [screen.blit(self.image, self.rect)]


class UpdateObject:
    """
    可更新对象
    """

    def update(self, events):
        pass


class Node(DisplayObject, UpdateObject):
    """
    自动显示、更新孩子的节点
    """

    def __init__(self):
        DisplayObject.__init__(self)
        UpdateObject.__init__(self)
        self.children = []
        self.update_os = []
        self.display_os = []

    def add_child(self, child):
        assert issubclass(type(child), Node)
        self.children.append(child)

    def add_children(self, *children):
        for child in children:
            self.add_child(child)

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)

    def display(self, screen):
        rects = []
        for child in self.children:
            rects.extend(child.display(screen))
        for display_o in self.display_os:
            rects.extend(display_o.display(screen))
        rects.extend(super(Node, self).display(screen))
        return rects

    def register_display(self, display_o):
        assert issubclass(type(display_o), DisplayObject)
        self.display_os.append(display_o)

    def remove_display(self, display_o):
        if display_o in self.display_os:
            self.display_os.remove(display_o)

    def update(self, events):
        for child in self.children:
            child.update(events)
        for update_o in self.update_os:
            update_o.update(events)
        super(Node, self).update(events)

    def register_update(self, update_o):
        assert issubclass(type(update_o), UpdateObject)
        self.update_os.append(update_o)

    def remove_update(self, update_o):
        if update_o in self.update_os:
            self.update_os.remove(update_o)
