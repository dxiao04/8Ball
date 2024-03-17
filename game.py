import sys;
import cgi;
from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse, parse_qsl;
import os;
import re; 
import math;
import Physics;

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
            currentDir = os.getcwd();
            tablePattern = re.compile(r"\/table-\d+.svg");
            content = "";
            for file in os.listdir(currentDir):
                if tablePattern.match("/" + file):
                    #print("removing " + os.path.join(currentDir, file));
                    os.remove(os.path.join(currentDir, file));
            
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
                gameName = form_data["game_name"].value;
                p1N = form_data["p1_name"].value;
                p2N = form_data["p2_name"].value;

                game = Physics.Game(gameName=gameName, player1Name=p1N, player2Name=p2N);

                accX = 0;
                accY = 0;
                if ballLen > Physics.VEL_EPSILON:
                    accX = (velX * (-1)) / ballLen * Physics.DRAG;
                    accY = (velY * (-1)) / ballLen * Physics.DRAG;
                table = Physics.Table();
                sbPos = Physics.Coordinate((float(form_data["sb_x"].value)), (float(form_data["sb_y"].value)));
                sb = Physics.StillBall((int(form_data["sb_number"].value)), sbPos);
                rbPos = Physics.Coordinate((float(form_data["rb_x"].value)), (float(form_data["rb_y"].value)));
                vel = Physics.Coordinate(velX, velY);
                acc = Physics.Coordinate(accX, accY);
                rb = Physics.RollingBall((int(form_data["rb_number"].value)), rbPos, vel, acc);
                table.add_object(sb);
                table.add_object(rb);
                i = 0;
                while(table): # writes tables
                    if (table != None):
                        f = open("table-%d.svg" %i, 'w');
                        f.write(table.svg());
                        f.close();
                    new_table = table.segment();
                    table = new_table;
                    i += 1;
                
                # makes the page look nice
                content += "<body style=""background-color:floralwhite;font-family:cursive;color:tomato;text-align:center"">\n\
                                <div style=""background-color:palegoldenrod;width:max-content;display:inline-block;margin:0 auto;"">\n\
                                <h3>original positions and velocities:</h3>";
                content += "<h4 style=""font-family:monospace"">still ball position: (%s, %s)<br> \n" % (form_data["sb_x"].value, form_data["sb_y"].value);
                content += "rolling ball position: (%s, %s)<br>\n " % (form_data["rb_x"].value, form_data["rb_y"].value);
                content += "rolling ball velX: %s velY: %s</h4>\n " % (form_data["rb_dx"].value, form_data["rb_dy"].value);
                content += "<a href = ""shoot.html"" style = ""color:tomato;""> go back </a></div><br>\n";
                i = 0;
                content += "<div style = ""display:inline-block"">"
                for img in os.listdir(currentDir): # displays tables in order
                    if tablePattern.match("/" + img):
                        content += "<img src = ""table-%s.svg"" style = ""padding:5px;height:55%%""><br>\n" % i;
                        i += 1;
                content += "<a href = ""shoot.html"" style = ""color:tomato;""> go back </a><br>\n";
                content += "</div>"
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
            self.wfile.write( bytes( content, "utf-8" ) );
        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );
if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();