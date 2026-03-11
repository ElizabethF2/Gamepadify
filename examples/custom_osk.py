#!/usr/bin/env python3

import gamepadify.osk as osk

LAYOUT = [
  '1 2 3',
  '4 5 6',
  '7 8 9',
  'Back 0 Enter ',
]

STYLE_SHEET = '''
  * {
    color: white;
    background-color: blue;
  }

  QPushButton {
    min-width: 5em;
    min-height: 5em;
  }
'''

def main():
  osk.show(layout = LAYOUT, style_sheet = STYLE_SHEET)

if __name__ == '__main__':
  main()
