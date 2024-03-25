import phylib;
import os;
import sqlite3;
import math; 

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;

HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;

SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

FRAME_RATE = 0.01;
# add more here

HEADER = """<link rel="stylesheet" type="text/css" href="display.css">\n
<script src="http://code.jquery.com/jquery-1.9.1.js"></script>\n
<script src='display.js'></script>\n

<div id="parent" style="position: relative;background-color:#FDEEF4">\n
<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" \
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n
<svg id="table" width="280" height="550" viewBox="-25 -25 1400 2750" \
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" \
style="padding:10%;">\n
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />\n""";
FOOTER = """</svg>\n
<svg id="myCanvas" width = "100%" height = "100%" viewBox="-25 -25 1400 2750" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" >\n
<line x1="0" y1="0" x2="0" y2="0" stroke='#FF0000' stroke-width="5" />\n
</svg>\n
</div>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "KHAKI",
    "DEEPSKYBLUE",
    "HOTPINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg(self):
        result = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, \
                                                                        self.obj.still_ball.pos.y, BALL_RADIUS, \
                                                                        BALL_COLOURS[self.obj.still_ball.number]);
        return result;

################################################################################

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;


    # add an svg method here
    def svg(self):
        result = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, \
                                                                        self.obj.rolling_ball.pos.y, BALL_RADIUS, \
                                                                        BALL_COLOURS[self.obj.rolling_ball.number]);
        return result;

################################################################################

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;


    # add an svg method here
    def svg(self):
        result = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, \
                                                                        self.obj.hole.pos.y, HOLE_RADIUS);
        return result;

################################################################################

class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion;


    # add an svg method here
    def svg(self):
        # on top ?
        if (self.obj.hcushion.y == 0):
            tempY = -25;
        # on bottom?
        elif(self.obj.hcushion.y == 2700):
            tempY = 2700;
        result = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (tempY);
        return result;

################################################################################

class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion;


    # add an svg method here
    def svg(self):
        # on left ?
        if (self.obj.vcushion.x == 0):
            tempX = -25;
        # on right?
        elif(self.obj.vcushion.x == 1350):
            tempX = 1350;
        result = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (tempX);
        return result;

################################################################################
class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retrieval support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.6f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        #print (result);
        return result;

    # add svg method here
    def svg(self):
        result = HEADER;
        for i,obj in enumerate(self):
            if (obj != None):
                result += obj.svg();
        result += FOOTER;
        return result;
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                                    Coordinate(0,0),
                                                    Coordinate(0,0),
                                                    Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                                Coordinate( ball.obj.still_ball.pos.x,
                                                                    ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;
    def cueBall(self, table):
        cb = None;
        for ball in table:
            if isinstance(ball,StillBall):
                if (ball.obj.still_ball.number == 0):
                   cb = ball;
        return cb;
    def setupTable(self, table):
        balls = [];
        
        balls.append(StillBall(1, Coordinate(675,675)));
        balls.append(StillBall(2, Coordinate(617,467)));
        balls.append(StillBall(3, Coordinate(617,573)));
        balls.append(StillBall(4, Coordinate(587, 521)));
        balls.append(StillBall(5, Coordinate(763, 521)));
        balls.append(StillBall(6, Coordinate(733, 467)));
        balls.append(StillBall(7, Coordinate(558, 467)));
        balls.append(StillBall(8, Coordinate(675, 573)));
        balls.append(StillBall(9, Coordinate(704, 624)));
        balls.append(StillBall(10, Coordinate(646, 521)));
        balls.append(StillBall(11, Coordinate(675, 467)));
        balls.append(StillBall(12, Coordinate(704, 521)));
        balls.append(StillBall(13, Coordinate(733, 573)));
        balls.append(StillBall(14, Coordinate(646, 624)));
        balls.append(StillBall(15, Coordinate(792, 467)));
        balls.append(StillBall(0, Coordinate(675, 2025)));
        for i in range (16):
            #print(balls[i]);
            table += balls[i];


        
    
    """ ============================ FOR TESTING ==================="""
    def write_svg( table_id, table ):
        os.remove("temp.txt");
        with open( "temp.txt", "a" ) as fp:
            fp.write( table.svg() );
            fp.write("NEXT FILE\n");
        

"""=========================================================================================
    ========================================================================================="""
# PART 3

class Database():
    conn = None;
    def __init__(self, reset=False):
        if (reset == True):
            if os.path.exists( 'phylib.db' ):
                os.remove( 'phylib.db' );
        self.conn = sqlite3.connect("phylib.db");
    
    def createDB(self):
        cur = self.conn.cursor();
        cur.execute("""SELECT * FROM sqlite_master
                                WHERE TYPE = 'table';""");
        tableList = cur.fetchall();
        if not(any (table[1] == 'Ball' for table in tableList)):
            cur.execute( """CREATE TABLE Ball 
                        ( BALLID    INTEGER    NOT NULL,
                        BALLNO   INTEGER    NOT NULL,
                        XPOS       FLOAT         NOT NULL,
                        YPOS       FLOAT         NOT NULL,
                        XVEL       FLOAT,
                        YVEL       FLOAT,
                        PRIMARY KEY (BALLID AUTOINCREMENT) );""" );
        if not (any (table[1] == 'TTable' for table in tableList)):
            cur.execute( """CREATE TABLE TTable 
                        ( TABLEID INTEGER    NOT NULL,
                        TIME       FLOAT        NOT NULL,
                        PRIMARY KEY (TABLEID AUTOINCREMENT) );""" );
        if not (any (table[1] == 'BallTable' for table in tableList)):
            cur.execute( """CREATE TABLE BallTable 
                        ( BALLID INTEGER    NOT NULL,
                        TABLEID INTEGER    NOT NULL,
                        FOREIGN KEY (BALLID) REFERENCES Ball,
                        FOREIGN KEY (TABLEID) REFERENCES TTable );""" );
        if not (any (table[1] == 'Shot' for table in tableList)):
            cur.execute( """CREATE TABLE Shot 
                        ( SHOTID INTEGER    NOT NULL,
                        PLAYERID INTEGER    NOT NULL,
                        GAMEID    INTEGER    NOT NULL,
                        PRIMARY KEY (SHOTID AUTOINCREMENT),
                        FOREIGN KEY (PLAYERID) REFERENCES Player,
                        FOREIGN KEY (GAMEID) REFERENCES Game );""" );
        # assume shots occur in increasing order of SHOTID
        if not (any (table[1] == 'TableShot' for table in tableList)):
            cur.execute( """CREATE TABLE TableShot 
                        ( TABLEID INTEGER    NOT NULL,
                        SHOTID    INTEGER    NOT NULL,
                        FOREIGN KEY (TABLEID) REFERENCES TTable,
                        FOREIGN KEY (SHOTID) REFERENCES Shot );""" );
        # assume TABLEIDs are in chronological order
        if not (any (table[1] == 'Game' for table in tableList)):
            cur.execute( """CREATE TABLE Game 
                        ( GAMEID     INTEGER           NOT NULL,
                        GAMENAME VARCHAR(64)    NOT NULL,
                        PRIMARY KEY (GAMEID AUTOINCREMENT) );""" );
        if not (any (table[1] == 'Player' for table in tableList)):
            cur.execute( """CREATE TABLE Player 
                        ( PLAYERID     INTEGER           NOT NULL,
                        GAMEID          INTEGER           NOT NULL,
                        PLAYERNAME  VARCHAR(64)    NOT NULL,
                        PRIMARY KEY (PLAYERID AUTOINCREMENT),
                        FOREIGN KEY (GAMEID) REFERENCES Game );""" );
        cur.close();
        self.conn.commit();

    def readTable (self, tableID):
        """create Balls whose BALLIDs are in the BallTable table with a TABLEID that
            is one larger than the method's argument"""
        retTable = Table();
        cur = self.conn.cursor();
        temp = cur.execute("""SELECT * FROM BallTable
                                                WHERE (BallTable.TABLEID = ?);""", (tableID + 1,)).fetchall();
        if (not temp):
            return None;
        cur.execute("""SELECT * FROM Ball, BallTable
                                    WHERE (Ball.BALLID = BallTable.BALLID
                                    AND BallTable.TABLEID = ?);""", (tableID + 1,));
        ballsTemp = cur.fetchall();
        for ball in ballsTemp:
            if (ball[4] == 'NULL' and ball[5] == 'NULL'):
                sb = StillBall(ball[1], Coordinate(ball[2], ball[3]));
                retTable.add_object(sb);
            else:
                velX = float(ball[4]);
                velY = float(ball[5]);
                ballLen = math.sqrt(velX * velX + velY * velY);
                accX = 0.0;
                accY = 0.0;
                if ballLen > VEL_EPSILON:
                    accX = (velX * (-1)) / ballLen * DRAG;
                    accY = (velY * (-1)) / ballLen * DRAG;
                rb = RollingBall(ball[1], Coordinate(ball[2], ball[3]), Coordinate(ball[4], ball[5]),
                                                    Coordinate(accX, accY));
                retTable.add_object(rb);
        cur.close();
        self.conn.commit();
        return retTable;

    def writeTable(self, table):
        cur = self.conn.cursor();
        cur.execute("""INSERT INTO TTable (TIME)
                                VALUES (?);""", (table.time,));
        cur.execute("""SELECT TABLEID FROM TTable;""");
        tableID = max(cur.fetchall())[0];
        for object in table:
            if isinstance( object, StillBall ):
                cur.execute("""INSERT INTO Ball
                                        VALUES (?, ?, ?, ?, ?, ?);""", (None, object.obj.still_ball.number,\
                                        object.obj.still_ball.pos.x, object.obj.still_ball.pos.y, "NULL", "NULL"));
                ballID = max(cur.execute("""SELECT BALLID FROM Ball;""").fetchall())[0];
                cur.execute("""INSERT INTO BallTable
                                        VALUES (?, ?);""", (ballID, tableID));
            if isinstance( object, RollingBall ):
                cur.execute("""INSERT INTO Ball
                                        VALUES (?, ?, ?, ?, ?, ?);""", (None, object.obj.rolling_ball.number,\
                                        object.obj.rolling_ball.pos.x, object.obj.rolling_ball.pos.y, \
                                        object.obj.rolling_ball.vel.x, object.obj.rolling_ball.vel.y));
                ballID = max(cur.execute("""SELECT BALLID FROM Ball;""").fetchall())[0];
                cur.execute("""INSERT INTO BallTable
                                        VALUES (?, ?);""", (ballID, tableID));
        self.conn.commit();

        '''data = cur.execute("""SELECT * FROM BallTable""");
        dataText = cur.fetchall();
        for column in data.description: 
            print(column[0]);
        print ('\n'.join(str(e) for e in dataText));'''

        cur.close();
        return tableID;

    def close(self):
        self.conn.commit();
        self.conn.close();
    
    def getGame (self, id):
        cur = self.conn.cursor();
        cur.execute("""SELECT * FROM Game, Player
                                WHERE (Player.GAMEID = ?
                                AND Game.GAMEID = ?);""", (id, id));
        dataText = cur.fetchall();
        self.conn.commit();
        cur.close();
        return dataText;
        
    def setGame (self, gN, p1N, p2N):
        cur = self.conn.cursor();
        cur.execute("""INSERT INTO Game
                                VALUES (?, ?);""", (None, gN));
        cur.execute("""SELECT GAMEID FROM Game;""");
        gameID = max(cur.fetchall())[0];
        cur.execute("""INSERT INTO Player
                                VALUES (?, ?, ?);""", (None, gameID, p1N));
        cur.execute("""INSERT INTO Player
                                VALUES (?, ?, ?);""", (None, gameID, p2N));          
        self.conn.commit();
        cur.close();
    
    def newShot(self, gameName, playerName):
        cur = self.conn.cursor();
        data = cur.execute("""SELECT * FROM Game, Player
                                            WHERE (Player.PLAYERNAME = ?
                                            AND Game.GAMENAME = ?);""", (playerName, gameName));
        dataText = data.fetchall();
        cur.execute("""INSERT INTO Shot
                                VALUES (?, ?, ?);""", (None, dataText[0][2], dataText[0][3]));
        cur.execute("""SELECT * FROM Shot
                                WHERE (Shot.PLAYERID = ?
                                AND Shot.GAMEID = ?);""", (dataText[0][2], dataText[0][3]));
        shotID = max(cur.fetchall())[0];
        self.conn.commit();
        cur.close();
        return shotID;

class Game():
    db = None;
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        db = Database();
        db.createDB();
        if (isinstance(gameID, int)):
            if not (gameName is None and player1Name is None and player2Name is None):
                raise TypeError;
            else:
                tempID = gameID + 1;
                table = db.getGame(tempID);
                gameName = table[0][1];
                player1Name = table[0][4];
                player2Name = table[1][4];
        elif (gameID is None):
            if not (isinstance(gameName, str) and isinstance(player1Name, str) and isinstance(player2Name, str)):
                raise TypeError;
            else:
                db.setGame(gN=gameName, p1N=player1Name, p2N=player2Name);
        else:
            raise TypeError;
        db.close();

    def shoot(self, gameName, playerName, table, xvel, yvel):
        db = Database();
        shotID = db.newShot(gameName, playerName);
        
        cb = table.cueBall(table);
        
        tempX = cb.obj.still_ball.pos.x;
        tempY = cb.obj.still_ball.pos.y;
        cb.type = phylib.PHYLIB_ROLLING_BALL;
        cb.obj.rolling_ball.pos.x = tempX;
        cb.obj.rolling_ball.pos.y = tempY;

        cb.obj.rolling_ball.vel.x = xvel;
        cb.obj.rolling_ball.vel.y = yvel;
        ballLen = math.sqrt(xvel * xvel + yvel * yvel);
        accX = 0.0;
        accY = 0.0;
        if ballLen > VEL_EPSILON:
            accX = (xvel * (-1)) / ballLen * DRAG;
            accY = (yvel * (-1)) / ballLen * DRAG;
        cb.obj.rolling_ball.acc.x = accX;
        cb.obj.rolling_ball.acc.y = accY;
        cb.obj.rolling_ball.number = 0;
        
        cur = db.conn.cursor();
        while table:
            startTime = table.time;
            temp = table.segment();
            if not temp:
                break;
            endTime = temp.time;
            seconds = math.floor((endTime - startTime)/FRAME_RATE);
            for i in range(seconds):
                frame = i * FRAME_RATE;
                tempTable = table.roll(frame);
                tempTable.time = startTime + frame;
                tableID = db.writeTable(tempTable);
                cur.execute(""" INSERT  INTO TableShot
                                        VALUES (?, ?)""",(tableID, shotID));
                db.conn.commit();
            table = table.segment();
        db.close();
