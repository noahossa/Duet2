#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import time

#--- enter the path to the log file below
f = "/path/to/terminal_log.txt"
#---

output1 = open(f).read().strip()

while True:
    time.sleep(1)
    output2 = open(f).read().strip()
    if output1 != output2:
        tx = output2.replace(output1, "")
        clipboard = gtk.clipboard_get()
        clipboard.set_text(tx)
        clipboard.store()
    output1 = output2
    