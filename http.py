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

#import urlparse
#import getopt
#import sys
import BaseHTTPServer
import clementineDriver as Clementine
import web as Web
import functionality as Functionality
#import os

class RequestHandler (BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET (self):

		self.web = None
		self.web = Web.Web()
		#web = Web.Web(self.clementine.GetInfo())
		
		#TODO: clean up code and clear up beahaviour
		#print "_____________________" + self.path +  "_____________________" 
		
		#TODO: implement ability to start Clementine from WebUI or automaticly
		#print "Trying to start Clementine"
		#os.system("clementine &")
		
		if self.path.endswith("refresh") and self.connectToClementine():
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write(self.web.PrintInfo())
			return
		elif self.path.endswith("tracklist.html") and self.connectToClementine():
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write(self.web.PrintInfo2(self.clementine))
			return
		else:
			if self.path.endswith(".png"):
				self.show_button()
			if self.path.endswith(".jpg") and self.connectToClementine():
				self.show_cover()
			elif self.path.endswith(".css"):
				f = open('style.css')
				self.send_response(200)
				self.send_header('Content-type', 'text/css')
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			else:
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
				
				if self.connectToClementine():
					backend = Functionality.Functionality(self.path,self.clementine)
					backend.run()
					self.web.printWebUI(self.wfile,self.clementine,backend)
				else:
					self.wfile.write(self.web.PrintError())
			return
	
	def connectToClementine(self):
		clementineSuccess = False
		try:
			self.clementine = Clementine.Clementine()
			self.web.initInfo(self.clementine.GetInfo())
			clementineSuccess = True
			#print "clementine sucess"
		except:
			clementineSuccess = False
			#print "clementine fail"
		return clementineSuccess
	
	def show_button (self):
		btn = str(self.path)
		btn = btn.replace('/','',1)
		f = open(btn, 'r')
		self.send_response(200)
		self.send_header('Content-type', 'image/png')
		self.end_headers()
		self.wfile.write(f.read())

	def show_cover (self):
		cover = str(self.clementine.GetInfo()['arturl'])
		cover = cover.replace('file://','')
		f = open(cover, 'r')
		self.send_response(200)
		self.send_header('Content-type', 'image/jpg')
		self.end_headers()
		self.wfile.write(f.read())
		print "SENDING ALBUMCOVER"
        
	# Override BaseHTTPRequestHandler.address_string() to avoid useless DNS lookups
	# in order to speed up non-localhost requests
	# Thanks to hokascha@gmail.com for the code snippet 
	def address_string(self):
		host, port = self.client_address[:2]
		#return socket.getfqdn(host)
		return host  
		