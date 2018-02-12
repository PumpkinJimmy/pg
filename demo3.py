import sys, random, math
import pygame
import core
import state


class Ball:
    def __init__(self):
        self.image = pygame.image.load("resource/ball.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = [random.choice([-2, 2]), random.choice([-2, 2])]

    def dis(self, other):
        return math.sqrt((self.rect.centerx - other.rect.centerx) ** 2 + \
                         (self.rect.centery - other.rect.centery) ** 2)

    def move(self):
        if self.rect.top < 0 or self.rect.bottom > 600:
            self.speed[1] = - self.speed[1]
        if self.rect.left < 0 or self.rect.right > 800:
            self.speed[0] = -self.speed[0]
        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]

    def reverse(self):
        self.speed[0] = -self.speed[0]
        self.speed[1] = -self.speed[1]


class MyState(state.State):
    def enter(self):
        self.balls = [Ball() for i in range(4)]
        for index, ball in enumerate(self.balls):
            ball.rect.topleft = (index % 3 * 200, index // 3 * 200)
        self.app = core.App.instance()
        self.app.screen.fill((255, 255, 255))

    def update(self, events):
        super(MyState, self).update(events)
        self.app.screen.fill((255, 255, 255))
        for ball in self.balls:
            ball.move()
        for ball in self.balls[:]:
            self.balls.remove(ball)
            for ballx in self.balls:
                if ball.dis(ballx) <= 120:
                    ball.reverse()
            self.balls.append(ball)
        for ball in self.balls:
            self.app.screen.blit(ball.image, ball.rect)
        pygame.display.flip()


if __name__ == "__main__":
    startup = MyState()
    app = core.App()
    sys.exit(app.run_with_state(startup))
