#!/usr/bin/env python3

NAME_OF_GAME = "LKS Game"

FIRST_TIME = '''
Hello!

Welcome to {0}!

To begin, please contact your fellow system administrator(s) to set up your
~/game/ folder. Due to the nature of Linux and to prevent cheating, the initial
set up *must* be completed by somebody with elevated privileges.


Setup
=====

If you have a ~/game/ folder already and the output of `ls -hal` shows that
the group is 'gameadmins' then you are good to begin! :-)


## Layout

The game is structured with levels to test your knowledge and skills of Linux.

There are two "action" commands:
    * --check
    * --goals


### Goals

To start off, you can run the following:

    $ game --goal

This will do two things:
    * Display the "highest completed level" for you
    * and show the goal(s) for the current level

If at any time later you want to see the goal(s) listed for a specific level:

    $ game --goal --level X

Where X is the number of the level you want to check.


### Checking

If you would like to check your work for a specific level:

    $ game --check --level 1

If you want to check all available levels you can run:

    $ game --check

If you want to check a different user, for a specific level or all levels:

    $ game --check --user yano

This will check all levels for the user 'yano'

Additionally,

    $ game --check --level 7 --user yano

Will check to see if 'yano' has Passed or Failed Level 7, if the level is
available.


### Help

If at any time you need a quick refreshing of the commands and arguments
available you can run:

    $ game

or

    $ game --help


### Shortcuts

If you would prefer not to type out --check or the whole word for the commands,
you can use the shortcuts. The shortcuts are just "-X" where X is the first
letter of the longer command. For example:

    * -h for --help
    * -c for --check
    * -l for --level
    * -u for --user
    * -g for --goals


'''.format(NAME_OF_GAME)
