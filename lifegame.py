#!/usr/bin/env python3

import re
import sys
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from lifegame_core import Cells

class LifegameWidget(Widget):
    def _cellColor(self, gen):
        intensity = gen/100 + 0.3
        r = 1 if intensity > 1 else intensity
        return r

    def updateCanvas(self, cells):
        print('start updating')
        self.canvas.clear()
        for x in range(cells.nx):
            for y in range(cells.ny):
                if cells.cell(x,y) == Cells.ALIVE:
                    with self.canvas:
                        cs = (self.size[0]/cells.nx, self.size[1]/cells.ny)
                        Color(self._cellColor(cells.gen(x, y)), 0, 0)
                        Rectangle(size=cs, pos=(cs[0]*x + self.x, cs[1]*y + self.y))
        print('end updating')

class IntegerInput(TextInput):
    pattern = re.compile('[0-9]')

    def insert_text(self, substring, from_undo=False):
        s = ''
        for ch in substring:
            if self.pattern.match(ch):
                s += ch
        return super(IntegerInput, self).insert_text(s, from_undo=from_undo)

class LifegameRoot(Widget):
    triggerLabel = StringProperty('start')

    def __init__(self, **kwargs):
        super(LifegameRoot, self).__init__(**kwargs)
        self.isRunning = False
        self.isInitialized = False
        self.cells = None
        self.period = 0.5
        self.schedule = None
        self.ids['sizeX'].text = '100'
        self.ids['sizeY'].text = '100'
        self.ids['density'].text = '5'

    def initCells(self, force=False):
        if self.isInitialized == True and force == False:
            print('skip initializing')
            return
        nx = int(self.ids['sizeX'].text)
        ny = int(self.ids['sizeY'].text)
        density = int(self.ids['density'].text)
        print('nx={0} ny={1} density={2}'.format(nx, ny, density))
        self.cells = Cells(nx, ny, density)
        self.isInitialized = True

    def startCells(self):
        self.schedule = Clock.schedule_interval(self.updateCells, self.period)

    def stopCells(self):
        self.schedule.cancel()

    def updateCells(self, dt):
        start = time.time()
        self.cells.survive()
        now = time.time()
        elapsed = (now - start) * 1000
        print('elapsed={0}'.format(elapsed))
        self.ids['widget'].updateCanvas(self.cells)
        print('refreshed')

    def onPressTrigger(self):
        if self.isRunning:
            self.triggerLabel = 'start'
            self.isRunning = False
            self.stopCells()
        else:
            self.triggerLabel = 'stop'
            self.isRunning = True
            self.initCells()
            self.startCells()

    def onPressReset(self):
        if self.isRunning == False:
            self.ids['widget'].canvas.clear()
            self.initCells(force=True)

class LifegameApp(App):
    def __init__(self, **kwargs):
        super(LifegameApp, self).__init__(**kwargs)
        self.title = 'Lifegame'

    def build(self):
        return LifegameRoot()

if __name__ == '__main__':
    LifegameApp().run()

