#!/usr/bin/env python
# -*- coding: utf-8 -*-

#	 This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import dbus
import dbus.service
from dbus.mainloop.qt import DBusQtMainLoop

class Clementine:
  
  def __init__(self):
    self.bus = dbus.SessionBus()
    self.server = self.bus.get_object('org.mpris.clementine', '/Player')
  
  def Next(self):
    self.server.Next()
    return True
  
  def Prev(self):
    self.server.Prev()
    return True
    
  def Stop(self):
    self.server.Stop()
    return True
    
  def Pause(self):
    self.server.Pause()
    return True
    
  def GetInfo(self):
    return self.server.GetMetadata()
