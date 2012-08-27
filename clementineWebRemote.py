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

import urlparse
import getopt
import sys
import BaseHTTPServer
from http import RequestHandler 
import os
import config

def main (argv):
	port = 3000
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:d", ["help", "port"])
	except getopt.GetoptError:
		usage()
		sys.exit()
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-p", "--port"):
			try:
				port = int(arg)
			except ValueError:
				print   "Incorrect port, launching at 3000."
	#clementine = Clementine.Clementine()
	print "Using port: " + str(port)
	
	ensure_dir(config.playlistDirectory)
	# TODO: Run ensure_dir here and run only once to reduce computing load?
	# TODO: Run ensure_dir for every clementine access to ensure it still exsists?
	
	
	httpd = BaseHTTPServer.HTTPServer(('', port), RequestHandler)
	httpd.serve_forever()
    
def usage ():
	print "\
	Usage: clementineWebRemote.py [options]\n\
	-h, --help                  Display this help and exit.\n\
	-p <port>, --port <port>    Launch remote listening on the specified port.\n\n\
	Examples:\n\
	http.py -p 8080             Launch remote listening the 8080 port"
	
def ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)

if __name__ == "__main__":
	sys.exit(main(sys.argv))
