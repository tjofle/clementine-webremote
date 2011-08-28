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
      <!--<title>" + self.info['artist'].encode('utf-8') + " - " + self.info['title'].encode('utf-8') + "</title>\n\-->\
      <title>Clementine Remote Control</title>\n\
      <script type='text/javascript'>\n\
			var cur='';\
			function loadXMLDoc()\n\
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
				    document.getElementById('cover').src=Math.random()+'.jpg'; \
				}\
				}\n\
			  }\n\
			xmlhttp.open('GET','refresh',true);\n\
			xmlhttp.send();\n\
			setTimeout('loadXMLDoc()',1000);\n\
			}\n\
		 </script>\n\
		 </head>\n<body onload='loadXMLDoc()'>"
  
  def PrintCover(self):
    cover = str(self.info['arturl'])
    cover = cover.replace('file://','')
    return "\
    <img class='cover' src='" + str(random.random()) + ".jpg' alt='" + self.info['album'].encode('utf-8') + "'id='cover' />"
    
  def PrintInfo(self):
    
    if not(self.info.has_key('album')):
        self.info['album']="unknown album"
    if not(self.info.has_key('title')):
        self.info['title']="unknown title"
    if not(self.info.has_key('artist')):
        self.info['artist']="unknown artist"

    title = self.info['title'].encode('utf-8')
    return "\
    <div class='info' id='info'>\n\
      <span class='artist'>" + self.info['artist'].encode('utf-8') + "</span><br />\
      " + self.info['album'].encode('utf-8') + "<br />\
      " + title + "<br />\
    </div>\n"
    
  def PrintControls(self):
    return "\
    <div class='info'>\n\
        <a class='cbutton' href='?action=Prev'><img src='images/prev.png' alt='Previous' /></a>\
        <a class='cbutton' href='?action=Pause'><img src='images/pause.png' alt='Pause' /></a>\
        <a class='cbutton' href='?action=Stop'><img src='images/stop.png' alt='Stop' /></a>\
        <a class='cbutton' href='?action=Next'><img src='images/next.png' alt='Next' /></a>\
        <a class='cbutton' href='?action=VolumeDown'><img src='images/down.png' alt='VolumeDown' /></a>\
        <a class='cbutton' href='?action=VolumeUp'><img src='images/up.png' alt='VolumeUp' /></a>\
        </div>\n"
    
  def PrintFooter(self):
    return "\
    </body>\n\
</html>\n"
