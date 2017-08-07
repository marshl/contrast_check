import csv
import sys
import curses
import time
import argparse


class Color:
    def __init__(self, r: int, g: int, b: int):
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
        return [x for x in list(csv_list) if len(x) == 3]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Find the color contrast of colors in the given file')
    parser.add_argument('filename', metavar='filename', nargs=1,
                        help='The input file')

    args = parser.parse_args()
    filename = args.filename[0]

    # values = stdin_to_list()
    values = read_color_file(filename)
    colors = [ColorClass(x[0], Color(*x[1].split(',')), Color(*x[2].split(','))) for x in values]

    scr = curses.initscr()
    curses.start_color()
    scr.keypad(True)
    scr.refresh()
    curses.noecho()

    pad = curses.newpad(len(colors) + 1, 100)

    for y in range(len(colors)):
        color = colors[y]
        pad.addstr(y + 1, 0, color.label)

        curses.init_color(curses.COLOR_BLACK, 255, 0, 0)

        for x in range(len(colors)):
            contrast_color = colors[x]
            pad.addstr(y + 1, 15 + 5 * x, 'foo')

    pad.refresh(0, 0, 0, 1, 20, 75)

    scr.getch()
    # curses.nocbreak()
    # curses.echo()
    curses.endwin()

    # for color in colors:
    #     print(color)
    #
    # for color1 in colors:
    #     for color2 in colors:
    #         print(str(color_contrast(color1.old_color, color2.old_color)))

    # print(Color(255, 255, 255).luminosity())
    blue = Color(0, 0, 255)
    white = Color(247, 247, 247)

    # print(color_contrast(blue, white))
