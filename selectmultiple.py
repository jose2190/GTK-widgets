"""
Este control esta basado en un codigo encontrado en algun rincon del web
que no logro recordar, si alguien reconoce el codigo
hagamelo saber para hacer la debida mencion :)
"""

import pygtk
pygtk.require('2.0')
import gtk
import gobject


class SelectMultiple(gtk.ScrolledWindow):
    """
    Control para crear una lista de seleccion multiple
    """
    def __init__(self, rows):
        super(SelectMultiple, self).__init__()
        self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        self.__rows = rows
        self.__create_list()
        self.show_all()
    
    def __create_list(self):
        self.__list = gtk.ListStore(gobject.TYPE_STRING)
        for row in self.__rows:
            self.__list.append((row, ))

        self.__treeview = gtk.TreeView()
        self.__treeview.set_model(self.__list)

        column = gtk.TreeViewColumn()
        cell = gtk.CellRendererText()
        column.pack_start(cell)
        column.add_attribute(cell,'text',0)
        self.__treeview.append_column(column)
        self.__treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

        self.add(self.__treeview)
    
    def get_selected(self):
        treeselection = self.__treeview.get_selection()
        (model, pathlist) = treeselection.get_selected_rows()

        return pathlist
    
    def select(self, index):
        """
        selecciona el indice recibido
        """
        treeselection = self.__treeview.get_selection()
        treeselection.select_path((index,))
    
    def unselect_all(self):
        treeselection = self.__treeview.get_selection()
        treeselection.unselect_all()


if __name__ == "__main__":
    from test import TestWindow

    list = []
    for i in range(15):list.append("item %s"%i)

    win = TestWindow()
    select = SelectMultiple(list)
    win.add(select)
    win.start()
