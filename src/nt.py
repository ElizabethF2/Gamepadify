import sys, os
_exclude = set(locals().keys())

from . import *

_INPUT_MOUSE = 0
_INPUT_KEYBOARD = 1
_KEYEVENTF_KEYUP = 2

_VK_CAPITAL = 20
_VK_NUMLOCK = 144
_VK_SCROLL = 145

_vk_key_map = {
  LEFT_MOUSE: 1, # VK_LBUTTON
  RIGHT_MOUSE: 2, # VK_RBUTTON
  MIDDLE_MOUSE: 4, # VK_MBUTTON,
  BACKSPACE_KEY: 8, # VK_BACK
  TAB_KEY: 9, # VK_TAB
  ENTER_KEY: 13, # VK_RETURN
  CAPSLOCK_KEY: _VK_CAPITAL,
  ESC_KEY: 27, # VK_ESCAPE
  SPACE_KEY: 32, # VK_SPACE
  **{KEYMAP[str(i)]: ord(str(i)) for i in range(10)}, # 0 - 9
  **{KEYMAP[chr(i+65)]: i+65 for i in range(26)}, # A - Z
  LEFT_META: 91, # VK_LWIN
  RIGHT_META: 92, # VK_RWIN
  **{KEYMAP['F'+str(i+1)]: i+112 for i in range(24)}, # VK_F1 - VK_F24
  ARROW_UP: 38, # VK_UP
  ARROW_DOWN: 40, # VK_DOWN
  ARROW_LEFT: 37, # VK_LEFT
  ARROW_RIGHT: 39, # VK_RIGHT
  LEFT_SHIFT: 160, # VK_LSHIFT
  RIGHT_SHIFT: 161, # VK_RSHIFT
  LEFT_CTRL: 162, # VK_LCONTROL
  RIGHT_CTRL: 163, # VK_RCONTROL
  LEFT_ALT: 164, # VK_LMENU
  RIGHT_ALT: 165, # VK_RMENU
  EQUALS_KEY: 187, # VK_OEM_PLUS
  COMMA_KEY: 188, # VK_OEM_COMMA
  MINUS_KEY: 189, # VK_OEM_MINUS
  PERIOD_KEY: 190, # VK_OEM_PERIOD
  SEMICOLON_KEY: 186, # VK_OEM_1
  SLASH_KEY: 191, # VK_OEM_2
  GRAVE_KEY: 192, # VK_OEM_3
  LEFT_BRACKET_KEY: 219, # VK_OEM_4
  BACKSLASH_KEY: 220, # VK_OEM_5
  RIGHT_BRACKET_KEY: 221, # VK_OEM_6
  APOSTROPHE_KEY: 222, # VK_OEM_7
}

_mouse_wheel_map = {
  REL_HWHEEL: 4096,  # MOUSEEVENTF_HWHEEL
  MOUSE_WHEEL: 2048, # MOUSEEVENTF_WHEEL
}

_led_map = {
  'capslock': ('VK_CAPITAL', _VK_CAPITAL),
  'numlock': ('VK_NUMLOCK', _VK_NUMLOCK),
  'scrolllock': ('VK_SCROLL', _VK_SCROLL),
}

_FILE_SHARE_READ = 1
_FILE_SHARE_WRITE = 2
_GENERIC_READ = 0x80000000
_GENERIC_WRITE = 0x40000000
_OPEN_EXISTING = 3
_FILE_ATTRIBUTE_NORMAL = 128
_FILE_FLAG_NO_BUFFERING = 0x20000000
_FILE_FLAG_WRITE_THROUGH = 0x80000000

# TODO error handling
def _call(dll, func, *args):
  import ctypes
  return getattr(getattr(ctypes.windll, dll), func)(*args)

def _setup_virtual_input_with_lock(ename, bits):
  if bits and UI_SET_RELBIT in bits:
    import io
    return io.BytesIO()
  class VigemClient():
    def __init__(self):
      pass
    def __del__(self):
      pass
  raise NotImplementedError('')
  return VigemClient()

def _open(path, mode = 'rb', exclusive = False):
  import ctypes, msvcrt
  name = ctypes.create_unicode_buffer(path)
  access = _GENERIC_READ
  if '+' in mode:
    access |= _GENERIC_WRITE
  if exclusive:
    share = _FILE_SHARE_WRITE if '+' in mode else _FILE_SHARE_READ
  else:
    share = 0
  disposition = _OPEN_EXISTING
  flags = (
    FILE_ATTRIBUTE_NORMAL | _FILE_FLAG_NO_BUFFERING | _FILE_FLAG_WRITE_THROUGH
  )
  handle = _call(
    'Kernel32', 'CreateFileW',
    path, access, share, None, disposition, flags, None
  )
  fh = msvcrt.open_osfhandle(handle)
  return open(fh, mode, buffering = False)

def wait_for_input_events(path,
                          callback,
                          sync_axis = True,
                          names_of_interest = DEFAULT_NAMES_OF_INTEREST,
                          timeout = None):
  with _open(path) as fh:
    # dname = TODO get device name
    if not __import__('re').match(names_of_interest, dname):
      return
    # uid = TODO get device uid
    device = Device(path, dname, uid, fh)
    if sync_axis:
      enqued_events = []
    os.set_blocking(fh.fileno(), False)
    try:
      # TODO register for WM_INPUT
      with _lock:
        intd = {'connected': True}
        _internal_state[dname, uid] = intd
      callback(ControllerEvent(device, None, CONNECTED, None, None))
      while intd['connected']:
        # TODO wait for WM_INPUT w/ timeout
        # if len(ep.poll(timeout = timeout)) < 1:
          # callback(ControllerEvent(device, None, DEVICE_IDLE, None, None))
        while True:
          try:
            buf = device.fh.read(24)
          except OSError as err:
            if err.errno == __import__('errno').ENODEV:
              intd['connected'] = False
              break
            else:
              raise err
          if not buf:
            break
          # Parse buf and convert to evdev types
          if _type == EV_KEY:
            if value:
              device.held_buttons.add(code)
            else:
              try:
                device.held_buttons.remove(code)
              except KeyError:
                pass
            callback(ControllerEvent(device, ts, _type, code, value))
          elif _type in (EV_ABS, EV_REL):
            device.axis[code] = value
            event = ControllerEvent(device, ts, _type, code, value)
            if sync_axis:
              enqued_events.append(event)
            else:
              callback(event)
          elif _type == EV_SYN and code == SYN_REPORT and sync_axis:
            if enqued_events:
              for event in enqued_events:
                callback(event)
              enqued_events = []
            else:
              callback(ControllerEvent(device, ts, TICK, None, None))
          else:
            callback(ControllerEvent(device, ts, TICK, None, None))
      callback(ControllerEvent(device, None, DISCONNECTED, None, None))
    finally:
      _cleanup_device(device)
      # TODO unsubscribe from WM_INPUT

def handle_controllers(callback,
                       ignore_existing = False,
                       ignore_new = False,
                       sync_axis = True,
                       names_of_interest = DEFAULT_NAMES_OF_INTEREST,
                       timeout = None):
  try:
    if not ignore_new:
      pass # TODO subscribe to WM_DEVICECHANGE and WM_INPUT_DEVICE_CHANGE
    if not ignore_existing:
      pass # TODO emum via SetupDiGetClassDevs
      # for name in os.listdir(INPUT_PATH):
      #   path = os.path.join(INPUT_PATH, name)
      #   if name[:5] == 'event' and name[5:].isdigit():
      #     callback(path,
      #              sync_axis = sync_axis,
      #              names_of_interest = names_of_interest,
      #              timeout = timeout)
  finally:
    if not ignore_new:
      pass # TODO unsubscribe from WM_DEVICECHANGE and WM_INPUT_DEVICE_CHANGE

def _send_input(mouse_x = 0,
                mouse_y = 0,
                mouse_data = 0,
                flags = 0,
                vk = None):
  if vk is None:
    buf = (
      _INPUT_MOUSE.to_bytes(4, byteorder = sys.byteorder, signed = True) +
      mouse_x.to_bytes(4, byteorder = sys.byteorder, signed = True) +
      mouse_y.to_bytes(4, byteorder = sys.byteorder, signed = True) +
      mouse_data.to_bytes(4, byteorder = sys.byteorder, signed = True)
    )
  else:
    buf = (
      _INPUT_KEYBOARD.to_bytes(4, byteorder = sys.byteorder, signed = True) +
      vk.to_bytes(4, byteorder = sys.byteorder, signed = True)
    )
  buf += flags.to_bytes(4, byteorder = sys.byteorder, signed = True)
  size = 24 + ctypes.sizeof(ctypes.c_void_p)
  buf += ((size - len(buf)) * b'\x00')  
  import ctypes
  buf = ctypes.create_string_buffer(buf)
  _call('User32', 'SendInput', 1, ctypes.byref(buf), size)

def _emit_mouse(code, value):
  if code == MOUSE_X:
    return _send_input(mouse_x = value)
  if code == MOUSE_Y:
    return _send_input(mouse_y = value)
  _send_input(mouse_data = value, flags = _mouse_wheel_map[code])

def _emit_keyboard(code, value):
  _send_input(vk = _vk_key_map[code],
              flags = 0 if value else _KEYEVENTF_KEYUP)

def emit(_type, code, value, sync = True, device = None):
  if device is None:
    if is_gamepad_event(_type, code):
      device = setup_virtual_gamepad()
      is_mouse_and_keyboard = False
    else:
      device = setup_virtual_mouse_and_keyboard()
      is_mouse_and_keyboard = True
  else:
    import io
    is_mouse_and_keyboard = type(device) is io.BytesIO
  if is_mouse_and_keyboard and _type == MOUSE:
    return _emit_mouse(code, value)
  if is_mouse_and_keyboard and _type == KEY:
    return _emit_keyboard(code, value)
  # TODO emit via VigemClient
  raise NotImplementedError()

def grab_exclusive_access(device):
  try:
    device.fh = _open(device.fh.name, exclusive = True)
    return True
  except OSError:
    return False

def release_exclusive_access(device):
  try:
    device.fh = _open(device.fh.name, exclusive = False)
    return True
  except OSError:
    return False

def set_rgb(device, color):
  # TODO
  return False

def rumble(device,
           duration,
           magnitude = 100,
           kind = FF_PERIODIC,
           effect_id = None,
           direction = FF_DIRECTION_DOWN,
           trigger_button = 0,
           trigger_interval = 0,
           replay_length = None,
           replay_delay = 0,
           attack_length = 0,
           attack_level = 0,
           fade_length = 0,
           fade_level = 0,
           strong_magnitude = None,
           weak_magnitude = None,
           waveform = FF_SINE,
           period = 0.1,
           offset = 0,
           phase = 0,
           load_effect = True,
           start_effect = True,
           stop_effect = False,
           remove_effect = True,
           loop_to_fill_duration = True,
           max_duration = 5):
  # TODO
  return None

def find_desktops(uid = None, user = None):
  # TODO find via EnumWindowStationsW and EnumDesktopsW
  return []

def start_gui_app(cmd,
                  env = None,
                  stdout = None,
                  stderr = None,
                  runtime_dir_roots = ('/run/user',),
                  display = None,
                  desktop = None,
                  qt_platform = None,
                  user = None):
  env = dict(os.environ if env is None else env)
  if qt_platform:
    env['QT_QPA_PLATFORM'] = qt_platform
  if not desktop:
    desktop = 
  if type(cmd) is str:
    cmd = [cmd]
  # TODO run as user on given desktop

def get_lit_leds(name, root = None):
  if (vk := _led_map.get(name)) is None:
    return []
  state = _call('User32', 'GetKeyState', vk[1])
  return [vk[0]] if state & 1 else []

__all__ = list(filter(lambda i: i[0] != '_' and i not in _exclude,
                      locals().keys()))

# TODO move to own module (login)

def get_processes():
  import re, subprocess
  out = subprocess.check_output('tasklist').decode().strip().splitlines()
  columns = re.split(r'\s{2,}', out[0])
  return [{columns[idx]: i for idx, i in enumerate(re.split(r'\s{2,}', line))}
          for line in out[2:]]

_login_ui = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI'
_password_provider = '{60B78E88-EAD8-445C-9CFD-0B87F74EA6CD}'
_pin_provider = '{D6886603-9D2F-4EB2-B667-1971041FA96B}'

def login(user = None, password = None, pin = None):
  import time
  start = time.time()
  if password is None and pin is None:
    password = ''
  if user is None:
    sid = None
  else:
    try:
      sid = get_sid_for_user(user)
    except FileNotFoundError:
      return False
  procs = get_processes()
  proc_img = {i['Image Name'].lower() for i in procs}
  import subprocess
  if 'logonui.exe' in proc_img:
    sessions_to_close = ()
  else:
    if current_user is None:
      return True
    out = subprocess.check_output((
      'powershell', '-c', '(gcim Win32_Computersystem).UserName'
    ))
    current_user = out.decode().strip().partition('\\')[-1]
    if current_user == user:
      return True
    sessions_to_close = {
      int(i['Session#']) for i in
      filter(lambda i: any((k.lower().endswith('session name') and
                            v.lower().endswith('console') for k,v in i.items())
                          ), procs)
    }
    if not sessions_to_close:
      return False
  import winreg
  values_to_restore = {}
  try:
    key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE,
                            _login_ui,
                            access = winreg.KEY_ALL_ACCESS)
  except OSError:
    return False
  try:
    if sid:
      for i in ('LastLoggedOnUserSID', 'SelectedUserSID'):
        try:
          values_to_restore[i] = winreg.QueryValueEx(key, i)
        except FileNotFoundError:
          pass
        winreg.SetValueEx(key, i, None, winreg.REG_SZ, sid)
    prov = _pin_provider if password is None else _password_provider
    try:
      p = winreg.QueryValueEx(key, 'LastLoggedOnProvider')
      last_prov = p[0]
      values_to_restore['LastLoggedOnProvider'] = p
    except FileNotFoundError:
      last_prov = None
    if last_prov != prov:
      winreg.SetValueEx(key, 'LastLoggedOnProvider', None, winreg.REG_SZ, prov)
    for session in sessions_to_close:
      _call('Wtsapi32', 'WTSDisconnectSession', None, session, True)
    subprocess.run(('taskkill', '/f', '/im', 'logonui.exe'))
    while True:
      time.sleep(0.1)
      procs = {i['Image Name'].lower() for i in get_processes()}
      if 'logonui.exe' in procs:
        break
  finally:
    for k,v in values_to_restore.items():
      winreg.SetValueEx(key, k, None, v[1], v[0])
  delta = time.time() - start
  for _ in range(2):
    time.sleep(5 * delta)
    tap_key(ESC_KEY)
  time.sleep(5 * delta)
  if password is None:
    type_string(str(pin), delay = 0.5 * delta)
  else:
    type_string(password + '\n', delay = 0.5 * delta)
  return True



# TODO move to own module (wakelock)

_POWER_REQUEST_CONTEXT_VERSION = 0
_POWER_REQUEST_CONTEXT_SIMPLE_STRING = 1

PowerRequestDisplayRequired = 0
PowerRequestSystemRequired = 1
PowerRequestAwayModeRequired = 2
PowerRequestExecutionRequired = 3

_what_map = {
  'sleep': PowerRequestDisplayRequired | PowerRequestSystemRequired,
  'idle': PowerRequestDisplayRequired | PowerRequestSystemRequired,
}

class WakeLock(object):
  def __init__(self,
               who = 'Gamepadify',
               why = 'no reason given',
               what = 'idle:sleep',
               mode = 'block'):
    if type(what) is str:
      flags = 0
      for w in what.split(':'):
        flags |= _what_map.get(w, 0)
    else:
      flags = what
    buf = (
      _POWER_REQUEST_CONTEXT_VERSION.to_bytes(4,
                                              byteorder = sys.byteorder,
                                              signed = False) +
      _POWER_REQUEST_CONTEXT_SIMPLE_STRING.to_bytes(4,
                                              byteorder = sys.byteorder,
                                              signed = False)
    )
    import ctypes
    reason = ctypes.create_unicode_buffer(who + ': ' + why)
    pointer_size = ctypes.sizeof(ctypes.c_void_p)
    size = 16 + (2 * pointer_size)
    buf += ctypes.addressof(reason).to_bytes(pointer_size,
                                             byteorder = sys.byteorder,
                                             signed = False)
    buf += ((size - len(buf)) * b'\x00')
    buf = ctypes.create_string_buffer(buf)
    handle = _call('Kernel32', 'PowerCreateRequest', ctypes.byref(buf))
    self.handle = handle
    _call('Kernel32', 'PowerSetRequest', handle, flags)

  def __del__(self):
    _call('Kernel32', 'CloseHandle', self.handle)

def try_get_wakelock(**kwargs):
  try:
    return WakeLock(**kwargs)
  except (RuntimeError, AttributeError):
    return None
