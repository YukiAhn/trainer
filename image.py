import pygame as pg


class Image:
    def __init__(self, rect: pg.Rect, image_ref: str, resizeable: bool = True):
        self.rect: pg.Rect = pg.Rect(rect)
        self.image_ref = pg.image.load(image_ref).convert_alpha()
        self.image = pg.transform.scale(self.image_ref, rect.size)
        self.rect.size = self.image.get_rect().size
        self.resizeable = resizeable

    def move(self, x: int, y: int) -> None:
        self.rect.topleft = x, y

    def resize(self, width: int, height: int) -> None:
        if not self.resizeable:
            return
        self.image = pg.transform.scale(self.image_ref, (width, height))
        self.rect.size = width, height

    def draw(self, display: pg.Surface) -> None:
        display.blit(self.image, self.rect.topleft)
