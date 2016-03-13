import sys
from termcolor import colored

WARNING = 0
PRIMARY = 1
ALERT   = 2

def readFileName():
    if(len(sys.argv) > 1):
        filename = sys.argv[1]
    else:
        raise Exception("No file name specified")
    return filename

def color_print(s, importance = WARNING):
    color = "red"
    if importance == PRIMARY:
        color = "blue"
    elif importance == ALERT:
        color = "yellow"
    else:
        color = "green"
    print colored(s, color)
