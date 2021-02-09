#!/usr/bin/env python3
'''
This is the main file that will control all functionality of the game
'''

import argparse
import getpass
#import imp
import importlib.machinery
import types
import os
import sys
#from docs import static

import glob


LEVEL_DIR = '/opt/lks_game/levels/'
DOC_DIR = '/opt/lks_game/docs/goals/'
NO_DOC = 'No documentation exists for the provided level.'


def level_num_to_pp(txt):
    '''
    Convert 'L0001.py' to 'Level 1'
    '''

    filename = txt
    if '/' in txt:
        ## we were given a full path!
        parts_temp = txt.split('/')
        filename = parts_temp[-1]

    parts = filename.split('.py')
    level_num = int(parts[0][1:])
    return "Level {0}".format(level_num)


def boolean_pp(txt):
    if txt in [True, 'True']:
        return "Passed"
    elif txt in [False, 'False']:
        return "Failed"

def get_current_user():
    if 'SUDO_USER' in os.environ:
        return os.environ['SUDO_USER']
    elif 'USER' in os.environ and os.environ['USER'] != 'root':
        return os.environ['USER']

    return getpass.getuser()


def level_enabled(level):
    '''
    Check to see if a specific level is enabled.
    '''

    if '.swp' in level:
        return False

    if '/' in level:
        ## might be full path?
        path_parts = level.split('/')
        level = path_parts[-1]

    if '.py' in level:
        ext_parts = level.split('.')
        level = int(ext_parts[0][1:])

    level_filename = lambda x: ('L{0}.py'.format(str(x).zfill(4)))

    level_path = os.path.join(LEVEL_DIR, level_filename(level))

    if not os.path.exists(level_path):
        return False

    loader = importlib.machinery.SourceFileLoader(level_filename(level),
                                                  level_path)

    py_mod = types.ModuleType(loader.name)
    loader.exec_module(py_mod)

    if hasattr(py_mod, 'enabled') and py_mod.enabled:
        return True
    else:
        return False


def list_of_available_levels():
    out = list()

    for level in os.listdir(LEVEL_DIR):
        level_path = os.path.join(LEVEL_DIR, level)
        if os.path.isfile(level_path) and level_enabled(level):
            out.append(level_path)

    return out


def highest_existing_level():
    onlylevels = list_of_available_levels()
    #for x in os.listdir(LEVEL_DIR):
        #x_path = os.path.join(LEVEL_DIR, x)
        #if os.path.isfile(x_path) and level_enabled(x):
            #onlylevels.append(x)

    levels = sorted(onlylevels)
    highest_level = levels[-1].split('/')[-1][1:-3]
    return int(highest_level)



def grab_doc_for_level(level, display=True, fallback=False, description=False):

    if level > highest_existing_level():
        level = highest_existing_level()

    level_filename = lambda x: ('L{0}.py'.format(str(x).zfill(4)))

    level_path = os.path.join(LEVEL_DIR, level_filename(level))

    prev_level_path = os.path.join(LEVEL_DIR, level_filename(level - 1))

    level_path_to_open = level_path

    if not os.path.exists(level_path):
        if fallback and os.path.exists(prev_level_path):
            level -= 1
            level_path_to_open = prev_level_path
        else:
            if display:
                print('a')
                print(NO_DOC)
                return False

    loader = importlib.machinery.SourceFileLoader(level_filename(level),
                                                level_path_to_open)

    py_mod_doc = types.ModuleType(loader.name)
    loader.exec_module(py_mod_doc)

    if not py_mod_doc.enabled:
        print('b')
        print(NO_DOC)
        return False

    if display:
        print(py_mod_doc.check_level.__doc__)

    if hasattr(py_mod_doc, 'description') and description:
        return py_mod_doc.description

    if not hasattr(py_mod_doc, 'description') and description:
        return

    return py_mod_doc.check_level.__doc__


def highest_completed_level(user):
    highest_level = 0

    for level in range(1, highest_existing_level() + 1):
        result = check_specific_level(user, level, display=False)
        if result:
            highest_level = level
        else:
            break

    return highest_level


def check_all_levels(user, display=True):
    onlylevels = list()

    for f in os.listdir(LEVEL_DIR):
        f_path = os.path.join(LEVEL_DIR, f)
        if os.path.isfile(f_path) and "swp" not in f:
            onlylevels.append(f_path)

    #onlylevels = [os.path.join(LEVEL_DIR, f) for f in os.listdir(LEVEL_DIR) if
                  #os.path.isfile(os.path.join(LEVEL_DIR, f))]

    pass_all_levels = False

    results = list()

    for level in sorted(onlylevels):
        loader = importlib.machinery.SourceFileLoader(level_num_to_pp(level), level)
        mod = types.ModuleType(loader.name)
        loader.exec_module(mod)
        if hasattr(mod, 'check_level') and hasattr(mod, 'enabled') and mod.enabled:
            result = mod.check_level(user)

            if display:
                print('{0}: {1}'.format(level_num_to_pp(level), boolean_pp(result)))

            results.append(result)

    if all(results) and display:
        print('Congratulations on passing all levels!')

    return results


def check_specific_level(user, level, display=True):
    '''
    Check if a given 'user' has passed a specific 'level'
    '''

    fix_level = str(level).zfill(4)

    level_check = os.path.join(LEVEL_DIR, 'L{0}.py'.format(fix_level))

    value = False
    result = None

    if os.path.exists(level_check):
        loader = importlib.machinery.SourceFileLoader(level_num_to_pp(level_check), level_check)
        mod = types.ModuleType(loader.name)
        loader.exec_module(mod)

        if hasattr(mod, 'check_level') and hasattr(mod, 'enabled') and mod.enabled:
            result = mod.check_level(user)
            if result:
                value = result
        elif hasattr(mod, 'check_level') and hasattr(mod, 'enabled') and user in ['yano']:
            result = mod.check_level(user)
            if result:
                value = result
        #py_mod = imp.load_source(LEVEL_DIR, level_check)
        #result = py_mod.check_level(user)
        if display:
            print('Level {0}: {1}'.format(fix_level, boolean_pp(result)))
    else:
        if display:
            print('The provided level does not exist or is not available for checking at this time.')

    return value


def main():
    '''Main routine function'''

    ## Determine whether to check a specific Level or all available Levels
    check_all_levels(get_current_user())
    return


if __name__ == '__main__':

    # iniate the parser
    parser = argparse.ArgumentParser(description='LKS Game')

    # add long and short arguments
    parser.add_argument('-l', '--level', help='Specify a level',
                        type=int)

    parser.add_argument('-c', '--check',
                        action='store_true',
                        help='Specify that you want the LKS-Game to check' + \
                        ' your work. With "--user" you can also check' + \
                        ' another user.')

    parser.add_argument('-u', '--user',
                        help='Specify a user.')

    parser.add_argument('-d', '--doc', '-g', '--goal', '--goals', dest='docs',
                        action='store_true',
                        help='Display documentation for your current level.' + \
                        ' With "--level" show goal(s) for that level.')

    parser.add_argument('-s', '--start',
                        action='store_true',
                        help="If you don't know where to begin. Start here.")

    # read arguments from the command line
    args = parser.parse_args()

    #if args.help:

    if args.start:
        print(static.FIRST_TIME)
        sys.exit(0)

    if args.check:
        # check for --level
        if args.level and args.user:
            check_specific_level(args.user, int(args.level))
        elif args.user:
            ## We have a --check with no argument
            check_all_levels(args.user)
        elif args.level:
            check_specific_level(get_current_user(), int(args.level))
        else:
            main()

    if args.docs:
        ## Show documentation or goal for a a given level
        if args.level:
            ## show doc for specific level
            grab_doc_for_level(args.level)

        elif not args.level:
            ## user only did: "--doc" with no level info provided
            user_highest_level = highest_completed_level(get_current_user())
            grab_doc_for_level(user_highest_level + 1, fallback=True)

    action_flags = [args.check, args.docs]

    if args.user and not any(action_flags):
        print("You have provided only a user. What would you like to do?")
        sys.exit(1)

    if args.level and not any(action_flags):
        print("You have provided only a level. What would you like to do?")
        sys.exit(1)

    #$if not args.user and not args.level and not args.check:
    if not any([args.user, args.level, args.check, args.docs]):
        parser.print_help()
