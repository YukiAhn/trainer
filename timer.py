import pygame as pg
import time


class Timer:
    def __init__(self, title, rect):
        self.text = title
        self.rect: pg.Rect = rect
        self.tic = time.time()
        self.font = "SourceSansPro-Regular.ttf"
        self.size = 40
        self.color = pg.Color((255, 0, 0))
        self._config_font()
        self._config_text()

    def _config_font(self):
        try:
            self.graphic_font = pg.font.Font(self.font, self.size)
        except OSError:  # can't read font file.
            self.graphic_font = pg.font.SysFont(self.font, self.size)

    def _config_text(self):
        self.graphic_text = self.graphic_font.render(self.text, True, self.color)

    def draw(self, display):
        self.change_text(f"Таймер = {time.time() - self.tic:.2f} секунд")
        x = self.rect.centerx - self.graphic_text.get_rect().width // 2
        y = self.rect.centery - self.graphic_text.get_rect().height // 2
        display.blit(self.graphic_text, (x, y))

    def change_text(self, text: str) -> None:
        self.text = text
        self._config_text()

    def change_size(self, size: int):
        self.size = size
        self._config_font()
        self._config_text()
