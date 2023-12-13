import pygame as pg


class Panel:
    def __init__(self, title, rect):
        self.text = title
        self.rect: pg.Rect = rect
        self.state = 0  # 0 - сокрыто, 1 - правильно, 2 - неправильно
        self.font = "SourceSansPro-Regular.ttf"
        self.size = 20
        self.color = pg.Color((0, 0, 0))
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
        pg.draw.rect(display, (0, 0, 0), self.rect)
        if self.state == 0:
            pg.draw.rect(display, (100, 100, 100), (self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4))
        if self.state == 1:
            pg.draw.rect(display, (100, 150, 100), (self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4))
        if self.state == 2:
            pg.draw.rect(display, (150, 000, 100), (self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4))
        if self.state == 3:
            pg.draw.rect(display, (100, 000, 200), (self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4))
        if self.state != 0:
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

    def mouse_over(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            return True
        return False