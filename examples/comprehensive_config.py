#!/usr/bin/env python3
# #!/usr/bin/env pypy3

from gamepadify import *

DARK_GREEN = (0, 10, 0)
DARK_PURPLE = (10, 0, 10)
DARK_YELLOW = (10, 10, 0)
BRIGHT_GREEN = (0, 200, 0)
BRIGHT_RED = (200, 0, 0)

ELIGIBLE_UNLOCK_BUTTONS = {CROSS, CIRCLE, SQUARE, TRIANGLE, X_BUTTON}

PINS = {

  
  # (TRIANGLE, TRIANGLE, SQUARE, SQUARE, TRIANGLE, TRIANGLE): 'Alice',
  (TRIANGLE,): '_toggle_sddm',
}

TIMEOUT = 5 * 60 # seconds

mymappings = {
  ('Wireless Controller', DPAD, DPAD_X): {
    'kind': KEY,
    'negative_key': ARROW_LEFT,
    'positive_key': ARROW_RIGHT,
    'deadzone': 1,
  },
  ('Wireless Controller', DPAD, DPAD_Y): {
    'kind': KEY,
    'negative_key': ARROW_UP,
    'positive_key': ARROW_DOWN,
    'deadzone': 1,
  },
  ('Wireless Controller', STICK, LSTICK_X): {
    'kind': MOUSE,
    'axis': MOUSE_X,
    'deadzone': 18,
  },
  ('Wireless Controller', STICK, LSTICK_Y): {
    'kind': MOUSE,
    'axis': MOUSE_Y,
    'deadzone': 18,
  },
  ('Wireless Controller', STICK, RSTICK_Y): {
    'kind': MOUSE,
    'axis': MOUSE_WHEEL,
    'initial_speed': -1,
    'max_speed': -1,
    'acceleration': 1,
  },
  ('Wireless Controller', BUTTON, CROSS): {
    'kind': BUTTON,
    'key': LEFT_MOUSE,
  },
  ('Wireless Controller', BUTTON, TRIANGLE): {
    'kind': BUTTON,
    'key': RIGHT_MOUSE,
  },
  ('Wireless Controller', BUTTON, CIRCLE): {
    'kind': BUTTON,
    'key': MIDDLE_MOUSE,
  },
  ('Wireless Controller', BUTTON, OPTIONS): {
    'kind': KEY,
    'key': LEFT_META,
  },
  ('Wireless Controller', BUTTON, R3): {
    'kind': KEY,
    'key': ESC_KEY,
  },
}

for k,v in list(mymappings.items()):
  mymappings['Sony Interactive Entertainment Wireless Controller', *k[1:]] = v
  mymappings['DualSense Wireless Controller', *k[1:]] = v

mymappings.update({
  ('8Bitdo SN30 Pro', DPAD, DPAD_X): {
    'kind': KEY,
    'negative_key': ARROW_LEFT,
    'positive_key': ARROW_RIGHT,
    'deadzone': 1,
  },
  ('8Bitdo SN30 Pro', DPAD, DPAD_Y): {
    'kind': KEY,
    'negative_key': ARROW_UP,
    'positive_key': ARROW_DOWN,
    'deadzone': 1,
  },
  ('8Bitdo SN30 Pro', BUTTON, A_BUTTON): {
    'kind': BUTTON,
    'key': LEFT_MOUSE,
  },
  ('8Bitdo SN30 Pro', BUTTON, Y_BUTTON): {
    'kind': BUTTON,
    'key': RIGHT_MOUSE,
  },
  ('8Bitdo SN30 Pro', BUTTON, B_BUTTON): {
    'kind': BUTTON,
    'key': MIDDLE_MOUSE,
  },
})

for k,v in list(mymappings.items()):
  if k[0] == '8Bitdo SN30 Pro':
    mymappings['Pro Controller', *k[1:]] = v

mymappings.update({
  ('8Bitdo SN30 Pro', STICK, LSTICK_X): {
    'kind': MOUSE,
    'axis': MOUSE_X,
    'deadzone': 3000,
    'stick_center': 32768,
  },
  ('8Bitdo SN30 Pro', STICK, LSTICK_Y): {
    'kind': MOUSE,
    'axis': MOUSE_Y,
    'deadzone': 3000,
    'stick_center': 32768,
  },
  ('8Bitdo SN30 Pro', STICK, RSTICK_Y): {
    'kind': MOUSE,
    'axis': MOUSE_WHEEL,
    'initial_speed': -1,
    'max_speed': -1,
    'acceleration': 1,
    'stick_center': 32768,
  },
  ('8Bitdo SN30 Pro', BUTTON, START_BUTTON): {
    'kind': KEY,
    'key': LEFT_META,
  },

  ('Pro Controller', STICK, LSTICK_X): {
    'kind': MOUSE,
    'axis': MOUSE_X,
    'deadzone': 2200,
    'stick_center': 0,
    'bound': 32767,
  },
  ('Pro Controller', STICK, LSTICK_Y): {
    'kind': MOUSE,
    'axis': MOUSE_Y,
    'deadzone': 2200,
    'stick_center': 0,
    'bound': 32767,
  },
  ('Pro Controller', STICK, RSTICK_Y): {
    'kind': MOUSE,
    'axis': MOUSE_WHEEL,
    'initial_speed': -1,
    'max_speed': -1,
    'acceleration': 1,
    'deadzone': 2200,
  },
  ('Pro Controller', BUTTON, OPTIONS): {
    'kind': KEY,
    'key': LEFT_META,
  },
})

def flash_color(device, color, rumble_durations):
  import time
  for _ in range(3):
    set_rgb(device, color)
    rumble(device, rumble_durations[0])
    time.sleep(0.1)
    set_rgb(device, DARK_YELLOW)
    rumble(device, rumble_durations[1])
    time.sleep(0.1)

# TODO make "Wireless Controller" name handling more generic

def handle_pin_entry_mode(event, device, dl):
  pin_entry_mode_enabled = dl.get('pin_entry_mode_enabled')

  if (not pin_entry_mode_enabled and
      ((button_released(event, R1) and
       SHARE in device.held_buttons and
       R3 in device.held_buttons) or
      (button_released(event, RB_BUTTON) and
       SELECT_BUTTON in device.held_buttons and
       LSTICK_BUTTON in device.held_buttons))):
    dl['pin_entry_mode_enabled'] = True
    dl['unlock_pin_buffer'] = []
    set_rgb(device, DARK_YELLOW)
    for _ in range(3):
      rumble(device, 0.1)
      __import__('time').sleep(0.2)
    return True

  if not pin_entry_mode_enabled:
    return False
  
  if (event.kind == BUTTON and
      event.name in ELIGIBLE_UNLOCK_BUTTONS and
      not event.value):
    dl['unlock_pin_buffer'].append(event.name)
    return True

  if button_released(event, R1) or button_released(event, RB_BUTTON):
    user = PINS.get(tuple(dl['unlock_pin_buffer']))
    if user == '_toggle_sddm':
      __import__('subprocess').run(('systemctl', 
        'stop' if __import__('subprocess').run((
          'systemctl', 'is-active', '--quiet', 'sddm'
        )).returncode == 0 else 'start',
      'sddm'))
    elif user:
      import gamepadify.login
      gamepadify.login.try_login_or_unlock(user)
      flash_color(device, BRIGHT_GREEN, (0.3, 0.1))
    else:
      flash_color(device, BRIGHT_RED, (0.1, 0.3))
    dl.pop('pin_entry_mode_enabled')
    dl.pop('unlock_pin_buffer')
    set_rgb(device, DARK_GREEN)
    return True
  
  # Block other input if we're in pin entry mode
  return True

def mycallback(event):
  device = event.device
  dl = device_local(device)
  enabled = dl.get('enabled', True)
  is_xbox = (device.name == '8Bitdo SN30 Pro')

  if is_idle(TIMEOUT, event, mappings = mymappings, deadzone = 20):
    return disconnect_controller(device.uid)

  if ((not is_xbox and 
       button_held(event, L1) and 
       SHARE in device.held_buttons) or
      (is_xbox and 
       button_held(event, LB_BUTTON) and 
       SELECT_BUTTON in device.held_buttons)):
    enabled = not enabled
    dl['enabled'] = enabled
    set_rgb(device, DARK_GREEN if enabled else DARK_PURPLE)
    if enabled:
      grab_exclusive_access(device)
      rumble(device, 0.1)
      __import__('time').sleep(0.2)
      rumble(device, 0.1)
    else:
      release_exclusive_access(device)
      rumble(device, 0.1)
    return

  if not enabled:
    return

  if handle_pin_entry_mode(event, device, dl):
    return

  if remap(mymappings, event):
    return
  
  if button_released(event, PS_HOME) or button_released(event, GUIDE_BUTTON):
    return disconnect_controller(device.uid)

  if button_released(event, X_BUTTON) or \
     (not is_xbox and button_released(event, SQUARE)):
    
    # HACK HACK HACK
    # import sys
    # if hasattr(sys, 'pypy_version_info'):
    #   return toggle_osk(cmd = ('python3', '-m', 'gamepadify.osk'))

    return toggle_osk()

  if event.kind == BUTTON and event.name in (L2, R2):
    opposite = L2 if event.name == R2 else R2
    if opposite not in device.held_buttons:
      if event.value:
        press_key(LEFT_META)
        press_key(EQUALS_KEY if event.name == R2 else MINUS_KEY)
      else:
        release_key(EQUALS_KEY if event.name == R2 else MINUS_KEY)
        release_key(LEFT_META)

  if event.kind == CONNECTED:
    grab_exclusive_access(device)
    import gamepadify.wakelock
    dl['wakelock'] = gamepadify.wakelock.try_get_wakelock()
    return set_rgb(device, DARK_GREEN)

  if event.kind == DISCONNECTED and count_devices() <= 1:
    import os, signal
    os.kill(os.getpid(), signal.SIGINT)

def main():
  try:
    with open('/proc/self/comm', 'r+') as f:
      f.write('my-gamepadify')
  except (FileNotFoundError, PermissionError):
    pass

  try:
    __import__('os').nice(20)
  except (AttributeError, OSError):
    pass

  automatically_handle_controllers(
    mycallback,
    names_of_interest = \
      '(?i).*Wireless Controller$|8Bitdo.+$|Pro Controller$',
    idle_timeout = TIMEOUT,
    controller_timeout = TIMEOUT
  )

if __name__ == '__main__':
  main()
