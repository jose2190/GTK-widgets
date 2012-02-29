#!/usr/bin/env python
import sys
import os

import gobject
import gtk


class DataList(gtk.ScrolledWindow):
    """
    Control para crear una lista de objectos gtk.TreeStore.

    * Debe recibir una tupla/lista de tuplas/listas con nombre de la columna
    y ancho:
    ( ("Producto", 200), ("Precio", 100), ("Cantidad", 150), )

    * Puede tener un valor extra que indique el tipo de columna:
    ( ("Producto",200,gobject.TYPE_STRING),("Precio", 100,gobject.TYPE_DOUBLE),
        ("Cantidad", 150, gobject.TYPE_INT), )

    Si no se pasa el tercer argumento se pondra la columna como de tipo texto
    (gobject.TYPE_STRING)
    """
    def __init__(self, columns):
        super(DataList, self).__init__()
        self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        self.__columns = columns
        self.__create_list()
        self.show_all()

    def __create_list(self):
        """
        crea la lista y sus columnas
        """
        types = []
        self.__cols = len(self.__columns)
        for c in self.__columns:
            if len(c) == 3:
                types.append(c[2])
            else:
                types.append(gobject.TYPE_STRING)

        self.__lstore = gtk.TreeStore(*types)

        self.__treeview = gtk.TreeView(self.__lstore)
        self.__treeview.set_rules_hint(True)
        self.add(self.__treeview)

        # agregamos columnas
        for i, col in enumerate(self.__columns):
            column = gtk.TreeViewColumn(col[0], gtk.CellRendererText(), text=i)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
            column.set_fixed_width(col[1])
            self.__treeview.append_column(column)

    def __set_properties(self):
        pass

    def get_treestore(self):
        """
        devuelve el TreeStore
        """
        return self.__lstore

    def add_row(self, data, niter=None):
        """
        agrega una nueva fila, recibe una lista de strings.

        solo agregara tantas columnas como tenga creada la lista.

        En caso de recibirse iter agrega una subfila a la fila existente.
        """
        if not niter:
            iter = self.__lstore.append(None)
        else:
            iter = self.__lstore.append(niter)

        for i, item in enumerate(data):
            if i < self.__cols:
                self.__lstore.set(iter, i, item)


    def delete_row(self, index):
        """
        elimina una fila de la lista

        debe pasarsele el indice de la fila a eliminar
        """
        niter = self.__lstore.get_iter((index,))
        self.__lstore.remove(niter)

    def delete_selected(self):
        """
        elimina la fila seleccionada
        """
        selection = self.__treeview.get_selection()
        model, iter = selection.get_selected()
        model.remove(iter)

    def select_row(self, path):
        """
        selecciona la fila especificada
        """
        self.__treeview.set_cursor(path)

    def get_selected(self):
        """
        devuelve una tupla de valores de la fila seleccionada, en caso de no
        haber ninguna seleccionada se devuelve None
        """
        selection = self.__treeview.get_selection()
        model, iter = selection.get_selected()

        if not iter:return None

        args = []
        for i in range(self.__cols):args.append(i)

        return model.get(iter, *args)

    def get_path_selected(self):
        """
        devuelve el path del elemento seleccionado, en caso
        de no haber devuelve una tupla vacia
        """
        niter = self.get_iter_selected()
        if niter:
            # se obtiene el indice de la fila
            return self.__lstore.get_path(niter)
        else:
            return ()

    def get_iter(self, path):
        """
        devuelve el iter del treeview
        """
        return self.__lstore.get_iter(path)

    def get_iter_selected(self):
        """
        devuelve el iter de la fila seleccionada, en caso de
        no haber seleccionada devuelve None
        """
        selection = self.__treeview.get_selection()
        model, iter = selection.get_selected()

        return iter

    def clear(self):
        """ elimina todas las filas de a lista """
        self.__lstore.clear()

    def set_value(self, niter, col, value):
        """
        establece el valor de celda
        """
        self.__lstore.set_value(niter, col, value)

    def expand_to_path(self, path):
        """
        expande la fila del path recibido
        """
        self.__treeview.expand_to_path(path)


    def connect_signal(self, signal, callback):
        """
        conecta una senial con la funcion obtenida
        """
        self.__treeview.connect(signal, callback)

    def set_focus(self):
        """
        pone el focus en el treeview
        """
        self.__treeview.grab_focus()


if __name__ == "__main__":
    from test import TestWindow

    sample_list = (
        ("Texto 1", 100),
        ("Texto2", 300),
        ("Entero", 100, gobject.TYPE_INT),
        ("Flotante", 50, gobject.TYPE_FLOAT),
    )

    row = ("texto 1", "Texto 2", 5, 300.5)
    win = TestWindow()
    datalist = DataList(sample_list)
    datalist.add_row(row)
    win.add(datalist)
    win.start()


