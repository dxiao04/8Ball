import sys;
import cgi;
from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse, parse_qsl;
import os;
import re; 
import math;
import json;
import Physics;
game = None;
gameName = "";
p1N = "";
p2N = "";
table = None;

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path);
        if parsed.path in ["/shoot.html"]:
            fp = open( '.'+self.path );
            content = fp.read();
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
        elif parsed.path in ["/shoot.css"]:
            fp = open( '.'+self.path );
            content = fp.read();
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/css" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
        elif parsed.path in ["/display.css"]:
            fp = open( '.'+self.path );
            content = fp.read();
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/css" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
        elif parsed.path in ["/display.js"]:
            fp = open( '.'+self.path );
            content = fp.read();
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/javascript" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );   

    def do_POST(self):
        parsed = urlparse(self.path);
        if parsed.path in ["/display.html"]:
            form_data = cgi.FieldStorage( fp=self.rfile,
                                          headers=self.headers,
                                          environ = { 'REQUEST_METHOD': 'POST',
                                                      'CONTENT_TYPE': 
                                                      self.headers['Content-Type'],
                                                    } 
                                        );
            
            content = "";
            
            # checks for invalid values
            if (len(form_data) < 3):
                content +=  "<h4 style=""font-family:monospace"">one or more fields are empty<br> \n";
                content += "<a href = ""shoot.html"" style = ""color:tomato;""> go back </a></h4><br>\n";
            elif (len(form_data["game_name"].value) > 64):
                content +=  "<h4 style=""font-family:monospace"">game name must be less than 64 characters<br> \n";
                content += "<a href = ""shoot.html"" style = ""color:tomato;""> go back </a></h4><br>\n";
            elif (len(form_data["p1_name"].value) > 64 or len(form_data["p2_name"].value) > 64):
                content +=  "<h4 style=""font-family:monospace"">player names must be less than 64 characters<br> \n";
                content += "<a href = ""shoot.html"" style = ""color:tomato;""> go back </a></h4><br>\n";
            else: # makes the game
                global gameName
                gameName = form_data["game_name"].value;
                global p1N 
                p1N= form_data["p1_name"].value;
                global p2N 
                p2N = form_data["p2_name"].value;

                global game
                game = Physics.Game(gameName=gameName, player1Name=p1N, player2Name=p2N);

                global table
                table = Physics.Table();
                table.setupTable(table);
                f = open("table.svg", 'w');
                f.write(table.svg());
                f.close();
                f = open("table.svg", 'r');
                content = """<link rel="stylesheet" type="text/css" href="display.css">\n
<script src="http://code.jquery.com/jquery-1.9.1.js"></script>\n
<script src='display.js'></script>\n
<div id="parent" style="position: relative;background-color:#FDEEF4">\n
<div id = "playerinfo">
<div class="column" id = "player1">
<p id = "p1N">""" + p1N +"""</p>
<p id = "p1S">
  7 ball(s) left
</p>
</div>
<div class="column" id = "player2">
<p id = "p2N">""" + p2N +"""</p>
<p id = "p2S">
  7 ball(s) left
</p>
</div>
</div>
<div id = "inner">

<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" \
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n""";
                content += f.read();
                content += """</div> <svg id="myCanvas" width = "100%" height = "100%" viewBox="-25 -25 1400 2750" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" >\n
<line x1="0" y1="0" x2="0" y2="0" stroke='#FF0000' stroke-width="5" />\n
</svg>\n
</div>\n"""
                f.close();
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();
            self.wfile.write( bytes( content, "utf-8" ) );
        elif parsed.path in ["/post"]:
            form_data = cgi.FieldStorage(
                                fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST'})
            xVel = float(form_data.getvalue('xVel'));
            yVel = float(form_data.getvalue('yVel'));
            #print(xVel, yVel);
            arr, table, existingBalls= game.shoot(gameName = gameName, playerName= p1N, table = table, xvel = xVel, yvel = yVel);
            
            existingArr = "#".join(str(x) for x in existingBalls);
            #print(existingArr);
            strArr = ''.join(str(x) for x in arr);
            strArr += ",";
            strArr += existingArr;

            #print(strArr)
            self.send_response( 200 );
            self.send_header('Content-Type', 'text/html')
            self.send_header( "Content-length", len( strArr ) );
            self.end_headers()
            self.wfile.write( bytes( strArr, "utf-8" ))
            #print(jsonStr);
            print("done");
        elif parsed.path in ["/respawn"]:
            respawnSVG = table.respawn();
            self.send_response( 200 );
            self.send_header('Content-Type', 'text/html')
            self.send_header( "Content-length", len( respawnSVG ) );
            self.end_headers()
            self.wfile.write( bytes( respawnSVG, "utf-8" ))
            #print(respawnSVG);
            print("respawned");
        elif parsed.path in ["/loser"]:
            form_data = cgi.FieldStorage( fp=self.rfile,
                                          headers=self.headers,
                                          environ = { 'REQUEST_METHOD': 'POST',
                                                      'CONTENT_TYPE': 
                                                      self.headers['Content-Type'],
                                                    } 
                                        );
            content = """
<body style = "background-color: red">
<div style= "text-align: center;color:white">
<h1 >""" + form_data.getvalue("loserPlayer") + """<br>LOST BY ILLEGALLY POTTING THE CUE BALL<br><br><br><br><br>

</h1>
<h2>
<a href = "shoot.html" style="color:white"> new game </a><br>
</h2>
</div>

</body>"""
            self.send_response( 200 );
            self.send_header('Content-Type', 'text/html')
            self.send_header( "Content-length", len( content ) );
            self.end_headers()
            self.wfile.write( bytes( content, "utf-8" ))

        elif parsed.path in ["/winner"]:
            form_data = cgi.FieldStorage( fp=self.rfile,
                                          headers=self.headers,
                                          environ = { 'REQUEST_METHOD': 'POST',
                                                      'CONTENT_TYPE': 
                                                      self.headers['Content-Type'],
                                                    } 
                                        );
            content = """
<body style = "background-color: green">
<div style= "text-align: center;color:white">
<h1 >""" + form_data.getvalue("winnerPlayer") + """<br>WON BY LEGALLY POTTING THE CUE BALL<br><br><br><br><br>

</h1>
<h2>
<a href = "shoot.html" style="color:white"> new game </a><br>
</h2>
</div>

</body>"""
            self.send_response( 200 );
            self.send_header('Content-Type', 'text/html')
            self.send_header( "Content-length", len( content ) );
            self.end_headers()
            self.wfile.write( bytes( content, "utf-8" ))
            
        
if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();