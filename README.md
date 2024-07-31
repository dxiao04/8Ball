
# Billiards/8 Ball Simulator

This project is a full stack web app (locally hosted and built from scratch) that allows two players to play a game of 8 ball. Completed for the University of Guelph's CIS2750/Angel of Death course.

## Physics Engine
Backend logic was developed in C. The physics engine simulates realistic ball movement and collisions between balls and walls. Calculated using balls' speeds, velocities, and directions at the point of collision. All types of phylib_object (and the table) were "converted" to classes in Python in Physics.py for ease of integration.
## Server
All server operations were written in Python. Game state, gameplay frames and GET/POST requests are also managed here (game.py).
## Frontend
The game interface and interactive components were implemented using HTML/CSS and Javascript/jQuery. 
- Game interface: Displays the players, pool table, and balls in an attractive and engaging fashion.
- User interactivity: All user interactions (including cue drawing) are designed to be intuitive and easy to understand.
