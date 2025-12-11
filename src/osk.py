#!/usr/bin/env python3

import sys, os, time
import qtpy.QtWidgets, qtpy.QtCore, qtpy.QtGui
from . import *

APP_ID = 'Gamepadify.OSK'

LAYOUT = [
  'Esc F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12 PgUp',
  '` 1 2 3 4 5 6 7 8 9 0 - = Back PgDn',
  'Tab q w e r t y u i o p [ ] \\ Del',
  'Caps a s d f g h j k l ; \' Enter Home',
  'Shift z x c v b n m , . / RShift End',
  'Ctrl Alt Space RAlt RCtrl',
]

# TODO fix hover

STYLE_SHEET = '''
  color: #17f50C;
  background-color: #000;
  
  QPushButton::hover
  {
  background-color : lightgreen;
  }
'''

HOLDABLE_KEYS = {
  'Shift': LEFT_SHIFT,
  'RShift': RIGHT_SHIFT,
  'Ctrl': LEFT_CTRL,
  'RCtrl': RIGHT_CTRL,
  'Alt': LEFT_ALT,
  'RAlt': RIGHT_ALT,
  'Caps': CAPSLOCK_KEY,
}

SHIFTABLE_KEYS = {v: k for k,v in SHIFTED_KEYS.items()}

def get_key_text(members, name, pressed):
  held_keys = members['held_keys']
  capslock = 'Caps' in held_keys
  shift = 'Shift' in held_keys or 'RShift' in held_keys
  if shift and not capslock:
    n = SHIFTABLE_KEYS.get(name)
    if n == '&':
      n = '&&'
    elif not n:
      n = name.upper() if len(name) == 1 else name
  elif capslock and not shift:
    n = name.upper() if len(name) == 1 else name
  elif shift and capslock:
    n = SHIFTABLE_KEYS.get(name)
    if n == '&':
      n = '&&'
    elif not n:
      n = name
  else:
    n = name
  if pressed and len(n) > 1:
    n = n.upper()
  return ('[ ' + n + ' ]') if pressed else n

def key_down(members, name):
  key = KEYMAP.get(name)
  if key and name not in HOLDABLE_KEYS:
    press_key(key)
    members['keys'][name].setText(get_key_text(members, name, True))

def release_hkey(members, name):
  hkey = HOLDABLE_KEYS.get(name)
  members['keys'][name].setText(name)
  members['held_keys'].remove(name)
  if name == 'Caps':
    press_key(hkey)
  release_key(hkey)
  if name in ('Shift', 'RShift', 'Caps'):
    for k, btn in members['keys'].items():
      if k not in HOLDABLE_KEYS:
        btn.setText(get_key_text(members, k, False))

def key_up(members, name):
  if (hkey := HOLDABLE_KEYS.get(name)):
    held_keys = members['held_keys']
    if name in held_keys:
      release_hkey(members, name)
    else:
      members['keys'][name].setText(get_key_text(members, name, True))
      held_keys.add(name)
      press_key(hkey)
      if name == 'Caps':
        release_key(hkey)
      if name in ('Shift', 'RShift', 'Caps'):
        for k, btn in members['keys'].items():
          if k not in HOLDABLE_KEYS:
            btn.setText(get_key_text(members, k, False))
  elif (key := KEYMAP.get(name)):
    release_key(key)
    members['keys'][name].setText(get_key_text(members, name, False))
    for n in list(members['held_keys']):
      if n != 'Caps':
        release_hkey(members, n)

def get_window_geometry_path():
  xdg_state_dir = os.environ.get('XDG_STATE_DIR', '~/.local/state')
  xdg_state_dir = os.path.expanduser(xdg_state_dir)
  return os.path.join(xdg_state_dir, 'gamepadify_osk')

def window_geometry_changed(unused, members):
  if not members.get('save_window_geometry'):
    return
  window = members.get('window')
  old_geometry = members.get('window_geometry')
  geometry = bytes(window.saveGeometry())
  if geometry != old_geometry:
    path = members.get('window_geometry_path')
    if not path:
      path = get_window_geometry_path()
    os.makedirs(os.path.dirname(path), exist_ok = True)
    with open(path, 'wb') as f:
      f.write(geometry)

def show(style_sheet = STYLE_SHEET,
         layout = LAYOUT,
         save_window_geometry = True,
         window_geometry_path = None):
  app = qtpy.QtWidgets.QApplication(['Gamepadify-OSK'])
  window = qtpy.QtWidgets.QWidget()
  app.setDesktopFileName(APP_ID)
  if style_sheet:
    window.setStyleSheet(style_sheet)
  window.setWindowFlags(
    qtpy.QtCore.Qt.WindowStaysOnTopHint |
    qtpy.QtCore.Qt.WindowDoesNotAcceptFocus
  )
  main_layout = qtpy.QtWidgets.QVBoxLayout()
  main_layout = qtpy.QtWidgets.QVBoxLayout()
  members = {
    'window': window,
    'keys': {},
    'held_keys': set(),
    'save_window_geometry': save_window_geometry,
  }
  if get_lit_leds('capslock'):
    members['held_keys'].add('Caps')
  if window_geometry_path:
    members['window_geometry_path'] = window_geometry_path
  else:
    window_geometry_path = get_window_geometry_path()

  try:
    with open(window_geometry_path, 'rb') as f:
      members['window_geometry'] = f.read()
      window.restoreGeometry(members['window_geometry'])
  except FileNotFoundError:
    pass
  
  window.moveEvent = lambda *u,m=members: window_geometry_changed(u,m)
  window.resizeEvent = lambda *u,m=members: window_geometry_changed(u,m)

  for row in layout:
    row_layout = qtpy.QtWidgets.QHBoxLayout()
    for key in row.split():
      p = key in members['held_keys']
      btn = qtpy.QtWidgets.QPushButton(text = get_key_text(members, key, p))
      row_layout.addWidget(btn)
      btn.pressed.connect(lambda m=members, k=key: key_down(m, k))
      btn.released.connect(lambda m=members, k=key: key_up(m, k))
      btn.setMinimumSize(10,10)
      members['keys'][key] = btn
      if key == 'Space':
        row_layout.setStretchFactor(btn, 4)      
    main_layout.addLayout(row_layout)

  window.setLayout(main_layout)
  window.show()
  app.exec()

def main():
  setup_virtual_mouse_and_keyboard()
  save_window_geometry = '--no-save-window-geometry' not in sys.argv
  show(save_window_geometry = save_window_geometry)

if __name__ == '__main__':
  main()
