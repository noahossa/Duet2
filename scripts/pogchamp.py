#import pyperclip
import mecode
import csv

from mecode import G

g = G()
g.home()
g.abs_move(z=478.91, y=5)  # move 10mm in x and 10mm in y
g.move(y=-10)
g.move(y=5)
g.move(z=84)
g.move(y=-10)
g.move(y=5)
g.abs_move(z=1278.39)
g.move(y=-10)
g.move(y=5)
g.move(z=84)
g.move(y=-10)
g.move(y=5)
g.home()  # move the tool head to the origin (0, 0)


# pyperclip.copy(str(g)) dumbbbbbbb

# g.view()
