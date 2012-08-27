#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This program is free software: you can redistribute it and/or modify
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
import sys
from dbus.mainloop.qt import DBusQtMainLoop

class Clementine:
  
	def __init__(self):
		self.bus = dbus.SessionBus()
		#try:
			#self.server = self.bus.get_object('org.mpris.clementine', '/Player')
			#self.tracklist = self.bus.get_object('org.mpris.clementine', '/TrackList')
			##qdbus org.mpris.clementine /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause 
			#self.mpris2 = self.bus.get_object('org.mpris.clementine', '/org/mpris/MediaPlayer2')
			#self.mpris2player = dbus.Interface(self.mpris2, dbus_interface='org.mpris.MediaPlayer2.Player')
		#except:
			#print "Clementine is not running? Exiting..."
			#sys.exit(-1)
		
		# Handle exception in http.py
		self.server = self.bus.get_object('org.mpris.clementine', '/Player')
		self.tracklist = self.bus.get_object('org.mpris.clementine', '/TrackList')
		self.mpris2 = self.bus.get_object('org.mpris.clementine', '/org/mpris/MediaPlayer2')
		self.mpris2player = dbus.Interface(self.mpris2, dbus_interface='org.mpris.MediaPlayer2.Player')
		self.propertiesManager = dbus.Interface(self.mpris2, 'org.freedesktop.DBus.Properties')
	
	def Next(self):
		self.server.Next()
		return True
  
	def Prev(self):
		self.server.Prev()
		return True
    
	def Play(self):
		self.server.Play()
		return True
	
	def Stop(self):
		self.server.Stop()
		return True
		
	def Pause(self):
		self.server.Pause()
		return True
	
	def GetInfo(self):
		return self.server.GetMetadata()
	
	def VolumeUp(self):
		self.server.VolumeUp(10)
		return True
	
	def VolumeDown(self):
		self.server.VolumeDown(10)
		return True
	
	def GetTrackNum(self):
		return self.tracklist.GetCurrentTrack()
	
	def GetListLength(self):
		return self.tracklist.GetLength()
	
	def GetTrackData(self,trackNumber):
		return self.tracklist.GetMetadata(trackNumber)
	
	def setNewTrack(self,trackNumber):
		self.tracklist.PlayTrack(trackNumber)
	
	def removeTrack(self,trackNumber):
		self.tracklist.DelTrack(trackNumber)
	
	def loadTrackList(self,url):
		self.mpris2player.OpenUri(url)
		
	def setShuffle(self,mode):
		self.propertiesManager.Set('org.mpris.MediaPlayer2.Player', 'Shuffle', mode)
		#self.mpris2player.Shuffle(mode)
		
	def getShuffle(self):
		return self.propertiesManager.Get('org.mpris.MediaPlayer2.Player', 'Shuffle')
		#return self.mpris2player.Shuffle()
		
	def setRepeat(self,mode):
		self.propertiesManager.Set('org.mpris.MediaPlayer2.Player', 'LoopStatus', mode)
		
	def getRepeat(self):
		return self.propertiesManager.Get('org.mpris.MediaPlayer2.Player', 'LoopStatus')
		
		
		
		
		
	
	#@dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ss', out_signature='v')
#def Get(self, interface, prop):
    #...
#@dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ssv')
#def Set(self, interface, prop, value):
    #...
#@dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='s', out_signature='a{sv}')
#def GetAll(self, interface):
    #...
    
    
    
    #- -----------------
    
    #proxy = bus.get_object('org.mpris.MediaPlayer2.rhythmbox','/org/mpris/MediaPlayer2')
#properties_manager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
#properties_manager.Set('org.mpris.MediaPlayer2.Player', 'Volume', 100.0)
#curr_volume = properties_manager.Get('org.mpris.MediaPlayer2.Player', 'Volume')