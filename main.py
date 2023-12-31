import pygame as pg
import sys
import random
from panel import Panel

pg.init()  # Инициализируем pygame

width = 1800
height = 1000
width_of_panel = 100
height_of_panel = 100
current_level = 0
answered = []

screen = pg.display.set_mode((width, height))  # Инициализируем окно приложения

periodic_table = [
    ['H', *[None] * 16, 'He'],
    ['Li', 'Be', *[None] * 10, 'B', 'C', 'N', 'O', 'F', 'Ne'],
    ['Na', 'Mg', *[None] * 10, 'Al', 'Si', 'P', 'S', 'Cl', 'Ar'],
    ['K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr'],
    ['Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe'],
    ['Cs', 'Ba', 'Lantanoids', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn'],
    ['Fr', 'Ra', 'Actinoids', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Hh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'],

]

panels = []

for i, row in enumerate(periodic_table):
    level = []
    for j, el in enumerate(row):
        if el is not None:
            level.append(Panel(el,
                                pg.Rect(
                                    j * width_of_panel, i * height_of_panel,
                                    width_of_panel, height_of_panel)
                                )
                          )
    panels.append(level)


def get_random_element(level: int):
    data = [el for el in periodic_table[level] if el is not None and el not in answered]
    if len(data) == 0:
        return None
    return random.choice(data)


guessed_panel = Panel('-', pg.Rect(width - width_of_panel * 3, height - height_of_panel * 3, width_of_panel * 3, height_of_panel * 3))
guessed_panel.state = 1
guessed_panel.change_size(40)
guessed = get_random_element(current_level)
guessed_panel.change_text(guessed)

while True:
    try:
        if guessed is None:
            current_level += 1
            guessed = get_random_element(current_level)
            guessed_panel.change_text(guessed)
    except IndexError:
        sys.exit(0)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            for row in panels[:current_level + 1]:
                for el in row:
                    if el.mouse_over() and el.text not in answered:
                        answered.append(el.text)
                        for sub_el in row:
                            if sub_el.state == 3:
                                sub_el.state = 2
                        if guessed == el.text:
                            el.state = 1
                        else:
                            el.state = 2
                            answered.append(guessed)
                            for sub_el in row:
                                if sub_el.text == guessed:
                                    sub_el.state = 3
                        try:
                            guessed = get_random_element(current_level)
                            if guessed is None:
                                current_level += 1
                                guessed = get_random_element(current_level)
                        except IndexError:
                            current_level = 0
                            for row in panels:
                                for el in row:
                                    if el.state != 1:
                                        answered.remove(el.text)
                                        el.state = 0
                            guessed = get_random_element(current_level)
                        guessed_panel.change_text(guessed)

    for row in panels[:current_level + 1]:
        for el in row:
            el.draw(screen)
    guessed_panel.draw(screen)
    pg.display.flip()
    screen.fill((60, 60, 80))
