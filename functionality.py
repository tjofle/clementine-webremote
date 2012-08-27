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

#import random
import urlparse
import unicodedata
import os
import time
import config
#from subprocess import call


class Functionality: 
	def __init__(self,http_path,clementine_driver):
		self.clementine = clementine_driver
		# TODO: move playlistDirectory functionality?

		self.playlistDirectory = config.playlistDirectory
		self.saveResult = ""	# used by web-UI to report failure to save playlist
		self.action = ""
		self.value = ""
		if '?' in http_path:
			http_path, tmp = http_path.split('?', 1)
			cmd = urlparse.parse_qs(tmp)
			self.action = self.cleanParameter(cmd['action'])
			if cmd.has_key('value'):	# value is generally track-ID or playlist name
				self.value = self.cleanParameter(cmd['value'])
		return
	#------	End of __init__
	
	def cleanParameter(self,uglyParameter):
		pureParameter = str(uglyParameter)
		pureParameter = pureParameter.replace('[','')
		pureParameter = pureParameter.replace(']','')
		pureParameter = pureParameter.replace('\'','')
		return pureParameter
	#------	cleanParameter()
	
	def run(self):
		if self.action == "Pause":
			self.clementine.Pause()
			# 
		elif self.action == "Play":
			self.clementine.Play()
			# 
		elif self.action == "Stop":
			self.clementine.Stop()
			# 
		elif self.action == "Next":
			self.clementine.Next()
			# 
		elif self.action == "Prev":
			self.clementine.Prev()
			# 
		elif self.action == "VolumeUp":
			self.clementine.VolumeUp()
			# 
		elif self.action == "VolumeDown":
			self.clementine.VolumeDown()
			# 
		elif self.action == "changeTrack":
			print self.value
			self.clementine.setNewTrack(int(self.value))
			# 
		elif self.action == "clearTrackList":
			self.clearTrackList()
			#
		elif self.action == "addTrackList":
			self.addTrackList(self.value)
			#
		elif self.action == "replaceTrackList":
			self.clearTrackList()
			self.addTrackList(self.value)
			#
		elif self.action == "saveTrackList":
			self.saveTrackList(self.value,False)	# Do not overwrite exsisting playlist
			#
		elif self.action == "forceSavePlaylist":
			self.saveTrackList(self.value,True)	# Overwrite exsisting playlist
			#
		elif self.action == "removeTrack":
			self.clementine.removeTrack(int(self.value))	
			#
		elif self.action == "setShuffle":
			if self.value == "on":
				self.clementine.setShuffle(True)
			if self.value == "off":
				self.clementine.setShuffle(False)
		elif self.action == "setRepeat":
			if self.value == "track":
				self.clementine.setRepeat("Track")
			if self.value == "playlist":
				self.clementine.setRepeat("Playlist")
			if self.value == "none":
				self.clementine.setRepeat("None")
		elif self.action == "startClementine":
			self.startClementine()
	#------	End of run()
	
	def startClementine(self):
		dummy = None
		#TODO: Implement this function
		#-- Start Clementine in not running?
		#-- Start Clementine when prompted by webUI?
		#call(["clementine", "&"])
		#print "Trying to start Clementine"
		#os.system("clementine &")
		#os.system("clementine --quiet >> clementineLogFile.log &")
		#os.system("some_command < input_file | another_command > output_file")
			
	def clearTrackList(self):
		listLength = int(self.clementine.GetListLength())
		#self.clementine.Stop()
		for x in reversed(range(0,listLength)):
			self.clementine.removeTrack(x)	
	#------	End of clearTrackList()
			
	def addTrackList(self, newList):
		base = "file:/"
		url = base + self.playlistDirectory + newList
		self.clementine.loadTrackList(url)
		# Wait here to avoid reloading the webpage before dBus can report correct tracklist length
		while int(self.clementine.GetListLength()) == 0:
			time.sleep(1)
			#print "waiting"
	#------	End of addTrackList()
	
	def saveTrackList(self, listName,force):
		fileExists = False
		invalidFilename = False
		listName = listName.encode('utf-8')
		if not(listName.endswith(".m3u")):
			listName += ".m3u"
		self.playlistFilename = listName # used by web to report success or failure to save
		
		# Check that listName does not already exist
		for filename in os.listdir(self.playlistDirectory):
			if str(filename).encode('utf-8') == listName:
				fileExists = True
		
		# Check that listName does not contain invalid characters
		if str("/") in listName:
			invalidFilename = True
		if str("..") in listName:
			invalidFilename = True
		self.invalidFilename = invalidFilename # used by web to report reason for failure
		
		if (fileExists and not(force)) or invalidFilename:
			#print "error could not save playlist: name \"" + listName + "\" already exists"
			self.saveResult = "Fail"
		else:
			fileName = self.playlistDirectory + listName
			fileHandle = open(fileName, 'w')
			self.createM3U(fileHandle)
			fileHandle.close()
			self.saveResult = "Success"
	#------	End of saveTrackList()
	
	def createM3U(self,outputFile):
		listLength = int(self.clementine.GetListLength())
		
		outputFile.write("#EXTM3U\n")
		for x in range(0,listLength):
			trackMetaData = self.clementine.GetTrackData(x)
			 
			if not(trackMetaData.has_key('title')):
				trackMetaData['title']=""
			if not(trackMetaData.has_key('artist')):
				trackMetaData['artist']=""
			if not(trackMetaData.has_key('time')):
				trackMetaData['time']="0"
			if not(trackMetaData.has_key('location')):
				trackMetaData['location']=""
			
			trackLength = (str(trackMetaData['time'])).encode('utf-8')
			artist = (trackMetaData['artist']).encode('utf-8')
			title = (trackMetaData['title']).encode('utf-8')
			trackUrl = (trackMetaData['location']).encode('utf-8')
			trackUrl = trackUrl.replace('file://','')
			
			
			outputFile.write("#EXTINF:")
			outputFile.write(trackLength)
			outputFile.write(",")
			outputFile.write(artist)
			outputFile.write(" - ")
			outputFile.write(title)
			outputFile.write("\n")
			outputFile.write(trackUrl)
			outputFile.write("\n")
	#------	End of createM3U()

