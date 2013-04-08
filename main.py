#!/usr/bin/env python2

import user
import termextract

import time
import BaseHTTPServer
import json
from cgi import parse_header, parse_multipart
from urlparse import parse_qs
import sys
from config import config

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length), 
                    keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("""<html><head><title>Title goes here.</title></head>
<body><form method="post">
<textarea name="data" cols="120" rows="30">
{ 
  "user": "testUser", 
  "actionGetRating": true, 
  "actionModRatings": true, 
  "modRatings": { "document": 1.0 },
  "actionDeleteUser": false, 
  "text": "Google just settled video codec patent claims with MPEG LA and its VP8 format, which it wants to be elevated to an Internet standard, already faces the next round of patent infringement allegations. Nokia submitted an IPR declaration to the Internet Engineering Task Force listing 64 issued patents and 22 pending patent applications it believes are essential to VP8. To add insult to injury, Nokia's declaration to the IETF says NO to royalty-free licensing and also NO to FRAND (fair, reasonable and non-discriminatory) licensing. Nokia reserves the right to sue over VP8 and to seek sales bans without necessarily negotiating a license deal. Two of the 86 declared IPRs are already being asserted in Mannheim, Germany, where Nokia is suing HTC in numerous patent infringement cases. A first VP8-related trial took place on March 8 and the next one is scheduled for June 14. In related Nokia-Google patent news, the Finns are trying to obtain a U.S. import ban against HTC to force it to disable tethering (or, more likely, to pay up)." 
}
</textarea><br />
<input type="submit" value="send"></form>""")
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")
    def do_POST(s):
        """Respond to a POST request."""
        postvars = s.parse_POST()
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.send_header("Cache-Control", "private, must-revalidate, max-age=0")
        s.send_header("Pragma", "no-cache")
        s.end_headers()
        if(postvars['data'][0]):
            data = json.loads(postvars['data'][0])
            if(not data):
                return
            t = user.User(data['user'])
            if(data['actionDeleteUser']):
                user.deleteUser(data['user'])
                return
            if(data['actionModRatings']):
                for i in data['modRatings'].keys():
                    t.modifyKeywordRating(i, data['modRatings'][i])
                t.saveData()
            if(data['actionGetRating']):
                kws = termextract.getKeywords(data['text'])
                data['keywords'] = kws
                data['rating'] = t.getRating(kws)
                s.wfile.write(json.dumps(data, indent=4))

if __name__ == '__main__':
    if(len(sys.argv) > 1):
        f = open(sys.argv[1], 'r')
        config.conf = json.load(f)
        f.close()
    hostname = config.conf['hostname']
    portNumber = config.conf['port']

    serverClass = BaseHTTPServer.HTTPServer
    httpd = serverClass((hostname, portNumber), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (hostname, portNumber)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (hostname, portNumber)
