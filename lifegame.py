#!/usr/bin/env python3

import sys
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from lifegame_core import Cells

class LifegameWidget(Widget):
    def update(self, cells):
        self.canvas.clear()
        for y in range(cells.ny):
            for x in range(cells.nx):
                status = cells.cell(x, y)
                if status == Cells.ALIVE:
                    with self.canvas:
                        csize = (self.size[0]/cells.nx, self.size[1]/cells.ny)
                        Color(1, 0, 0)
                        Rectangle(pos=(csize[0]*x, csize[1]*y), size=csize)

class LifegameApp(App):
    def __init__(self, nx, ny, density, **kwargs):
        super(LifegameApp, self).__init__(**kwargs)
        self.cells = Cells(nx, ny, density)
        self.title = "Lifegame"
        self.gen = 0

    def build(self):
        root = BoxLayout(orientation='vertical')
        self.label = label = Label(text='0', size_hint=(None, 0.1))
        self.wid = wid = LifegameWidget()
        Clock.schedule_interval(self.update, period)
        root.add_widget(label)
        root.add_widget(wid)
        return root

    def update(self, dt):
        self.cells.survive()
        self.wid.update(self.cells)
        self.label.text = "gen={0}".format(self.gen)
        self.gen += 1

class LifegameConsole:
    DISPLAY_STATUS = {Cells.UNDEFINED: "?",
                      Cells.DEAD: ".",
                      Cells.ALIVE: "@"}

    def write(self, gen, cells):
        print("gen={0}".format(gen))
        for y in range(cells.ny):
            for x in range(cells.nx):
                status = cells.cell(x, y)
                print("{0} ".format(LifegameConsole.DISPLAY_STATUS[status]), end="")
            print("")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: {0} nx ny [density]".format(sys.argv[0]))
        quit()
    nx = int(sys.argv[1])
    ny = int(sys.argv[2])
    density = int(sys.argv[3])
    period = 0.5
    LifegameApp(nx, ny, density).run()

