import sys
import pygame


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

    default_config = {
        'tick': 60,
        'screen_size': (800, 600),
        'bgcolor': (255, 255, 255),
        'caption': "App",
    }
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
        self.config = self.default_config
        if config is None:
            config = {}
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
