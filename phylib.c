#include "phylib.h"

#include <stdio.h>

phylib_object * phylib_new_still_ball(unsigned char number, phylib_coord * pos) {
    phylib_object * newObj;
    newObj = (phylib_object * ) malloc(sizeof(phylib_object));
    if (newObj == NULL) {
        return NULL;
    }
    newObj -> type = PHYLIB_STILL_BALL;
    newObj -> obj.rolling_ball.acc.x = 0.0;
    newObj -> obj.rolling_ball.acc.y = 0.0;
    newObj -> obj.rolling_ball.vel.x = 0.0;
    newObj -> obj.rolling_ball.vel.y = 0.0;
    newObj -> obj.still_ball.number = number;
    newObj -> obj.still_ball.pos.x = pos -> x;
    newObj -> obj.still_ball.pos.y = pos -> y;
    return newObj;
}
/* alllocate memory for a phylib_object, set its type to still ball, and 
set its info as the given parameters. returns a pointer to the object .
if malloc fails, return null before trying and failing to set info */

phylib_object * phylib_new_rolling_ball(unsigned char number, phylib_coord * pos,
    phylib_coord * vel, phylib_coord * acc) {
    phylib_object * newObj;
    newObj = (phylib_object * ) malloc(sizeof(phylib_object));
    if (newObj == NULL) {
        return NULL;
    }
    newObj -> type = PHYLIB_ROLLING_BALL;

    newObj -> obj.rolling_ball.number = number;
    newObj -> obj.rolling_ball.pos.x = pos -> x;
    newObj -> obj.rolling_ball.pos.y = pos -> y;
    newObj -> obj.rolling_ball.vel.x = vel -> x;
    newObj -> obj.rolling_ball.vel.y = vel -> y;
    newObj -> obj.rolling_ball.acc.x = acc -> x;
    newObj -> obj.rolling_ball.acc.y = acc -> y;
    return newObj;
}

phylib_object * phylib_new_hole(phylib_coord * pos) {
    phylib_object * newObj;
    newObj = (phylib_object * ) malloc(sizeof(phylib_object));
    if (newObj == NULL) {
        return NULL;
    }
    newObj -> type = PHYLIB_HOLE;

    double x = 0.0;
    double y = 0.0;
    x = pos -> x;
    y = pos -> y;
    newObj -> obj.hole.pos.x = x;
    newObj -> obj.hole.pos.y = y;
    return newObj;
}
// same as above but for rolling ball

phylib_object * phylib_new_hcushion(double y) {
    phylib_object * newObj;
    newObj = (phylib_object * ) malloc(sizeof(phylib_object));
    if (newObj == NULL) {
        return NULL;
    }
    newObj -> type = PHYLIB_HCUSHION;

    newObj -> obj.hcushion.y = y;
    return newObj;
}
// same as above but for hcushion

phylib_object * phylib_new_vcushion(double x) {
    phylib_object * newObj;
    newObj = (phylib_object * ) malloc(sizeof(phylib_object));
    if (newObj == NULL) {
        return NULL;
    }
    newObj -> type = PHYLIB_VCUSHION;

    newObj -> obj.vcushion.x = x;
    return newObj;
}
// same as above but for vcushion

phylib_table * phylib_new_table(void) {
    phylib_table * newTable;
    newTable = (phylib_table * ) malloc(sizeof(phylib_table));
    if (newTable == NULL) {
        return NULL;
    }

    newTable -> time = 0.0;
    newTable -> object[0] = phylib_new_hcushion(0.0);
    newTable -> object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    newTable -> object[2] = phylib_new_vcushion(0.0);
    newTable -> object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    // holes 
    phylib_coord tempCoord;
    tempCoord.x = 0.0;
    tempCoord.y = 0.0;
    newTable -> object[4] = phylib_new_hole( & tempCoord);
    tempCoord.x = 0.0;
    tempCoord.y = PHYLIB_TABLE_LENGTH / 2;
    newTable -> object[5] = phylib_new_hole( & tempCoord);
    tempCoord.x = 0.0;
    tempCoord.y = PHYLIB_TABLE_LENGTH;
    newTable -> object[6] = phylib_new_hole( & tempCoord);
    tempCoord.x = PHYLIB_TABLE_LENGTH / 2;
    tempCoord.y = 0.0;
    newTable -> object[7] = phylib_new_hole( & tempCoord);
    tempCoord.x = PHYLIB_TABLE_WIDTH;
    tempCoord.y = PHYLIB_TABLE_LENGTH / 2;
    newTable -> object[8] = phylib_new_hole( & tempCoord);
    tempCoord.x = PHYLIB_TABLE_WIDTH;
    tempCoord.y = PHYLIB_TABLE_LENGTH;
    newTable -> object[9] = phylib_new_hole( & tempCoord);

    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
        newTable -> object[i] = NULL;
    }
    return newTable;
}
/* allocate memory for a table, returning null if it fails.
table time is set to 0.0. assign values of its array 
elements to the pointers created by the above functions.
in this order: hcushions at y = 0.0, y = PHYLIB_TABLE_LENGTH,
vcushions at x = 0.0, x=PHYLIB_TABLE_WIDTH. 
6 holes: corners where cushions meet and 2 more
between top and bottom holes. remaining pointers are null*/

/////////////////////////////////////////////////////

void phylib_copy_object(phylib_object ** dest, phylib_object ** src) {
    if ( * src == NULL) {
        * dest = NULL;
        return;
    }
    phylib_object * newObj = (phylib_object * ) malloc(sizeof(phylib_object));
    * dest = newObj;
    memcpy( * dest, * src, sizeof(phylib_object));
}
/* allocate memory for a phylib_object. save the address of it 
at the location pointed to by dest. copy over the contents of the
object at src. use memcpy. if src points at a null pointer, dest 
will also be assigned the value of null */

phylib_table * phylib_copy_table(phylib_table * table) {
    if (table == NULL) {
        return NULL;
    }
    phylib_table * dest = (phylib_table * ) malloc(sizeof(phylib_table));
    if (dest == NULL) {
        return NULL;
    }
    dest -> time = table -> time;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        phylib_copy_object( & (dest -> object[i]), & (table -> object[i]));
    }
    return dest;
}
/* allocate memory for a new phylib_table, returning
null if the malloc fails. the contents pointed to by 
table will be copied to the new location and the address returned */

void phylib_add_object(phylib_table * table, phylib_object * object) {
    if (table != NULL && object != NULL){
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table -> object[i] == NULL) {
            table -> object[i] = object;
            return;
        }
    }
    }
}
/* iterate over the object array in phylib_table until 
it finds a null pointer. assign that pointer to the address
of object. if there are no null pointers in the array, do nothing */

void phylib_free_table(phylib_table * table) {
    if (table != NULL){
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table -> object[i] != NULL) {
            free(table -> object[i]);
            table -> object[i] = NULL;
        }
    }
    free(table);
    }
}
/* free every non null pointer in the object array of table.
then it should free table */

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {
    phylib_coord result;
    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;
    return result;
}
/* return the difference between c1 and c2. i.e.
the result's x = c1.x - c2.x and similarly for y */

double phylib_length(phylib_coord c) {
    double hyp = 0.0;
    hyp = sqrt((c.x * c.x) + (c.y * c.y));
    return hyp;
}
/* return the length of the vector/coord c.
use the pythagorean theorem. don't use exp */

double phylib_dot_product(phylib_coord a, phylib_coord b) {
    double dotP = (a.x * b.x) + (a.y * b.y);
    return dotP;
}
/* return dot product of a and b. the sum of the 
product of x values and product of y values */

double phylib_distance(phylib_object * obj1, phylib_object * obj2) {

    if (obj1 == NULL || obj1 -> type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }
    phylib_coord distance;
    distance.x = 0.0;
    distance.y = 0.0;
    double dDistance = 0.0;
    phylib_coord cushionCoord;
    cushionCoord.x = 0.0;
    cushionCoord.y = 0.0;
    if (obj2 != NULL) {
        if (obj2 -> type == PHYLIB_ROLLING_BALL) {
            distance = phylib_sub(obj1 -> obj.rolling_ball.pos, obj2 -> obj.rolling_ball.pos);
            dDistance = phylib_length(distance) - PHYLIB_BALL_DIAMETER;
        } else if (obj2 -> type == PHYLIB_STILL_BALL) {
            distance = phylib_sub(obj1 -> obj.rolling_ball.pos, obj2 -> obj.still_ball.pos);
            dDistance = phylib_length(distance) - PHYLIB_BALL_DIAMETER;
        } else if (obj2 -> type == PHYLIB_HOLE) {
            distance = phylib_sub(obj1 -> obj.rolling_ball.pos, obj2 -> obj.hole.pos);
            dDistance = phylib_length(distance) - PHYLIB_HOLE_RADIUS;
        }
        // cushions
        else if (obj2 -> type == PHYLIB_VCUSHION) {
            dDistance = fabs(obj2->obj.vcushion.x - obj1->obj.rolling_ball.pos.x) - PHYLIB_BALL_RADIUS;
        } else if (obj2 -> type == PHYLIB_HCUSHION) {
            dDistance = fabs(obj2->obj.hcushion.y - obj1->obj.rolling_ball.pos.y) - PHYLIB_BALL_RADIUS;
        } else {
            return -1.0;
        }
    }

    return dDistance;
}
/* calculate distance between obj1 and obj2. obj1 must
be a rolling ball. return -1.0 otherwise. ....... see the doc */

void phylib_roll(phylib_object * new, phylib_object * old, double time) {
    if (new == NULL || old == NULL){
        return;
    }
    if ((new -> type != PHYLIB_ROLLING_BALL) || (old -> type != PHYLIB_ROLLING_BALL)) {
        return;
    }
    double newX = 0.0;
    newX = old -> obj.rolling_ball.pos.x + (old -> obj.rolling_ball.vel.x * time);
    newX += (0.5 * old -> obj.rolling_ball.acc.x) * (time * time);
    new -> obj.rolling_ball.pos.x = newX;
    double newY = 0.0;
    newY = old -> obj.rolling_ball.pos.y + (old -> obj.rolling_ball.vel.y * time);
    newY += (0.5 * old -> obj.rolling_ball.acc.y) * (time * time);
    new -> obj.rolling_ball.pos.y = newY;

    new -> obj.rolling_ball.vel.x = old -> obj.rolling_ball.vel.x + (old -> obj.rolling_ball.acc.x * time);
    new -> obj.rolling_ball.vel.y = old -> obj.rolling_ball.vel.y + (old -> obj.rolling_ball.acc.y * time);
    if (!SAME_SIGN(new -> obj.rolling_ball.vel.x, old -> obj.rolling_ball.vel.x)) {
        new -> obj.rolling_ball.vel.x = 0.0;
        new -> obj.rolling_ball.acc.x = 0.0;
    }
    if (!SAME_SIGN(new -> obj.rolling_ball.vel.y, old -> obj.rolling_ball.vel.y)) {
        new -> obj.rolling_ball.vel.y = 0.0;
        new -> obj.rolling_ball.acc.y = 0.0;
    }
}
// updates the new ball after the old ball has rolled for a period of time

unsigned char phylib_stopped(phylib_object * object) {
    double vLength = 0.0;
    if (object == NULL || object->type != PHYLIB_ROLLING_BALL){
        return 0;
    }
    vLength = phylib_length(object -> obj.rolling_ball.vel);
    if (vLength < PHYLIB_VEL_EPSILON) {
        object->type = PHYLIB_STILL_BALL;
        object -> obj.rolling_ball.acc.x = 0.0;
        object -> obj.rolling_ball.acc.y = 0.0;
        object -> obj.rolling_ball.vel.x = 0.0;
        object -> obj.rolling_ball.vel.y = 0.0;
        object -> obj.still_ball.number = object -> obj.rolling_ball.number;
        object -> obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
        object -> obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;
        return 1;
    }
    return 0;
}
// checks if a rolling ball has stopped and converts it to a still ball

void phylib_bounce(phylib_object ** a, phylib_object ** b) {
    if (b != NULL) {
        int caseNum = (int)(( * b) -> type);
        phylib_coord r_ab;
        phylib_coord v_rel;
        phylib_coord n;
        double v_rel_n = 0.0;
        double aSpeed = 0.0;
        double bSpeed = 0.0;
        switch (caseNum) {
        case 0: // still ball
            ( * b) -> type = PHYLIB_ROLLING_BALL;
            ( * b) -> obj.rolling_ball.number = ( * b) -> obj.still_ball.number;
            ( * b) -> obj.rolling_ball.pos = ( * b) -> obj.still_ball.pos;
        case 1: // rolling ball
            r_ab = phylib_sub(( * a) -> obj.rolling_ball.pos, ( * b) -> obj.rolling_ball.pos);
            v_rel = phylib_sub(( * a) -> obj.rolling_ball.vel, ( * b) -> obj.rolling_ball.vel);
            n.x = (r_ab.x) / (phylib_length(r_ab));
            n.y = (r_ab.y) / (phylib_length(r_ab));
            v_rel_n = phylib_dot_product(v_rel, n);
            ( * a) -> obj.rolling_ball.vel.x  -= (v_rel_n * n.x);
            ( * a) -> obj.rolling_ball.vel.y -=(v_rel_n * n.y);
            ( * b) -> obj.rolling_ball.vel.x += (v_rel_n * n.x);
            ( * b) -> obj.rolling_ball.vel.y += (v_rel_n * n.y);
            aSpeed = phylib_length(( * a) -> obj.rolling_ball.vel);
            if (aSpeed > PHYLIB_VEL_EPSILON) {
                ( * a) -> obj.rolling_ball.acc.x = ((( * a) -> obj.rolling_ball.vel.x) * (-1)) / aSpeed * PHYLIB_DRAG;
                ( * a) -> obj.rolling_ball.acc.y = ((( * a) -> obj.rolling_ball.vel.y) * (-1)) / aSpeed * PHYLIB_DRAG;
            }
            bSpeed = phylib_length(( * b) -> obj.rolling_ball.vel);
            if (bSpeed > PHYLIB_VEL_EPSILON) {
                ( * b) -> obj.rolling_ball.acc.x = ((( * b) -> obj.rolling_ball.vel.x) * (-1)) / bSpeed * PHYLIB_DRAG;
                ( * b) -> obj.rolling_ball.acc.y = ((( * b) -> obj.rolling_ball.vel.y) * (-1)) / bSpeed * PHYLIB_DRAG;
            }
            break;
        case 2: // hole
            free( * a);
            * a = NULL;
            break;
        case 3: // hcushion
            ( * a) -> obj.rolling_ball.acc.y *= -1;
            ( * a) -> obj.rolling_ball.vel.y *= -1;
            break;
        case 4: // vcushion
            ( * a) -> obj.rolling_ball.acc.x *= -1;
            ( * a) -> obj.rolling_ball.vel.x *= -1;
            break;
        }
    }
}
// bounces two objects (**a should be a rolling ball)

unsigned char phylib_rolling(phylib_table * t) {
    int rolling = 0;
    if (t != NULL){
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (t -> object[i] != NULL && t -> object[i] -> type == PHYLIB_ROLLING_BALL) {
            rolling++;
        }
    }
    }
    return rolling;
}
// counts rolling balls on the table

phylib_table * phylib_segment(phylib_table * table) {
    if (table == NULL || phylib_rolling(table) == 0) {
        return NULL;
    }
    phylib_table * newTable = phylib_copy_table(table);
    double tempTime = PHYLIB_SIM_RATE;
    while (tempTime <= PHYLIB_MAX_TIME) {
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            // object loop
            if (newTable -> object[i] != NULL && newTable -> object[i] -> type == PHYLIB_ROLLING_BALL) {
                phylib_roll(newTable -> object[i], table -> object[i], tempTime);
            }
        }
        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++){
                for (int k = 0; k < PHYLIB_MAX_OBJECTS; k++){
                    if (j != k && newTable->object[j] != NULL && newTable->object[k] != NULL){
                        double tempDist = phylib_distance(newTable->object[j], newTable->object[k]);
                        if (tempDist < 0.0 && tempDist != -1.0){
                            phylib_bounce(&(newTable->object[j]), &(newTable->object[k]));
                            newTable -> time += tempTime;
                            return newTable;
                        }
                    }
                }
                 if (phylib_stopped(newTable->object[j])){
                    newTable -> time += tempTime;
                    return newTable;
                }
            }
        tempTime += PHYLIB_SIM_RATE;
    }  
    newTable -> time += tempTime;
    return newTable;
}
/* returns a copy of a table after balls have rolled and
a ball has stopped, bounced or PHYLIB_MAX_TIME is reached */

/////////////////////////////////////////////////////

// ASSIGNMENT 2

char * phylib_object_string(phylib_object * object) {
    static char string[80];
    if (object == NULL) {
        snprintf(string, 80, "NULL;");
        return string;
    }
    switch (object -> type) {
    case PHYLIB_STILL_BALL:
        snprintf(string, 80,
            "STILL_BALL (%d,%6.6lf,%6.6lf)",
            object -> obj.still_ball.number,
            object -> obj.still_ball.pos.x,
            object -> obj.still_ball.pos.y);
        break;
    case PHYLIB_ROLLING_BALL:
        snprintf(string, 80,
            "ROLLING_BALL (%d,%6.6lf,%6.6lf,%6.6lf,%6.6lf,%6.6lf,%6.6lf)",
            object -> obj.rolling_ball.number,
            object -> obj.rolling_ball.pos.x,
            object -> obj.rolling_ball.pos.y,
            object -> obj.rolling_ball.vel.x,
            object -> obj.rolling_ball.vel.y,
            object -> obj.rolling_ball.acc.x,
            object -> obj.rolling_ball.acc.y);
        break;
    case PHYLIB_HOLE:
        snprintf(string, 80,
            "HOLE (%6.6lf,%6.6lf)",
            object -> obj.hole.pos.x,
            object -> obj.hole.pos.y);
        break;
    case PHYLIB_HCUSHION:
        snprintf(string, 80,
            "HCUSHION (%6.6lf)",
            object -> obj.hcushion.y);
        break;
    case PHYLIB_VCUSHION:
        snprintf(string, 80,
            "VCUSHION (%6.6lf)",
            object -> obj.vcushion.x);
        break;
    }
    return string;
    
}
/* The phylib_wrap.c file should be compiled with the -fPIC option and the -I option with the path
to the python include file to create a phylib_wrap.o file. */
