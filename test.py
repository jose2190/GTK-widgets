import pygtk
pygtk.require("2.0")

import gtk

class TestWindow(gtk.Window):
    def __init__(self, title="Test"):
        super(TestWindow, self).__init__()
        self.set_title(title)

        self.connect("delete-event", self.main_quit)

    def main_quit(self, widget, event=None):
        gtk.main_quit()

    def start(self):
        self.show_all()
        gtk.main()

