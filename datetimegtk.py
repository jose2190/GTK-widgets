# -*- coding: utf-8 -* 

"""
CalendarEntry:
Matí­as Alejandro Torres

TimerPicker
Encontrado en algun ricon de internet que no logro recordar,
si alguien reconoce el codigo hagamelo saber para hacer
la debida mencion :)

"""

import pygtk 
import gtk 
import datetime 
import time 
import gobject 
import logging

class CalendarEntry (gtk.HBox): 
    __gsignals__ = { 
        'changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )) 
    } 
    def __init__(self): 
        gtk.HBox.__init__ (self, False, 0) 
        self.calendar = gtk.Calendar () 
        self.entry = gtk.Entry () 
        self.button = gtk.Button (label = '^') 
        self.cwindow = gtk.Window (gtk.WINDOW_TOPLEVEL) 
        self.display = False 
        self.currentDate = datetime.date.today() 
                        
        self.cwindow.set_position (gtk.WIN_POS_MOUSE) 
        self.cwindow.set_decorated (False) 
        self.cwindow.set_modal (True) 
        self.cwindow.add(self.calendar) 
        
        self.entry.set_width_chars (10) 
        
        self.pack_start(self.entry, True, True, 0) 
        self.pack_start(self.button, False, False, 0) 
        
        self.__connect_signals () 
        self.update_entry () 

    def __connect_signals(self): 
        self.day_selected_handle = self.calendar.connect ('day-selected', self.update_entry) 
        self.day_selected_double_handle = self.calendar.connect ('day-selected-double-click', self.hide_widget) 
        self.clicked_handle = self.button.connect ('clicked', self.show_widget) 
        self.activate = self.entry.connect ('activate', self.update_calendar) 
        self.focus_out = self.entry.connect ('focus-out-event', self.focus_out_event) 
            
    def __block_signals(self): 
        self.calendar.handler_block (self.day_selected_handle) 
        self.calendar.handler_block (self.day_selected_double_handle) 
        self.button.handler_block (self.clicked_handle) 
        self.entry.handler_block (self.activate) 
        self.entry.handler_block (self.focus_out) 
    
    def __unblock_signals(self): 
        self.calendar.handler_unblock (self.day_selected_handle) 
        self.calendar.handler_unblock (self.day_selected_double_handle) 
        self.button.handler_unblock (self.clicked_handle) 
        self.entry.handler_unblock (self.activate) 
        self.entry.handler_unblock (self.focus_out) 

    def get_text(self): 
            return self.entry.get_text () 

    def set_date(self, date): 
        if not date: 
            date = datetime.date.fromtimestamp (time.time()) 
        self.currentDate = date 
        self.__block_signals () 
        self.calendar.select_day (1) 
        self.calendar.select_month (self.currentDate.month-1, self.currentDate.year) 
        self.calendar.select_day (self.currentDate.day) 
        self.__unblock_signals () 
        self.update_entry () 

    def get_date(self): 
        return self.currentDate 

    def hide_widget(self, *args): 
        self.cwindow.hide_all () 

    def show_widget(self, *args): 
        self.cwindow.show_all () 

    def update_entry(self, *args): 
        year,month,day = self.calendar.get_date () 
        month = month +1; 
        self.currentDate = datetime.date(year, month, day) 
        text = self.currentDate.strftime ("%d/%m/%Y") 
        self.entry.set_text (text) 
        self.emit('changed', self.currentDate) 

    def update_calendar(self, *args): 
        try: 
            dt = datetime.datetime.strptime (self.entry.get_text (), "%d/%m/%Y") 
        except: 
            try: 
                dt = datetime.datetime.strptime (self.entry.get_text (), "%d/%m/%y") 
            except: 
                logging.info ('CalendarEntry.update_calendar: Error parsing date, setting it as today...') 
                dt = datetime.date.fromtimestamp(time.time()) 
                
        self.set_date (dt) 
        self.hide_widget () 
    
    def focus_out_event(self, widget, event): 
        self.update_calendar() 
        self.hide_widget () 


class TimePicker(gtk.VBox):
    def __init__(self):
        super(TimePicker, self).__init__()
        sp_h_adj = gtk.Adjustment(0, 0, 24, 1, 10, 0)
        self.sp_h = gtk.SpinButton(sp_h_adj, 1, 0)
        self.sp_h.set_numeric(True)
        self.sp_h.set_size_request(50, 27)

        sp_m_adj = gtk.Adjustment(0, 0, 59, 1, 10, 0)
        self.sp_m = gtk.SpinButton(sp_m_adj, 1, 0)
        self.sp_m.set_numeric(True)
        self.sp_m.set_size_request(45, 27)

        sp_s_adj = gtk.Adjustment(0, 0, 59, 1, 10, 0)
        self.sp_s = gtk.SpinButton(sp_s_adj, 1, 0)
        self.sp_s.set_numeric(True)
        self.sp_s.set_size_request(45, 27)

        box = gtk.HBox()
        box.pack_start(self.sp_h, False)
        box.pack_start(self.sp_m, False)
        box.pack_start(self.sp_s, False)

        self.pack_start(box, False)
        self.show_all()


    def get_time(self):
        """Start choosen process"""
        # Get spinbutton values as int, calculate total and current time
        h = self.sp_h.get_value_as_int()
        m = self.sp_m.get_value_as_int()
        s = self.sp_s.get_value_as_int()

        t = datetime.time(h, m, s)
        return t
    
    def set_time(self, time):
        self.sp_h.set_value(time.hour)
        self.sp_m.set_value(time.minute)
        self.sp_s.set_value(time.second)

class DateTimeEntry (gtk.HBox): 
    __gsignals__ = { 
        'changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )) 
    } 
    def __init__(self): 
        gtk.HBox.__init__ (self, False, 0) 
        self.calendar = gtk.Calendar () 
        self.entry = gtk.Entry () 
        self.button = gtk.Button (label = '^') 
        self.cwindow = gtk.Window (gtk.WINDOW_TOPLEVEL) 
        self.display = False 
        self.currentDate = datetime.date.today() 
                        
        self.cwindow.set_position (gtk.WIN_POS_MOUSE) 
        self.cwindow.set_decorated (False) 
        self.cwindow.set_modal (True) 

        self.timepicker = TimePicker()
        self.btn_done = gtk.Button("Hecho")
        box2 = gtk.HBox()
        box2.pack_start(self.timepicker, False)
        box2.pack_start(self.btn_done)

        box = gtk.VBox()
        box.pack_start(self.calendar, False)
        box.pack_start(box2, False)

        self.cwindow.add(box) 
        
        self.entry.set_width_chars (10) 
        
        self.pack_start(self.entry, True, True, 0) 
        self.pack_start(self.button, False, False, 0) 
        
        self.__connect_signals () 
        self.update_entry () 

    def __connect_signals(self): 
        self.day_selected_handle = self.calendar.connect ('day-selected', self.update_entry) 
        self.day_selected_double_handle = self.calendar.connect ('day-selected-double-click', self.hide_widget) 
        self.clicked_handle = self.button.connect ('clicked', self.show_widget) 
        self.activate = self.entry.connect ('activate', self.update_calendar) 
        self.focus_out = self.entry.connect ('focus-out-event', self.focus_out_event) 
        self.click = self.btn_done.connect("clicked", self.on_done_clicked)
            
    def __block_signals(self): 
        self.calendar.handler_block (self.day_selected_handle) 
        self.calendar.handler_block (self.day_selected_double_handle) 
        self.button.handler_block (self.clicked_handle) 
        self.entry.handler_block (self.activate) 
        self.entry.handler_block (self.focus_out) 
    
    def __unblock_signals(self): 
        self.calendar.handler_unblock (self.day_selected_handle) 
        self.calendar.handler_unblock (self.day_selected_double_handle) 
        self.button.handler_unblock (self.clicked_handle) 
        self.entry.handler_unblock (self.activate) 
        self.entry.handler_unblock (self.focus_out) 
    
    def on_done_clicked(self, widget):
        self.update_entry()
        self.hide_widget()
        
    def get_text(self): 
            return self.entry.get_text () 

    def set_datetime(self, date): 
        if not date: 
            date = datetime.datetime.fromtimestamp(time.time()) 
        self.currentDate = date 
        self.__block_signals () 
        self.calendar.select_day(1) 
        self.calendar.select_month (self.currentDate.month-1, self.currentDate.year) 
        self.calendar.select_day(self.currentDate.day) 

        t = datetime.time(date.hour, date.minute, date.second)
        self.timepicker.set_time(t)
        self.__unblock_signals () 
        self.update_entry () 

    def get_datetime(self): 
        dt = datetime.datetime(self.currentDate.year, self.currentDate.month,
            self.currentDate.day, self.currentDate.hour, self.currentDate.minute,
            self.currentDate.second)

        return dt 

    def hide_widget(self, *args): 
        self.cwindow.hide_all() 

    def show_widget(self, *args): 
        self.cwindow.show_all() 

    def update_entry(self, *args): 
        year,month,day = self.calendar.get_date() 
        month = month +1; 
        t = self.timepicker.get_time()
        self.currentDate = datetime.datetime(year, month, day, t.hour, t.minute, t.second) 
        text = self.currentDate.strftime("%d/%m/%Y %H:%M:%S") 
        self.entry.set_text(text) 
        self.emit('changed', self.currentDate) 

    def update_calendar(self, *args): 
        try: 
            dt = datetime.datetime.strptime(self.entry.get_text (), "%d/%m/%Y %H:%M:%S") 
        except: 
            try: 
                dt = datetime.datetime.strptime(self.entry.get_text (), "%d/%m/%y %H:%M:%S") 
            except: 
                logging.info ('CalendarEntry.update_calendar: Error parsing date, setting it as today...') 
                dt = datetime.datetime.fromtimestamp(time.time()) 
                
        self.set_datetime(dt) 
        self.hide_widget() 
    
    def focus_out_event(self, widget, event): 
        self.update_calendar() 
        self.hide_widget() 

    
