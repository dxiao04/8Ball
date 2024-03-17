#include <math.h>
#include <stdlib.h>
#include <string.h>
// ball info
#define PHYLIB_BALL_RADIUS (28.5) // mm
#define PHYLIB_BALL_DIAMETER (2*PHYLIB_BALL_RADIUS)

// table info
#define PHYLIB_HOLE_RADIUS (2*PHYLIB_BALL_DIAMETER)
#define PHYLIB_TABLE_LENGTH (2700.0) // mm
#define PHYLIB_TABLE_WIDTH (PHYLIB_TABLE_LENGTH/2.0) // mm

// physics info
#define PHYLIB_SIM_RATE (0.0001) // s
#define PHYLIB_VEL_EPSILON (0.01) // mm/s
#define PHYLIB_DRAG (150.0) // mm/s^2
#define PHYLIB_MAX_TIME (600) // s
#define PHYLIB_MAX_OBJECTS (26)

#define SAME_SIGN(num1, num2) (num1 >= 0) == (num2 >= 0)

/////////////////////////////////////////////////////

// polymorphic object types ?
typedef enum {
    PHYLIB_STILL_BALL = 0,
    PHYLIB_ROLLING_BALL = 1,
    PHYLIB_HOLE = 2,
    PHYLIB_HCUSHION = 3,
    PHYLIB_VCUSHION = 4,
} phylib_obj;

// vector
typedef struct {
    double x;
    double y;
} phylib_coord;

// still ball (cue ball number is 0)
typedef struct {
    unsigned char number;
    phylib_coord pos;
} phylib_still_ball;

// rolling ball
typedef struct {
    unsigned char number;
    phylib_coord pos;
    phylib_coord vel;
    phylib_coord acc;
} phylib_rolling_ball;

// hole
typedef struct {
    phylib_coord pos;
} phylib_hole;

// horizontal cushion (on the short sides of the table)
typedef struct {
    double y;
} phylib_hcushion;

// vertical cushion
typedef struct {
    double x;
} phylib_vcushion;

// union to store any of the above structs in one space (but only one can contain a value at a time)
typedef union {
    phylib_still_ball still_ball;
    phylib_rolling_ball rolling_ball;
    phylib_hole hole;
    phylib_hcushion hcushion;
    phylib_vcushion vcushion;
} phylib_untyped;

// the union can store any of the above structs but can't identify what class it is. this struct is for that
typedef struct {
    phylib_obj type; // enum indicating the class of the object
    phylib_untyped obj; // object itself
} phylib_object; // used to represent a generic object in billiards

typedef struct {
    double time;
    phylib_object *object[PHYLIB_MAX_OBJECTS]; // array of objects ?
} phylib_table;

/////////////////////////////////////////////////////

phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos );
    /* alllocate memory for a phylib_object, set its type to still ball, and 
    set its info as the given parameters. returns a pointer to the object .
    if malloc fails, return null before trying and failing to set info */

phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, 
phylib_coord *vel, phylib_coord *acc );

phylib_object *phylib_new_hole( phylib_coord *pos );

phylib_object *phylib_new_hcushion( double y );

phylib_object *phylib_new_vcushion( double x );

phylib_table *phylib_new_table( void );
    /* allocate memory for a table, returning null if it fails.
    table time is set to 0.0. assign values of its array 
    elements to the pointers created by the above functions.
    in this order: hcushions at y = 0.0, y = PHYLIB_TABLE_LENGTH,
    vcushions at x = 0.0, x=PHYLIB_TABLE_WIDTH. 
    6 holes: corners where cushions meet and 2 more
    between top and bottom holes. remaining pointers are null*/

/////////////////////////////////////////////////////

 void phylib_copy_object( phylib_object **dest, phylib_object **src );
    /* allocate memory for a phylib_object. save the address of it 
    at the location pointed to by dest. copy over the contents of the
    object at src. use memcpy. if src points at a null pointer, dest 
    will also be assigned the value of null */

phylib_table *phylib_copy_table( phylib_table *table );
    /* allocate memory for a new phylib_table, retuning
    null if the malloc fails. the contents pointed to by 
    table will be copied to the new location and the address returned */

void phylib_add_object( phylib_table *table, phylib_object *object );
    /* iterate over the object array in phylib_table until 
    it finds a null pointer. assign that pointer to the address
    of object. if there are no null pointers in the array, do nothing */

void phylib_free_table( phylib_table *table );
    /* free every non null pointer in the object array of table.
    then it should free table */

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 );
    /* return the difference between c1 and c2. i.e.
    the result's x = c1.x - c2.x and similarly for y */

double phylib_length( phylib_coord c );
    /* return the length of the vector/coord c.
    use the pythagorean theorem. don't use exp */

double phylib_dot_product( phylib_coord a, phylib_coord b );
    /* return dot product of a and b. the sum of the 
    product of x values and product of y values */

double phylib_distance( phylib_object *obj1, phylib_object *obj2 );
    /* calculate distance between obj1 and obj2. obj1 must
    be a rolling ball. return -1.0 otherwise. ....... see the doc */

/////////////////////////////////////////////////////

void phylib_roll( phylib_object *new, phylib_object *old, double time );

unsigned char phylib_stopped( phylib_object *object );

void phylib_bounce( phylib_object **a, phylib_object **b );

unsigned char phylib_rolling( phylib_table *t );

phylib_table *phylib_segment( phylib_table *table );

/////////////////////////////////////////////////////

// ASSIGNMENT 2

char *phylib_object_string( phylib_object *object );
