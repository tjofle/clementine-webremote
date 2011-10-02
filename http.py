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
import clementine as Clementine
import web as Web

class RequestHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET (self):
        self.clementine = Clementine.Clementine()
        web = None
        web = Web.Web(self.clementine.GetInfo())
        if self.path.endswith("refresh"):
        
          self.send_response(200)
          self.send_header("Content-type", "text/html")
          self.end_headers()
          self.wfile.write(web.PrintInfo())
          return
              
        else:
            if self.path.endswith(".png"):
                self.show_button()
            if self.path.endswith(".jpg"):
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
              self.check_function()
              self.end_headers()
              if self.clementine.GetTrackNum() == -1:
		print   "Clementine is stopped"
		self.wfile.write(web.PrintStopped())
	      else:
		print self.clementine.GetTrackNum()
		self.wfile.write(web.PrintHeader())
		self.wfile.write(web.PrintInfo())
		self.wfile.write(web.PrintCover())
		self.wfile.write(web.PrintControls())
		self.wfile.write(web.PrintFooter())
            return
    
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
    
    def check_function (self):
        path = self.path
        cmd = None
        if '?' in path:
          path, tmp = path.split('?', 1)
          cmd = urlparse.parse_qs(tmp)
          if str(cmd['action']) == "['Pause']":
            self.clementine.Pause()
          elif str(cmd['action']) == "['Next']":
            self.clementine.Next()
          elif str(cmd['action']) == "['Prev']":
            self.clementine.Prev()
          elif str(cmd['action']) == "['Stop']":
            self.clementine.Stop()
          elif str(cmd['action']) == "['VolumeUp']":
            self.clementine.VolumeUp()
          elif str(cmd['action']) == "['VolumeDown']":
            self.clementine.VolumeDown()
                   
    
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
    clementine = Clementine.Clementine()
    print "Using port: " + str(port)
    httpd = BaseHTTPServer.HTTPServer(('', port), RequestHandler)
    httpd.serve_forever()
def usage ():
    print "\
    Usage: http.py [options]\n\
    -h, --help                  Display this help and exit.\n\
    -p <port>, --port <port>    Launch remote listening on the specified port.\n\n\
    Examples:\n\
    http.py -p 8080             Launch remote listening the 8080 port"

if __name__ == "__main__":
    sys.exit(main(sys.argv))
