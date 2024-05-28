import pygame as pg
import sys
import random
import time
from panel import Panel
from timer import Timer
from button import Button
import pickle

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


timer = Timer("0", pg.Rect(width / 2, 50, 50, 50))
mismatches = 0

load_bnt = Button(pg.Rect(width / 2 - 50, 150, 50, 50), "download.png", "download-hover.png")
save_bnt = Button(pg.Rect(width / 2 + 50, 150, 50, 50), "save.png", "save-hover.png")


def save_result():
    with open("result.txt", 'wa') as file:
        print(f"Вы прошли тренер за {time.time() - timer.tic:.2f} секунд, сделав {mismatches} ошибок", file=file)


guessed_panel = Panel('-', pg.Rect(width - width_of_panel * 3, height - height_of_panel * 3, width_of_panel * 3, height_of_panel * 3))
guessed_panel.state = 1
guessed_panel.change_size(40)
guessed = get_random_element(current_level)
guessed_panel.change_text(guessed)


while True:
    try:
        # noinspection PyInterpreter
        if guessed is None:
            current_level += 1
            guessed = get_random_element(current_level)
            guessed_panel.change_text(guessed)
    except IndexError:
        save_result()
        sys.exit(0)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if load_bnt.mouse_over():
                try:
                    with open('save.txt', 'r') as file:
                        panels.clear()
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
                                    level[-1].state = int(file.readline())
                            panels.append(level)
                        current_level = int(file.readline())
                        answered = list(map(lambda x: x[:-1], file.readlines()))
                except Exception:
                    pass
            if save_bnt.mouse_over():
                with open('save.txt', 'w') as file:
                    for row in panels:
                        for el in row:
                            print(el.state, file=file)
                    print(current_level, file=file)
                    print(*answered, sep="\n", file=file)
                    sys.exit(0)
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
                            mismatches += 1
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
        timer.draw(screen)
        save_bnt.draw(screen)
        load_bnt.draw(screen)
    guessed_panel.draw(screen)
    pg.display.flip()
    screen.fill((60, 60, 80))
