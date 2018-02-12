class DisplayObject:
    """
    可视对象
    """
    def render(self, screen):
        return screen.blit(self.image, self.rect)

