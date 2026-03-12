#!/usr/bin/env python3

import os
from . import *

def list_all_devices():
  results = []
  for fname in os.listdir(INPUT_PATH):
    if fname[:5] == 'event' and fname[5:].isdigit():
      path = os.path.join(INPUT_PATH, fname)
      with open(path, 'rb') as fh:
        name = get_ioctl(fh, EVIOCGNAME)
        uid = get_ioctl(fh, EVIOCGUNIQ)
      results.append({'path': path, 'name': name, 'uid': uid})
  return results

def main():
  for result in list_all_devices():
    print(f'Path: {result['path']}')
    print(f'Name: {result['name']}')
    print(f'UID: {result['uid']}')
    print('')

if __name__ == '__main__':
  main()
