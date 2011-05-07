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

class Web:
  def __init__(self, info):
    self.info = info
    return
    
  def PrintHeader(self):
    return "\
    <?xml version='1.0' encoding='UTF-8'?>\
    <!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML Basic 1.1//EN\"\
    \"http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd\">\
    <html>\n\
    <head>\n\
      <meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1'>\n\
      <link rel='stylesheet' href='style.css' type='text/css' media='screen' />\n\
      <title>" + self.info['artist'] + " - " + self.info['title'] + "</title>\n\
    </head>\n<body>"
  
  def PrintCover(self):
    cover = str(self.info['arturl'])
    cover = cover.replace('file://','')
    return "\
    <img class='cover' src='" + str(random.random()) + ".jpg' alt='" + self.info['album'] + "' />"
    
  def PrintInfo(self):
    title = self.info['title']

    return "\
    <div class='info'>\n\
      <span class='artist'>" + self.info['artist'] + "</span><br />\
      " + self.info['album'] + "<br />\
      " + title + "<br />\
    </div>\n"
    
  def PrintControls(self):
    return "\
    <div class='info'>\n\
        <a class='cbutton' href='?action=Prev'><img src='images/prev.png' alt='Previous' /></a>\
        <a class='cbutton' href='?action=Pause'><img src='images/pause.png' alt='Pause' /></a>\
        <a class='cbutton' href='?action=Stop'><img src='images/stop.png' alt='Stop' /></a>\
        <a class='cbutton' href='?action=Next'><img src='images/next.png' alt='Next' /></a>\
    </div>\n"
    
  def PrintFooter(self):
    return "\
    </body>\n\
</html>\n"
