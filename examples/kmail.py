#!/usr/bin/env python
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import duckylights

DBusGMainLoop(set_as_default=True)

session_bus = dbus.SessionBus()

with duckylights.keyboard() as dev, dev.programming() as ducky:
    def changed(a,b):
        count = min(10, int(b['count']))
        colors = ['000000'] * (6 * 22)
        colors[count*6+1] = 'ff0000'
        ducky.custom_mode(colors)

    session_bus.add_signal_receiver(changed, 'Update', 'com.canonical.Unity.LauncherEntry')

    from gi.repository import GLib

    loop = GLib.MainLoop()
    loop.run()
