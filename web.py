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

import random
import unicodedata
import os

class Web:
	def __init__(self):
		#TODO: remove need for self.dummy
		# dummy is currently needed to contrsuct Web-object without parsing parameters to constructor
		self.dummy = None
	#------	__init__()
	
	# TODO: restrucutre code to avoid need for 'info'
	def initInfo(self,info):
		self.info = info
		if not(self.info.has_key('album')):
			#self.info['album']="Unknown album"
			self.info['album']=""
		if not(self.info.has_key('title')):
			self.info['title']="Unknown title"
		if not(self.info.has_key('artist')):
			#self.info['artist']="Unknown artist"
			self.info['artist']=""
		return
	#------	End of initInfo()
		
	def printWebUI(self,outputFile,clementine_driver,backend):
		#print clementine_driver.GetTrackNum()
		self.clementine = clementine_driver
		self.backend = backend
		
		outputFile.write(self.PrintHeader())
		outputFile.write(self.PrintInfo())
		outputFile.write(self.PrintCover())
		outputFile.write(self.PrintControls())
		outputFile.write(self.PrintTracklist())
		outputFile.write(self.PrintPlaylistManipulator())
		outputFile.write(self.PrintFooter())
	#------	End of printWebUI()
    
	def PrintHeader(self):
		return "\
		<?xml version='1.0' encoding='UTF-8'?>\
		<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML Basic 1.1//EN\"\
		\"http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd\">\
		<html>\n\
		<head>\n\
			<meta charset='utf-8'>\
			<meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1'>\n\
			<link rel='stylesheet' href='style.css' type='text/css' media='screen' />\n\
			<title>" + self.info['artist'].encode('utf-8') + " - " + self.info['title'].encode('utf-8') + " - Clementine Web Remote</title>\n\
			<script type='text/javascript'>\n\
				var cur='';\
				function loadXMLDoc(firstRun)\n\
					{ \n\
					if (window.XMLHttpRequest)\n\
						{// code for IE7+, Firefox, Chrome, Opera, Safari \n\
						xmlhttp=new XMLHttpRequest();\n\
						}\n\
					else\n\
						{// code for IE6, IE5\n\
						xmlhttp=new ActiveXObject('Microsoft.XMLHTTP');\n\
						}\n\
					xmlhttp.onreadystatechange=function()\n\
					{\n\
						if (xmlhttp.readyState==4 && xmlhttp.status==200)\n\
							{\n\
								document.getElementById('info').innerHTML=xmlhttp.responseText;\n\
								if (xmlhttp.responseText!=cur){\n\
									cur=xmlhttp.responseText;\
									//document.getElementById('cover').src=Math.random()+'aaaaaaaa.jpg'; \n\
									//document.getElementById('tracklistID').innerHTML='tracklist.html'; \n\
									//document.getElementById('tracklistID').src='tracklist.html'; \n\
									if (firstRun != 'true'){\n\
										window.location.href='/';\n\
									}\n\
								}\
							}\n\
					}\n\
					xmlhttp.open('GET','refresh',true);\n\
					xmlhttp.send();\n\
					setTimeout('loadXMLDoc(\"false\")',5000);\n\
					}\n\
			</script>\n\
		 </head>\n<body onload='loadXMLDoc(\"true\")'>"
	#------	End of PrintHeader()
  
	def PrintCover(self):
		#cover = str(self.info['arturl'])
		#cover = cover.replace('file://','')
		#return cover + "\
		#<img class='cover' src='" + str(random.random()) + ".jpg' alt='" + self.info['album'].encode('utf-8') + "'id='cover' />"
		return "\
		<img class='cover' src='" + str(random.random()) + ".jpg' alt='" + self.info['album'].encode('utf-8') + "' id='cover' />"
	#------	End of PrintCover()
    
	def PrintInfo(self):
		title = self.info['title'].encode('utf-8')
		return "\
		<div class='info' id='info'>\n\
			<span class='artist'>" + self.info['artist'].encode('utf-8') + "</span><br />\
			" + self.info['album'].encode('utf-8') + "<br />\
			" + title + "<br />\
		</div>\n"
	#------	End of PrintInfo()
    
	def PrintControls(self):
		htmlReply = "\
		<div class='info'>\n\
		<a class='cbutton' href='?action=Prev'><img src='images/prev.png' alt='Previous' /></a>\
		<a class='cbutton' href='?action=Pause'><img src='images/pause.png' alt='Pause' /></a>"
		
		if self.clementine.GetTrackNum() == -1:
			htmlReply += "<a class='cbutton' href='?action=Play'><img src='images/play.png' alt='Play' /></a>"
		else:
			htmlReply += "<a class='cbutton' href='?action=Stop'><img src='images/stop.png' alt='Stop' /></a>"
			
		htmlReply += "\
		<a class='cbutton' href='?action=Next'><img src='images/next.png' alt='Next' /></a>\
		<a class='cbutton' href='?action=VolumeDown'><img src='images/down.png' alt='VolumeDown' /></a>\
		<a class='cbutton' href='?action=VolumeUp'><img src='images/up.png' alt='VolumeUp' /></a>\
		</div>\n"
		
		
		# TODO: make repeat and shuffle prettier
		#--- Shuffle:
		htmlReply += "<span class='info'>\n"
		if self.clementine.getShuffle() == True:
			htmlReply += "<a class='tracklist' href='?action=setShuffle&value=off'>Shuffle: on</a>"
		else: 
			htmlReply += "<a class='tracklist' href='?action=setShuffle&value=on'>Shuffle: off</a>"
		
		#--- Repeat:
		htmlReply += "<br/>Repeat-mode:<br/>"
		
		emphTrackHead = ""
		emphTrackTail = ""
		emphPlaylistHead = ""
		emphPlaylistTail = ""
		emphNoneHead = ""
		emphNoneTail = ""
		
		#print "-----------------  " + self.clementine.getRepeat()
		if str(self.clementine.getRepeat()) == "Track":
			emphTrackHead = "<b><i>"
			emphTrackTail = "</i></b>"
		elif str(self.clementine.getRepeat()) == "Playlist":
			emphPlaylistHead = "<b><i>"
			emphPlaylistTail = "</i></b>"
		elif str(self.clementine.getRepeat()) == "None":
			emphNoneHead = "<b><i>"
			emphNoneTail = "</i></b>"
			
		htmlReply += emphTrackHead + "<a class='tracklist' href='?action=setRepeat&value=track'>Track<a>" + emphTrackTail
    		htmlReply += " - " + emphPlaylistHead + "<a class='tracklist' href='?action=setRepeat&value=playlist'>Playlist<a>" + emphPlaylistTail
		htmlReply += " - " + emphNoneHead + "<a class='tracklist' href='?action=setRepeat&value=none'>No Repeat<a>" + emphNoneTail
		
		htmlReply += "</span>"
		
		return htmlReply
	#------	End of PrintControls()


	def PrintFooter(self):
		return "\
		</body>\n\
		</html>\n"
	#------	End of PrintFooter()

	def PrintError(self):
		return "\
		<?xml version='1.0' encoding='UTF-8'?>\
		<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML Basic 1.1//EN\"\
		\"http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd\">\
		<html>\n\
		<head>\n\
		<meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1'>\n\
		<link rel='stylesheet' href='style.css' type='text/css' media='screen' />\n\
		<title>Not Playing - Clementine Web Remote</title>\n\
		</head>\n\
		<body>\n\
		<br/><br/>Could not connect to Clementine. Please make sure it is running and refresh this page.\n\
		</body>\n\
		</html>\n"
	#------	End of PrintError()
    
	def preprocessMetadata(self,trackMetaData):

		if not(trackMetaData.has_key('location')):
			trackMetaData['location']=""
			
		if not(trackMetaData.has_key('album')):
			trackMetaData['album']=""
			
		if not(trackMetaData.has_key('title')):
			trackMetaData['title'] = trackMetaData['location']
			if trackMetaData['title'] == "":
				trackMetaData['title'] = "Unknown title"
				
		if not(trackMetaData.has_key('artist')):
			trackMetaData['artist']=""
		else:
			trackMetaData['artist']= trackMetaData['artist'] + " - "
			
		if not(trackMetaData.has_key('time')):
			trackMetaData['time']= " - "
		else:
			minutes = int(trackMetaData['time'])//60
			seconds = int(trackMetaData['time']) - 60*minutes
			minutesStr = str(minutes).encode('utf-8')
			secondsStr = str(seconds).encode('utf-8')
			if seconds < 10:
				secondsStr = "0" + secondsStr
			trackMetaData['time']= minutesStr + ":" + secondsStr
		
		trackMetaData['title'] = (trackMetaData['title']).encode('utf-8')
		trackMetaData['artist'] = (trackMetaData['artist']).encode('utf-8')	
		trackMetaData['album'] = (trackMetaData['album']).encode('utf-8')
		trackMetaData['time'] = (trackMetaData['time']).encode('utf-8')
		trackMetaData['location'] = (trackMetaData['location']).encode('utf-8')
		
		return trackMetaData
	#------	End of preprocessMetadata()
    
    
	def PrintTracklistEntry(self,trackMetaData,thisTrack,currentlyPlayingTrack):
		#-------Track list item-----------------------------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		htmlReply = ""
		
		htmlTrackNo = str(int(thisTrack)+1)
		htmlArtistTitle = "<a href='?action=changeTrack&value=" + str(thisTrack).encode('utf-8')
		htmlArtistTitle += "' id='track" + str(thisTrack).encode('utf-8') + "'>"
		htmlArtistTitle += trackMetaData['artist'] + trackMetaData['title'] + "</a>"
		htmlTime = trackMetaData['time']
		htmlOptions = "<a href='?action=removeTrack&value=" + str(thisTrack).encode('utf-8') + "'>"
		htmlOptions += "<img src=\"images/cross_12.png\" alt=\"Remove track\" height=\"12\" width=\"12\" />" 
		htmlOptions +="</a>"
		
		#----$$$$$$$$ Emphasize currently playing track $$$$$$$$$$$$$$
		if currentlyPlayingTrack == thisTrack:
			emphHead = "<b><i><span class='currentTrack'>" 
			emphTail = "</span></i></b>"
			htmlTrackNo = emphHead + htmlTrackNo + emphTail
			htmlArtistTitle = emphHead + htmlArtistTitle + emphTail
			htmlTime = emphHead + htmlTime + emphTail
			htmlOptions = emphHead + htmlOptions + emphTail	
		
		
		htmlReply += "<tr>"		
		
		htmlReply += "<td class='tracklistTrackNo'>"
		htmlReply += htmlTrackNo
		htmlReply += "</td>"
		
		htmlReply += "<td class='tracklistArtistTitle'>"
		htmlReply += htmlArtistTitle
		htmlReply += "</td>"
		
		htmlReply += "<td class='tracklistTime'>"
		htmlReply += htmlTime
		htmlReply += "</td>"
		
		htmlReply += "<td class='tracklistOptions'>"
		htmlReply += htmlOptions
		htmlReply += "</td>"
		
		htmlReply += "</tr>"
		
		
		return htmlReply
	#------	End of PrintTracklistEntry()
		
		
	def PrintTracklist(self):
		#clementine = self.clementine
		#return "<p>Total track number: DUMMY</p>\n"
		#return "<p>Total track number: " + str(clementine.GetListLength()).encode('utf-8') + "</p>\n"
		listLength = int(self.clementine.GetListLength())
		currentTrack = int(self.clementine.GetTrackNum())
		htmlReply = ""
		htmlReply = "<p><a class='tracklist' href='#track" + str(max(currentTrack-10,0)).encode('utf-8') + "'>Jump to current track</a></p>"
		htmlReply += "<div class='outerTracklistDiv' id='tracklistID'>"
		htmlReply += "<span class='tracklist'>\n\n"
		
		#--------------Tracklist-----------------------------------------------------------------------------------------
		#htmlReply += "<div class='container'>"
		htmlReply += "<table class='tracklistTable'>"
		for x in range(0,listLength):
			trackMetaData = self.preprocessMetadata(self.clementine.GetTrackData(x))
			htmlReply = htmlReply + self.PrintTracklistEntry(trackMetaData,x,currentTrack)
			
		htmlReply += "</table>"
		#htmlReply += "</div>"
		htmlReply += "</span>"
		htmlReply += "</div>\n"
		#-------------------------------------------------------------------------------------------------------

		return htmlReply
	#------	End of PrintTracklist()

		
	def PrintPlaylistManipulator(self):
		playlistDirectory = self.backend.playlistDirectory
		
		htmlReply = ""
		#htmlReply += "<div class='outerTracklistDiv'>"
		htmlReply += "<span class='tracklist' id='playlistManipulator'>\n"
		htmlReply += "<div class='playlistManipulatorOuter'>"
		htmlReply += "<br/><h2>Playlists</h2>"
		
		#htmlReply = htmlReply + "<div class='playlistManipulatorOuter'>"
		#-----------Add playlist--------------------------------------------------------------------------------
		htmlReply += "<div class='playlistManipulatorInnerRight'>"
		htmlReply += "\n<p>---- Append playlist: ----<br/>" 
		for filename in os.listdir(playlistDirectory):
			if filename.endswith(".m3u"):
				htmlReply += "<a href='?action=addTrackList&value=" + str(filename).encode('utf-8') + "'>"
				htmlReply += str(filename).encode('utf-8')
				htmlReply += "</a><br/>"
		htmlReply += "</p></div>"
		#-------------------------------------------------------------------------------------------------------


		#-----------Replace playlist----------------------------------------------------------------------------
		htmlReply +="<div class='playlistManipulatorInnerLeft'>"
		htmlReply += "\n<p>---- Replace playlist: ----<br/>" 
		for filename in os.listdir(playlistDirectory):
			if filename.endswith(".m3u"):
				htmlReply +="<a href='?action=replaceTrackList&value=" + str(filename).encode('utf-8') + "'>"
				htmlReply += str(filename).encode('utf-8')
				htmlReply += "</a><br/>"
		htmlReply += "</p></div>"
		#--------------------------------------------------------------------------------------------------------

		htmlReply += "<div class='playlistManipulatorInnerBottom'>"
		#-----------Clear playlist-------------------------------------------------------------------------------
		htmlReply += "<span class='generalURL'>"
		htmlReply += "<a href='?action=clearTrackList'>Clear Tracklist</a><br/><br/>"
		htmlReply += "</span>"
		#--------------------------------------------------------------------------------------------------------
		
		
		#------------Save playlist--------------------------------------------------------------------------------
		htmlReply = htmlReply +  "<form name='input' action='#playlistManipulator' method='get'>\
						<input type='hidden' name='action' value='saveTrackList' />\
						Save playlist as:<br/> <input type='text' name='value' />\
						<input type='submit' value='Save' />\
						</form>"
		
		if self.backend.saveResult == "Fail":
			if self.backend.invalidFilename:
				htmlReply += "Could not save playlist, " + self.backend.playlistFilename
				htmlReply += " contains invalid characters."
			else:
				htmlReply += "Could not save playlist, name already exists.<br/>Enter a new name or override<br/>"
				htmlReply += "<a href='?action=forceSavePlaylist&value=" + self.backend.playlistFilename 
				htmlReply += "#playlistManipulator'><i>Overwrite " + self.backend.playlistFilename  + "</i></a>"
		if self.backend.saveResult == "Success":
			htmlReply += "Playlist successfully saved as " + self.backend.playlistFilename  
		#----------------------------------------------------------------------------------------------------------
		htmlReply += "</div>" # end of playlistManipulatorInnerBottom
		htmlReply += "</div>" # end of playlistManipulatorOuter
		
		htmlReply += "</span>"
		#htmlReply += "</div>\n"
		htmlReply += "<br/>"
		return htmlReply
	#------	End of PrintPlaylistManipulator()
		
	# TODO: fix / change AJAX beahavior and remove PrintInfo2
	def PrintInfo2(self,clementine_driver):
		self.clementine = clementine_driver
		return self.PrintTracklist()
	#------	End of PrintInfo2()
	
	
	
	