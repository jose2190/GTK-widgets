#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gobject
import gtk


class ImageButton(gtk.Button):
    def __init__(self, image, label="", position=gtk.POS_TOP):
        super(ImageButton, self).__init__()
        img = gtk.Image()
        img.set_from_file(image)
        if label:
            lbl = gtk.Label(label)

        if position == gtk.POS_TOP or position == gtk.POS_BOTTOM:
            box = gtk.VBox()
        else:
            box = gtk.HBox()
        if position == gtk.POS_TOP or position == gtk.POS_LEFT:
            box.pack_start(img, False)
            if label:
                box.pack_start(lbl)
        elif position == gtk.POS_BOTTOM or position == gtk.POS_RIGTH:
            if label:
                box.pack_start(lbl, False)
            box.pack_start(img)

        self.add(box)
        self.show_all()

class ImagePressButton(gtk.ToggleButton):
    def __init__(self, image, label="", position=gtk.POS_TOP):
        super(ImagePressButton, self).__init__()
        img = gtk.Image()
        img.set_from_file(image)
        if label:
            lbl = gtk.Label(label)

        if position == gtk.POS_TOP or position == gtk.POS_BOTTOM:
            box = gtk.VBox()
        else:
            box = gtk.HBox()
        if position == gtk.POS_TOP or position == gtk.POS_LEFT:
            box.pack_start(img, False)
            if label:
                box.pack_start(lbl, False)
        elif position == gtk.POS_BOTTOM or position == gtk.POS_RIGTH:
            if label:
                box.pack_start(lbl, False)
            box.pack_start(img, False)
        self.add(box)
        self.show_all()

if __name__ == "__main__":
    from test import TestWindow

    import os
    path = os.path.join(os.path.dirname(__file__), "cancel.png")
    imagebtn = ImageButton(path)
    imagebtn2 = ImageButton(path, label="Cancelar")

    win = TestWindow()
    hbox = gtk.HBox()
    hbox.pack_start(imagebtn)
    hbox.pack_start(imagebtn2)
    win.add(hbox)
    win.start()
