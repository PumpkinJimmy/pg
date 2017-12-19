import random
import pygame
from core import App
import state


class MyScene(state.State):
    def enter(self):
        self.app = App.instance()
        self.app.screen.fill((255, 255, 255))
        self.screen = pygame.Surface((50, 50))
        self.screen.fill((255, 255, 255))
        pygame.draw.circle(self.screen, (255, 0, 0), (25, 25), 25, 0)
        self.rect = self.screen.get_rect()
        self.rect.topleft = (0, 0)
        self.speed = [random.randint(1, 5), random.randint(1, 5)]
        self.app.screen.blit(self.screen, self.rect)
        pygame.display.flip()

    def update(self, events):
        super(MyScene, self).update(events)
        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]
        if self.rect.right >= self.app.rect.right:
            self.speed[0] = -self.speed[0]
        if self.rect.bottom >= self.app.rect.bottom:
            self.speed[1] = -self.speed[1]
        if self.rect.left <= self.app.rect.left:
            self.speed[0] = -self.speed[0]
        if self.rect.top <= self.app.rect.top:
            self.speed[1] = -self.speed[1]
        self.app.screen.fill((255, 255, 255))
        self.app.screen.blit(self.screen, self.rect)
        pygame.display.flip()


if __name__ == "__main__":
    app = App()
    startup = MyScene()
    app.run_with_state(startup)
