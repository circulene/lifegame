#!/usr/bin/env python3
import timeit
from lifegame_core import Cells


def bench(size):
    setup="""\
from lifegame_core import Cells
cells = Cells({0}, {0})"""
    num = 10
    time = timeit.timeit(setup=setup.format(size), stmt="cells.survive()", number=num)
    print("size={0} elapsed={1} ms".format(size, time/num*1000))

bench(50)
bench(100)
bench(300)
bench(1000)
