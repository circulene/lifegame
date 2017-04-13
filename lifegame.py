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
                        unit = 10
#                        scale = (cells.nx/self.canvas.size[0], cells.ny/self.canvas.size[1])
                        Color(1, 0, 0)
                        Rectangle(pos=(x*unit, y*unit), size=(unit, unit))
#                        Rectangle(pos=(scale[0]*x*unit, scale[1]*y*unit), size=(unit, unit))

class LifegameApp(App):
    def build(self):
        self.cells = Cells(nx, ny)
        self.title = "Lifegame"
        self.gen = 0
        self.console = LifegameConsole()
        root = BoxLayout(orientation='vertical')
        self.label = label = Label(text='0')
        self.wid = wid = LifegameWidget()
        Clock.schedule_interval(self.update, period)
        layout = BoxLayout(size_hint=(1, None), height=50)
        root.add_widget(layout)
        root.add_widget(label)
        root.add_widget(wid)
        return root

    def update(self, dt):
        self.cells.survive()
        self.wid.update(self.cells)
        self.console.write(self.gen, self.cells)
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
        print("usage: {0} nx ny".format(sys.argv[0]))
        quit()
    nx = int(sys.argv[1])
    ny = int(sys.argv[2])
    period = 0.5
    LifegameApp().run()

