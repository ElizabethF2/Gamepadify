#!/usr/bin/env python3

# Randomly moves the mouse once per minute to keep an application from
# timing out due to inactivity

import random, time
from gamepadify import *

def main():
  sr = random.SystemRandom()
  try:
    while True:
      x, y = 0, 0
      while x == 0 and y == 0:
        x = sr.randint(-1, 1)
        y = sr.randint(-1, 1)
      move_mouse(x, y)
      time.sleep(60)
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  main()
