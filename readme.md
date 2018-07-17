LKS Game
--------

This is a game written in Python to help userse learn Linux.

Setup
=====

Step One
========

As an admin with sudo powers

$ `sudo ./setup_game.sh`

This sets up EVERYBODY with a game folder!


Step Two
========

Compile main.sh with the [Shell Script Compiler tool (SHC)](http://www.datsi.fi.upm.es/~frosal/).

$ `shc -U -f main.sh -o game`

Put this all in your `/opt/lks_game/`


Step Three
==========

Add `/opt/lks_game/game` to the system PATH for all users.
