import time
import sys
import os
#import curses
"""
toolbar_width = 40

# setup toolbar
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

for i in range(toolbar_width):
    time.sleep(0.1) # do real work here
    # update the bar
    sys.stdout.write("-")
    sys.stdout.flush()

sys.stdout.write("\n")
"""
"""
for i in range(10):
	print(i)

stdscr = curses.initscr()
"""
"""
for i in range(10):
	sys.stdout.write("\l" * 2)
	sys.stdout.write("Her")
"""
for i in range(10):
	print(i)
os.system("cls")
for i in range(10, 20):
	print(i)