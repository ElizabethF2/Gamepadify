#!/usr/bin/env python3

import sys
from . import *

def callback(event):
  if event.kind == 'TICK':
    return
  print('Device Name:', repr(event.device.name))
  print('Device UID:', repr(event.device.uid))
  print('Device Path:', event.device.path)
  print('Event:', event)
  print('')

def main():
  kwargs = {}
  if len(sys.argv) > 1:
    kwargs['names_of_interest'] = sys.argv[1]
  automatically_handle_controllers(callback, **kwargs)

if __name__ == '__main__':
  main()
