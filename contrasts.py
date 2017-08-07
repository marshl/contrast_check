import csv
import sys
import curses
import time
import argparse
import os


class Color:
    def __init__(self, label, r: int, g: int, b: int):
        self.label = label
        self.r, self.g, self.b = int(r), int(g), int(b)

    def float_r(self):
        return self.r / 255

    def float_g(self):
        return self.g / 255

    def float_b(self):
        return self.b / 255

    @staticmethod
    def to_luminosity(val):
        if val <= 0.03928:
            return val / 12.92
        else:
            return ((val + 0.055) / 1.055) ** 2.4

    def lum_r(self):
        return self.to_luminosity(self.float_r())

    def lum_g(self):
        return self.to_luminosity(self.float_g())

    def lum_b(self):
        return self.to_luminosity(self.float_b())

    def luminosity(self):
        return 0.2126 * self.lum_r() + 0.7152 * self.lum_g() + 0.0722 * self.lum_b()

    def __str__(self):
        return f'{self.r},{self.g},{self.b}'


class ColorClass:
    def __init__(self, label, old_color: Color, new_color: Color):
        self.label = label
        self.old_color, self.new_color = old_color, new_color

    def __str__(self):
        return f'{self.label}: {self.old_color} {self.new_color}'


def color_contrast(color1: Color, color2: Color):
    lum1, lum2 = color1.luminosity(), color2.luminosity()
    return (max(lum1, lum2) + 0.05) / (min(lum1, lum2) + 0.05)


def stdin_to_list():
    stdin_content = sys.stdin.read()
    stdin_csv = csv.reader(stdin_content.split("\n"), delimiter="\t")
    return [x for x in list(stdin_csv) if len(x) == 3]


def read_color_file(filename):
    with open(filename, 'r') as csv_file:
        csv_list = csv.reader(csv_file, delimiter="\t")
        return [x for x in list(csv_list) if len(x) == 2]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Find the color contrast of colors in the given file')
    parser.add_argument('filename', metavar='filename', nargs=1,
                        help='The input file')

    args = parser.parse_args()
    filename = args.filename[0]

    # values = stdin_to_list()
    values = read_color_file(filename)
    # colors = [ColorClass(x[0], Color(*x[1].split(',')), Color(*x[2].split(','))) for x in values]
    colors = [Color(x[0], *x[1].split(',')) for x in values]
    longest_name = max([len(x.label) for x in colors])

    aa_pass_count = sum(color_contrast(x, y) >= 4.5 for x in colors for y in colors)
    aaa_pass_count = sum(color_contrast(x, y) >= 7 for x in colors for y in colors)

    try:

        scr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        scr.keypad(True)

        max_x = scr.getmaxyx()[1]
        max_y = scr.getmaxyx()[0]

        scr.refresh()
        curses.noecho()

        cols = len(colors) * 7 + longest_name + 1
        rows = len(colors) * int(1 + round(cols / max_x, 0)) * 2 + 3

        curses.resizeterm(rows, cols)

        for i in range(len(colors)):
            color = colors[i]
            curses.init_color(i,
                              int(color.r * 1000 / 255),
                              int(color.g * 1000 / 255),
                              int(color.b * 1000 / 255))

        current_y = 1
        for y in range(len(colors)):
            color = colors[y]
            scr.addstr(current_y, 0, color.label)
            scr.addstr(current_y + 1, 0, f'({color.r},{color.g}, {color.b})')

            current_x = longest_name + 1

            for x in range(len(colors)):
                contrast_color = colors[x]
                pair_num = y * len(colors) + x + 1
                curses.init_pair(pair_num, x, y)

                contrast = color_contrast(contrast_color, color)

                if contrast > 7:
                    text = ' PASS '
                elif contrast > 4.5:
                    text = ' pass '
                else:
                    text = ' fail '

                if current_x + len(text) >= max_x:
                    current_x = longest_name
                    current_y += 1
                scr.addstr(current_y, current_x, text, curses.color_pair(pair_num))

                current_x += 7

            current_y += 2

        scr.addstr(current_y, 0, f'{aa_pass_count} color combinations pass AA')
        scr.addstr(current_y + 1, 0, f'{aaa_pass_count} color combinations pass AAA')

        scr.refresh()
        scr.getch()
        scr.getch()
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
