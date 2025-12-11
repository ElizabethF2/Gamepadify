#!/usr/bin/env python3

import sys, os, signal, time
from gamepadify import *

mymappings = {
  ('2.4G RF Keyboard & Mouse', KEY, ENTER_KEY): {
    'kind': BUTTON,
    'key': LEFT_MOUSE,
  },
  ('2.4G RF Keyboard & Mouse', KEY, BACKSPACE_KEY): {
    'kind': BUTTON,
    'key': RIGHT_MOUSE,
  },
  ('2.4G RF Keyboard & Mouse', KEY, W_KEY): {
    'kind': MOUSE,
    'axis': MOUSE_Y,
    'amount': -3000,
  },
  ('2.4G RF Keyboard & Mouse', KEY, S_KEY): {
    'kind': MOUSE,
    'axis': MOUSE_Y,
    'amount': 3000,
  },
  ('2.4G RF Keyboard & Mouse', KEY, A_KEY): {
    'kind': MOUSE,
    'axis': MOUSE_X,
    'amount': -3000,
  },
  ('2.4G RF Keyboard & Mouse', KEY, D_KEY): {
    'kind': MOUSE,
    'axis': MOUSE_X,
    'amount': 3000,
  },
}

def mycallback(event):
  device = event.device
  dl = device_local(device)
  enabled = dl.get('enabled', False)

  if event.kind == KEY and \
     event.name == NUMBER_1_KEY and \
     event.value == 0 and \
     P_KEY in device.held_buttons:
    dl['enabled'] = not enabled
    if enabled:
      release_exclusive_access(device)
    else:
      grab_exclusive_access(device)
    return

  if not enabled:
    return
  
  if remap(mymappings, event):
    return
  
  if event.kind == KEY and event.name == ESC_KEY:
    os.kill(os.getpid(), signal.SIGINT)
    return
  
  # Pass through any keys that haven't been remapped
  # The event gets proxied from the real keyboard to Gamepadify's virtual keyboard
  # This ensures non-remapped keys can still be used even when enabled is true
  if event.name not in (NUMBER_1_KEY, P_KEY):
    emit(event.kind, event.name, event.value)

def main():
  try:
    automatically_handle_controllers(mycallback,
                                     names_of_interest = '2.4G RF Keyboard & Mouse')
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  main()
