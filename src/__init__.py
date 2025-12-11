import sys, os, threading
_exclude = set(locals().keys())

IN_CREATE = 0x00000100
INPUT_PATH = '/dev/input'
UINPUT_PATH = '/dev/uinput'
INOTIFY_BUF_SIZE = 32
MAX_MOUSE_ACCELERATION = 999999

UINPUT_PREFIX = b'\x03\x00\x11\x22\x33\x44\x00\x00'
UINPUT_MOUSE_AND_KEYBOARD_NAME = 'gamepadify_virtual_mouse_and_keyboard'
UINPUT_GAMEPAD_NAME = 'gamepadify_virtual_gamepad'
UINPUT_MAX_NAME_SIZE = 80
UINPUT_SETUP_SIZE = UINPUT_MAX_NAME_SIZE + 12
UINPUT_CACHE_PREFIX = '_cached_uinput_fd_'

DEFAULT_NAMES_OF_INTEREST = '.*Controller.*|.*Gamepad.*'

CROSS = 304
CIRCLE = 305
TRIANGLE = 307
SQUARE = 308

A_BUTTON = CROSS
B_BUTTON = CIRCLE
X_BUTTON = 306
Y_BUTTON = TRIANGLE

L1 = 310
R1 = 311
L2 = 312
R2 = 313

LB_BUTTON = 308
RB_BUTTON = 309

LT_AXIS = 2
RT_AXIS = 5

L3 = 317
R3 = 318

LSTICK_BUTTON = 312
RSTICK_BUTTON = 313

SHARE = 314
OPTIONS = 315
PS_HOME = 316

SELECT_BUTTON = 310
START_BUTTON = 311
GUIDE_BUTTON = 139

DPAD_X = 16
DPAD_Y = 17

LSTICK_X = 0
LSTICK_Y = 1
RSTICK_X = 3
RSTICK_Y = 4

MIN_BUTTON = CROSS
MAX_BUTTON = R3

ARROW_UP = 103
ARROW_DOWN = 108
ARROW_LEFT = 105
ARROW_RIGHT = 106

ESC_KEY = 1
NUMBER_1_KEY = 2
NUMBER_2_KEY = 3
NUMBER_3_KEY = 4
NUMBER_4_KEY = 5
NUMBER_5_KEY = 6
NUMBER_6_KEY = 7
NUMBER_7_KEY = 8
NUMBER_8_KEY = 9
NUMBER_9_KEY = 10
NUMBER_0_KEY = 11
MINUS_KEY = 12
EQUALS_KEY = 13
BACKSPACE_KEY = 14
TAB_KEY = 15
Q_KEY = 16
W_KEY = 17
E_KEY = 18
R_KEY = 19
T_KEY = 20
Y_KEY = 21
U_KEY = 22
I_KEY = 23
O_KEY = 24
P_KEY = 25
LEFT_BRACKET_KEY = 26
RIGHT_BRACKET_KEY = 27
ENTER_KEY = 28
LEFT_CTRL = 29
RIGHT_CTRL = 97
A_KEY = 30
S_KEY = 31
D_KEY = 32
F_KEY = 33
G_KEY = 34
H_KEY = 35
J_KEY = 36
K_KEY = 37
L_KEY = 38
SEMICOLON_KEY = 39
APOSTROPHE_KEY = 40
BACKSLASH_KEY = 43
LEFT_SHIFT = 42
RIGHT_SHIFT = 54
Z_KEY = 44
X_KEY = 45
C_KEY = 46
V_KEY = 47
B_KEY = 48
N_KEY = 49
M_KEY = 50
COMMA_KEY = 51
PERIOD_KEY = 52
SLASH_KEY = 53
GRAVE_KEY = 41
LEFT_ALT = 56
RIGHT_ALT = 100
SPACE_KEY = 57
CAPSLOCK_KEY = 58
LEFT_META = 125
RIGHT_META = 126

HOME_KEY = 102
END_KEY = 107
DELETE_KEY = 111
PAGE_UP_KEY = 104
PAGE_DOWN_KEY = 109

F1_KEY = 59
F2_KEY = 60
F3_KEY = 61
F4_KEY = 62
F5_KEY = 63
F6_KEY = 64
F7_KEY = 65
F8_KEY = 66
F9_KEY = 67
F10_KEY = 68
F11_KEY = 87
F12_KEY = 88
F13_KEY = 183
F14_KEY = 184
F15_KEY = 185
F16_KEY = 186
F17_KEY = 187
F18_KEY = 188
F19_KEY = 189
F20_KEY = 190
F21_KEY = 191
F22_KEY = 192
F23_KEY = 193
F24_KEY = 194

LEFT_MOUSE = 0x110
RIGHT_MOUSE = 0x111
MIDDLE_MOUSE = 0x112

# TODO constants for other gamepads

EV_SYN = 0
EV_KEY = 1
EV_REL = 2
EV_ABS = 3
EV_MSC = 4
EV_LED = 0x11
EV_FF  = 0x15

REL_X = 0
REL_Y = 1
REL_HWHEEL = 6
REL_WHEEL = 8

KEY = EV_KEY
BUTTON = EV_KEY
STICK = EV_ABS
DPAD = EV_ABS
MOUSE = EV_REL
MOUSE_X = REL_X
MOUSE_Y = REL_Y
MOUSE_WHEEL = REL_WHEEL

CONNECTED = 'CONNECTED'
DISCONNECTED = 'DISCONNECTED'
DEVICE_IDLE = 'DEVICE_IDLE'
TICK = 'TICK'

SYN_REPORT = 0

EVIOCGNAME = 0x80004506
EVIOCGUNIQ = 0x80004508

EVIOCGRAB = 0x40044590
EVIOCREVOKE = 0x40044591

EVIOCSFF = 0x40304580
EVIOCRMFF = 0x40044581

FF_RUMBLE = 80
FF_PERIODIC = 81
FF_CONSTANT = 82

FF_GAIN = 96

FF_SQUARE = 88
FF_TRIANGLE = 89
FF_SINE = 90
FF_SAW_UP = 91
FF_SAW_DOWN = 92
FF_CUSTOM = 93

FF_DIRECTION_DOWN = 0x0
FF_DIRECTION_UP = 0x8000
FF_DIRECTION_LEFT = 0x4000
FF_DIRECTION_RIGHT = 0xC000

MAX_FF_DURATION = 32.767

UI_SET_EVBIT = 0x40045564
UI_SET_KEYBIT = 0x40045565
UI_SET_RELBIT = 0x40045566
UI_SET_ABSBIT = 0x40045567
UI_DEV_SETUP = 0x405c5503
UI_DEV_CREATE = 0x5501

MIN_KEY = 1
MAX_KEY = 0x2FF

KEYMAP = {
  'Esc': ESC_KEY,
  '1': NUMBER_1_KEY,
  '2': NUMBER_2_KEY,
  '3': NUMBER_3_KEY,
  '4': NUMBER_4_KEY,
  '5': NUMBER_5_KEY,
  '6': NUMBER_6_KEY,
  '7': NUMBER_7_KEY,
  '8': NUMBER_8_KEY,
  '9': NUMBER_9_KEY,
  '0': NUMBER_0_KEY,
  '-': MINUS_KEY,
  '=': EQUALS_KEY,
  'Back': BACKSPACE_KEY,
  '\b': BACKSPACE_KEY,
  'Tab': TAB_KEY,
  '\t': TAB_KEY,
  'q': Q_KEY,
  'w': W_KEY,
  'e': E_KEY,
  'r': R_KEY,
  't': T_KEY,
  'y': Y_KEY,
  'u': U_KEY,
  'i': I_KEY,
  'o': O_KEY,
  'p': P_KEY,
  '[': LEFT_BRACKET_KEY,
  ']': RIGHT_BRACKET_KEY,
  'Enter': ENTER_KEY,
  '\n': ENTER_KEY,
  'a': A_KEY,
  's': S_KEY,
  'd': D_KEY,
  'f': F_KEY,
  'g': G_KEY,
  'h': H_KEY,
  'j': J_KEY,
  'k': K_KEY,
  'l': L_KEY,
  ';': SEMICOLON_KEY,
  '\'': APOSTROPHE_KEY,
  '\\': BACKSLASH_KEY,
  'z': Z_KEY,
  'x': X_KEY,
  'c': C_KEY,
  'v': V_KEY,
  'b': B_KEY,
  'n': N_KEY,
  'm': M_KEY,
  ',': COMMA_KEY,
  '.': PERIOD_KEY,
  '/': SLASH_KEY,
  '`': GRAVE_KEY,
  'Space': SPACE_KEY,
  ' ': SPACE_KEY,
  'F1': F1_KEY,
  'F2': F2_KEY,
  'F3': F3_KEY,
  'F4': F4_KEY,
  'F5': F5_KEY,
  'F6': F6_KEY,
  'F7': F7_KEY,
  'F8': F8_KEY,
  'F9': F9_KEY,
  'F10': F10_KEY,
  'F11': F11_KEY,
  'F12': F12_KEY,
  'F13': F13_KEY,
  'F14': F14_KEY,
  'F15': F15_KEY,
  'F16': F16_KEY,
  'F17': F17_KEY,
  'F18': F18_KEY,
  'F19': F19_KEY,
  'F20': F20_KEY,
  'F21': F21_KEY,
  'F22': F22_KEY,
  'F23': F23_KEY,
  'F24': F24_KEY,
  'PgUp': PAGE_UP_KEY,
  'PgDn': PAGE_DOWN_KEY,
  'Del': DELETE_KEY,
  'Home': HOME_KEY,
  '\r': HOME_KEY,
  'End': END_KEY,
}

SHIFTED_KEYS = {
  '!': '1',
  '@': '2',
  '#': '3',
  '$': '4',
  '%': '5',
  '^': '6',
  '&': '7',
  '*': '8',
  '(': '9',
  ')': '0',
  '_': '-',
  '+': '=',
  '{': '[',
  '}': ']',
  ':': ';',
  '"': "'",
  '<': ',',
  '>': '.',
  '|': '\\',
  '?': '/',
  '~': '`',
}

PERPENDICULAR_AXIS = {
  LSTICK_X: LSTICK_Y,
  LSTICK_Y: LSTICK_X,
  RSTICK_X: RSTICK_Y,
  RSTICK_Y: RSTICK_X,
}

class Device(object):
  def __init__(self, path, name, uid, fh):
    self.path = path
    self.name = name
    self.uid = uid
    self.fh = fh
    self.held_buttons = set()
    self.axis = {}

class ControllerEvent(object):
  def __init__(self, device, ts, kind, name, value):
    self.device = device
    self.time = ts
    self.kind = kind
    self.name = name
    self.value = value

  def __repr__(self):
    return (f'ControllerEvent(kind={self.kind}, ' +
                            f'name={self.name}, ' +
                            f'value={self.value})')

_lock = threading.Lock()
_internal_state = {}

def _setup_virtual_input_with_lock(ename, bits):
  import fcntl
  uinput_fd = open(UINPUT_PATH, 'wb', buffering = False)
  for k, v in (bits or {}).items():
    for i in v:
      fcntl.ioctl(uinput_fd, k, i)
  setup_buf = (
    UINPUT_PREFIX + 
    ename + 
    (b'\x00' * (UINPUT_SETUP_SIZE - len(UINPUT_PREFIX)))
  )
  fcntl.ioctl(uinput_fd, UI_DEV_SETUP, setup_buf)
  fcntl.ioctl(uinput_fd, UI_DEV_CREATE)
  return uinput_fd

def setup_virtual_input(name, use_cache = True, cache_to = None, bits = None):
  if use_cache:
    if cache_to is None:
      cache_to = _internal_state.setdefault('uinput_cache', {})
    elif type(cache_to) is ControllerEvent:
      cache_to = cache_to.device
    if type(cache_to) is Device:
      cache_to = _internal_state[cache_to.name,
                                 cache_to.uid].setdefault('uinput_cache', {})
    cache_key = UINPUT_CACHE_PREFIX + name
    if (uinput_fd := cache_to.get(cache_key)) is not None:
      return uinput_fd
  ename = name.encode()
  if len(ename) >= UINPUT_MAX_NAME_SIZE:
    raise ValueError('Name {} too long'.format(repr(name)))
  with _lock:
    if not use_cache or (uinput_fd := cache_to.get(cache_key)) is None:
      uinput_fd = _setup_virtual_input_with_lock(ename, bits)
      if use_cache:
        cache_to[cache_key] = uinput_fd
    return uinput_fd

def setup_virtual_mouse_and_keyboard(name = UINPUT_MOUSE_AND_KEYBOARD_NAME,
                                     use_cache = True,
                                     cache_to = None):
  return setup_virtual_input(name, use_cache = use_cache, cache_to = cache_to,
    bits = {
      UI_SET_EVBIT: (EV_KEY, EV_REL),
      UI_SET_KEYBIT: tuple(range(MIN_KEY, MAX_KEY + 1)),
      UI_SET_RELBIT: (MOUSE_X, MOUSE_Y, MOUSE_WHEEL),
    }
  )

def setup_virtual_gamepad(name = UINPUT_GAMEPAD_NAME,
                          use_cache = True,
                          cache_to = None):
  return setup_virtual_input(name, use_cache = use_cache, cache_to = cache_to,
    bits = {
      UI_SET_EVBIT: (EV_KEY, EV_ABS),
      UI_SET_KEYBIT: tuple(range(MIN_BUTTON, MAX_BUTTON + 1)),
      UI_SET_ABSBIT: (
        LSTICK_X, LSTICK_Y,
        RSTICK_X, RSTICK_Y,
        DPAD_X, DPAD_Y,
      ),
    }
  )

def is_gamepad_event(_type, code):
  if _type in (EV_ABS, EV_FF):
    return True
  if _type == EV_KEY and code >= MIN_BUTTON and code <= MAX_BUTTON:
    return True
  return False

def emit(_type, code, value, sync = True, device = None):
  if device is None:
    if is_gamepad_event(_type, code):
      device = setup_virtual_gamepad()
    else:
      device = setup_virtual_mouse_and_keyboard()
  buf = 16 * b'\x00'
  buf += _type.to_bytes(2, byteorder = sys.byteorder, signed = False)
  buf += code.to_bytes(2, byteorder = sys.byteorder, signed = False)
  buf += value.to_bytes(4,
                        byteorder = sys.byteorder,
                        signed = _type in (EV_ABS, EV_REL))
  os.write(device if type(device) is int else device.fileno(), buf)
  if sync and _type != EV_SYN:
    emit(EV_SYN, SYN_REPORT, 0, device = device)
  return True

def stop_listening_to_device(device):
  _internal_state[device.name, device.uid]['connected'] = False

def disconnect_controller(uid):
  import subprocess
  try:
    proc = subprocess.run(('bluetoothctl', 'disconnect', uid),
                          capture_output = True)
    ret = (proc.returncode == 0)
  except FileNotFoundError:
    ret = False
  return ret

def handle_controllers(callback,
                       ignore_existing = False,
                       ignore_new = False,
                       sync_axis = True,
                       names_of_interest = DEFAULT_NAMES_OF_INTEREST,
                       idle_timeout = None,
                       controller_timeout = None):
  if not ignore_new:
    import ctypes, ctypes.util
    libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno = True)
    fd = libc.inotify_init()
    if fd == -1:
      raise OSError(ctypes.get_errno())
  try:
    if not ignore_new:
      wd = libc.inotify_add_watch(fd, INPUT_PATH.encode(), IN_CREATE)
      if wd == -1:
        raise OSError(ctypes.get_errno())
    if not ignore_existing:
      for name in os.listdir(INPUT_PATH):
        path = os.path.join(INPUT_PATH, name)
        if name[:5] == 'event' and name[5:].isdigit():
          callback(path,
                   sync_axis = sync_axis,
                   names_of_interest = names_of_interest,
                   timeout = idle_timeout)
    if not ignore_new:
      if controller_timeout is not None:
        import select
        ep = select.epoll(1)
        ep.register(fd, select.EPOLLIN)
        _internal_state.setdefault('device_last_seen', 0)
      while True:
        try:
          if controller_timeout is not None:
            remaining = min(controller_timeout,
                            __import__('time').time() -
                            _internal_state['device_last_seen'])
            if len(ep.poll(timeout = controller_timeout)) < 1:
              if count_devices() > 0:
                continue
              break
          buf = os.read(fd, INOTIFY_BUF_SIZE)
        except KeyboardInterrupt:
          break
        name = buf[16:buf.find(0, 16)].decode()
        if name[:5] == 'event' and name[5:].isdigit():
          callback(os.path.join(INPUT_PATH, name),
                   sync_axis = sync_axis,
                   names_of_interest = names_of_interest,
                   timeout = idle_timeout)
  finally:
    if not ignore_new:
      os.close(fd)
      if controller_timeout is not None:
        ep.close()

def wait_for_controllers(callback, **kwargs):
  kwargs.setdefault('ignore_new', False)
  handle_controllers(callback, **kwargs)

def _get_ioctl(fh, cmd, buflen = 256):
  buf = bytearray(buflen)
  try:
    import fcntl
    fcntl.ioctl(fh, cmd | (buflen << 16), buf)
  except FileNotFoundError:
    return None
  buf = buf.decode()
  return buf[:buf.find('\x00')]

def _cleanup_device(device = None):
  exists = False
  device_count = 0
  with _lock:
    if device:
      intd = _internal_state.pop((device.name, device.uid))
    for k in _internal_state.keys():
      if type(k) is tuple:
        device_count += 1
        if device and k[1] == device.uid:
          exists = True
    if device and not exists:
      _internal_state.get('controller_local', {}).pop(device.uid, None)
      if not _internal_state.get('controller_local'):
        _internal_state.pop('controller_local', None)
      if device_count < 1:
        if (osk_proc := _internal_state.pop('osk_proc', None)):
          osk_proc.terminate()
        _internal_state.pop('uinput_cache', None)
        if mevt := intd.get('mouse_event'):
          intd['disconnected'] = True
          mevt.set()
          if mwt := intd.get('mouse_worker_thread'):
            mwt.join()
        if 'device_last_seen' in _internal_state:
          _internal_state['device_last_seen'] = __import__('time').time()
      __import__('gc').collect()
  return device_count

def count_devices():
  return _cleanup_device()

def _event_handler_thread(queue, callback):
  while True:
    event = queue.get()
    callback(event)
    if event.kind == DISCONNECTED:
      break

def wait_for_input_events(path,
                          callback,
                          sync_axis = True,
                          names_of_interest = DEFAULT_NAMES_OF_INTEREST,
                          timeout = None):
  try:
    fh = open(path, 'rb+', buffering = False)
  except FileNotFoundError:
    return
  with fh:
    dname = _get_ioctl(fh, EVIOCGNAME)
    if not __import__('re').match(names_of_interest, dname):
      return
    uid = _get_ioctl(fh, EVIOCGUNIQ)
    device = Device(path, dname, uid, fh)
    if sync_axis:
      enqued_events = []
    if timeout is not None:
      import select
      ep = select.epoll(1)
      ep.register(fh, select.EPOLLIN)
    try:
      with _lock:
        intd = {'connected': True}
        _internal_state[dname, uid] = intd
      import queue
      q = queue.Queue()
      q.put(ControllerEvent(device, None, CONNECTED, None, None))
      callback_thread = threading.Thread(
        target = _event_handler_thread,
        args = (q, callback),
        daemon = True
      )
      callback_thread.start()
      while intd['connected']:
        if timeout is not None and len(ep.poll(timeout = timeout)) < 1:
          q.put(ControllerEvent(device, None, DEVICE_IDLE, None, None))
        else:
          try:
            buf = fh.read(24)
          except OSError as err:
            if err.errno == __import__('errno').ENODEV:
              intd['connected'] = False
              break
            else:
              raise err
          if not buf:
            break
          ts = int.from_bytes(buf[0:8],
                              byteorder = sys.byteorder,
                              signed = False)
          m = int.from_bytes(buf[8:16],
                             byteorder = sys.byteorder,
                             signed = False)
          ts += (0.000001 * m)
          _type = int.from_bytes(buf[16:18],
                                 byteorder = sys.byteorder,
                                 signed = False)
          code = int.from_bytes(buf[18:20],
                                byteorder = sys.byteorder,
                                signed = False)
          value = int.from_bytes(buf[20:],
                                 byteorder = sys.byteorder,
                                 signed = _type == EV_ABS)
          if _type == EV_KEY:
            if value:
              device.held_buttons.add(code)
            else:
              try:
                device.held_buttons.remove(code)
              except KeyError:
                pass
            q.put(ControllerEvent(device, ts, _type, code, value))
          elif _type in (EV_ABS, EV_REL):
            device.axis[code] = value
            event = ControllerEvent(device, ts, _type, code, value)
            if sync_axis:
              enqued_events.append(event)
            else:
              q.put(event)
          elif _type == EV_SYN and code == SYN_REPORT and sync_axis:
            if enqued_events:
              for event in enqued_events:
                q.put(event)
              enqued_events = []
            else:
              q.put(ControllerEvent(device, ts, TICK, None, None))
          else:
            q.put(ControllerEvent(device, ts, TICK, None, None))
      q.put(ControllerEvent(device, None, DISCONNECTED, None, None))
      callback_thread.join()
    finally:
      _cleanup_device(device = device)
      if timeout is not None:
        ep.close()

def _controller_connected_callback(path, callback, **kwargs):
  t = threading.Thread(target = wait_for_input_events,
                       args = (path, callback),
                       kwargs = kwargs,
                       daemon = True)
  t.start()

def device_local(device):
  intd = _internal_state[device.name, device.uid]
  return intd.setdefault('device_local', {})

def controller_local(device):
  cl = _internal_state.get('controller_local')
  if cl is None:
    with _lock:
      cl = _internal_state.setdefault('controller_local', {})
      return cl.setdefault(device.uid, {})
  if (intd := cl.get(device.uid)) is not None:
    return intd
  with _lock:
    return cl.setdefault(device.uid, {})

def _mouse_worker(intd, frequency, mevt):
  delay = 1.0/frequency
  spx = 1
  spy = 1
  spvw = 1
  i = 0
  while not intd.get('disconnected'):
    xd = intd.get('mouse_x_delta', 0)
    yd = intd.get('mouse_y_delta', 0)
    vwd = intd.get('mouse_vw_delta', 0)

    if xd != 0 and (i % intd['mouse_x_skip']) == 0:
        spx = min(spx * intd['mouse_x_acceleration'], MAX_MOUSE_ACCELERATION)
        emit(EV_REL,
             MOUSE_X,
             (-1 if xd < 0 else 1) *
               min(abs(intd['mouse_x_max_speed']), round(abs(xd) * spx)))
    else:
      spx = 1
    if yd != 0 and (i % intd['mouse_y_skip']) == 0:
        spy = min(spy * intd['mouse_y_acceleration'], MAX_MOUSE_ACCELERATION)
        emit(EV_REL,
            MOUSE_Y,
            (-1 if yd < 0 else 1) *
              min(abs(intd['mouse_y_max_speed']), round(abs(yd) * spy)))
    else:
      spy = 1
    if vwd != 0 and (i % intd['mouse_vw_skip']) == 0:
      spvw = min(spvw * intd['mouse_vw_acceleration'], MAX_MOUSE_ACCELERATION)
      emit(EV_REL,
           MOUSE_WHEEL,
           (-1 if vwd < 0 else 1) *
             min(abs(intd['mouse_vw_max_speed']), round(abs(vwd) * spvw)))
    else:
      spvw = 1
    if xd == 0 and yd == 0 and vwd == 0:
      mevt.wait()
      mevt.clear()
    else:
      __import__('time').sleep(delay)
    
    i += 1
    if i == frequency:
      i = 0

def remap(mappings,
          event,
          deadzone = 0,
          initial_speed = 1000,
          max_speed = 10000,
          acceleration = 1.01,
          frequency = 100,
          skip_ratio = 0,
          stick_center = 127.5,
          perpendicular_axis = PERPENDICULAR_AXIS):
  dev = event.device
  dname = dev.name
  ekind = event.kind
  ename = event.name
  mapping = mappings.get((dname, ekind, ename))
  if not mapping:
    return False
  handled = False
  intd = _internal_state[dname, dev.uid]
  kind = mapping.get('kind')
  if kind == KEY:
    if ekind == EV_KEY:
      code = mapping.get('key')
      if code is None:
        return False
      value = 1 if event.value else 0
      return emit(EV_KEY, code, value)
    elif ekind == EV_ABS:
      evalue = event.value
      dz = mapping.get('deadzone', deadzone)
      if evalue <= -dz:
        code = mapping.get('negative_key')
        if code:
          return emit(EV_KEY, code, 1)
      elif evalue >= dz:
        code = mapping.get('positive_key')
        if code:
          return emit(EV_KEY, code, 1)
      else:
        # TODO spurious - may release an actually held key
        for i in ('negative_key', 'positive_key'):
          code = mapping.get(i)
          if code:
            emit(EV_KEY, code, 0)
        return True
  elif kind == MOUSE:
    axis = mapping.get('axis')
    if ekind == EV_ABS:
      if axis == MOUSE_X:
        kd = 'mouse_x_delta'
        ka = 'mouse_x_acceleration'
        km = 'mouse_x_max_speed'
        ks = 'mouse_x_skip'
      elif axis == MOUSE_Y:
        kd = 'mouse_y_delta'
        ka = 'mouse_y_acceleration'
        km = 'mouse_y_max_speed'
        ks = 'mouse_y_skip'
      elif axis == MOUSE_WHEEL:
        kd = 'mouse_vw_delta'
        ka = 'mouse_vw_acceleration'
        km = 'mouse_vw_max_speed'
        ks = 'mouse_vw_skip'
      else:
        return False
      old = intd.get(kd)
      dz = mapping.get('deadzone', deadzone)
      sc = mapping.get('stick_center', stick_center)
      isp = mapping.get('initial_speed', initial_speed)
      msp = mapping.get('max_speed', max_speed)
      accel = mapping.get('acceleration', acceleration)
      sr = mapping.get('skip_ratio', skip_ratio)
      bound = mapping.get('bound', 0)
      rng = abs(sc - bound)
      v = event.value - sc
      if abs(v) < dz:
        v = 0
      v /= rng
      paxis = perpendicular_axis.get(axis)
      if paxis is not None:
        pv = dev.axis.get(paxis, 0)
        pv = (pv - sc) / rng
        intd[ks] = max(round(sr * ((frequency * (1 - ((v*v)+(pv*pv)))))), 1) \
                    if v != 0 else 1
      else:
        intd[ks] = max(round(sr * ((frequency * (1 - abs(v))))), 1) \
                    if v != 0 else 1
      v = round(v * isp)
      intd[kd] = v
      intd[ka] = accel
      intd[km] = msp
      if old == v:
        return True
      if (mevt := intd.get('mouse_event')) and v != 0:
        mevt.set()
        return True
      with _lock:
        if mevt := intd.get('mouse_event'):
          return True
        mevt = threading.Event()
        intd['mouse_event'] = mevt
        t = threading.Thread(target = _mouse_worker,
                             args = (intd, frequency, mevt),
                             daemon = True)
        t.start()
        intd['mouse_worker_thread'] = t
        return True
    elif kind == STICK and ekind == STICK:
      emit(STICK, mapping['axis'], event.value)
    elif kind == STICK and ekind == BUTTON:
      sc = mapping.get('stick_center', stick_center)
      emit(STICK, mapping['axis'], 2 * sc)
    elif ekind == EV_KEY and event.value > 0:
      emit(EV_REL, axis, mapping.get('amount', 0))
      return True
  return False

def update_idle_timer(event,
                      mappings = None,
                      stick_center = 127.5,
                      deadzone = None,
                      auto_start_timer = True):
  device = event.device
  dname = device.name
  ekind = event.kind
  intd = _internal_state[dname, device.uid]
  ts = event.time
  last_interaction = intd.get('last_interaction')
  if last_interaction is None:
    if ts is not None and auto_start_timer:
      intd['last_interaction'] = ts
      return 0
    return None
  elif ts is None:
    return None
  delta = ts - last_interaction
  if mappings is None:
    mapping = {} if ekind in (STICK, BUTTON) else None
  else:
    mapping = mappings.get((dname, ekind, event.name))
  if mapping is None:
    return delta
  if ekind == STICK:
    sc = mapping.get('stick_center', stick_center)
    dz = mapping.get('deadzone', 0) if deadzone is None else deadzone
    v = (event.value - sc)
    if abs(v) <= dz:
      return delta
  elif ekind != BUTTON:
    return delta
  intd['last_interaction'] = ts
  return 0

def get_idle_time(event):
  if (ts := event.time) is None:
    return None
  device = event.device
  intd = _internal_state[device.name, device.uid]
  if (last_interaction := intd.get('last_interaction')) is None:
    return 0
  return ts - last_interaction

def is_idle(timeout,
            event,
            mappings = None,
            update_idle_timer = True,
            **kwargs):
  if update_idle_timer:
    idle_time = globals()['update_idle_timer'](event,
                                               mappings = mappings,
                                               **kwargs)
  else:
    idle_time = get_idle_time(event)
  if idle_time is not None and idle_time > timeout:
    return True
  if event.kind == DEVICE_IDLE:
    return True
  return False

def press_key(key, device = None):
  if type(key) is str:
    key = KEYMAP[key]
  emit(EV_KEY, key, 1, device = device)

def release_key(key, device = None):
  if type(key) is str:
    key = KEYMAP[key]
  emit(EV_KEY, key, 0, device = device)

def tap_key(key, duration = 0.25, device = None):
  press_key(key, device = device)
  __import__('time').sleep(duration)
  release_key(key, device = device)

press_button = press_key
release_button = release_key
tap_button = tap_key

def button_held(event, button):
  if event.kind != BUTTON:
    return False
  if event.name != button:
    return False
  return event.value

def button_released(event, button):
  if event.kind != BUTTON:
    return False
  if event.name != button:
    return False
  return not event.value

def type_string(s, duration = 0.25, delay = 0.1, device = None):
  for c in s:
    if (key := KEYMAP.get(c)) is not None:
      tap_key(key, duration = duration, device = device)
    elif (key := KEYMAP.get(c.lower())) is not None:
      press_key(LEFT_SHIFT, device = device)
      tap_key(key, duration = duration, device = device)
      release_key(LEFT_SHIFT, device = device)
    elif (key := SHIFTED_KEYS.get(c)) is not None:
      press_key(LEFT_SHIFT, device = device)
      tap_key(KEYMAP[key], duration = duration, device = device)
      release_key(LEFT_SHIFT, device = device)
    else:
      raise ValueError('Unable to type key(s) for {}'.format(repr(c)))
    __import__('time').sleep(delay)

def grab_exclusive_access(device):
  try:
    __import__('fcntl').ioctl(device.fh, EVIOCGRAB, 1)
    return True
  except OSError:
    return False

def release_exclusive_access(device):
  try:
    __import__('fcntl').ioctl(device.fh, EVIOCGRAB, 0)
    return True
  except OSError:
    return False

def evdev_to_hidraw_input(device,
                          hidraw_dir = '/sys/class/hidraw'):
  intd = _internal_state[device.name, device.uid]
  if (res := intd.get('hidraw_input')) is not None:
    return res
  with _lock:
    if (res := intd.get('hidraw_input')) is not None:
      return res
    evdev_name = os.path.basename(device.path)
    try:
      hdir = os.listdir(hidraw_dir)
    except FileNotFoundError:
      hdir = []
    for hr in hdir:
      dev_dir = os.path.join(hidraw_dir, hr, 'device')
      input_dir = os.path.join(dev_dir, 'input')
      try:
        for inp in os.listdir(input_dir):
          if evdev_name in os.listdir(os.path.join(input_dir, inp)):
            intd['hidraw_input'] = dev_dir, inp
            return dev_dir, inp
      except FileNotFoundError:
        pass
    intd['hidraw_input'] = None, None
    return None, None

def set_rgb(device, color):
  dev_dir, inp = evdev_to_hidraw_input(device)
  try:
    with open(os.path.join(dev_dir,
                           'leds',
                           inp+':rgb:indicator/multi_index'), 'r') as f:
      indicies = {k:v for k,v in enumerate(f.read().split())}
    if set(indicies.values()) == {'red', 'green', 'blue'}:
      color_map = {'red': color[0], 'green': color[1], 'blue': color[2]}
      with open(os.path.join(dev_dir,
                           'leds',
                           inp+':rgb:indicator/multi_intensity'), 'w') as f:
        f.write(' '.join(map(str, (color_map[indicies[i]] for i in range(3)))))
      return True
  except (FileNotFoundError, TypeError):
    pass
  try:
    for i, c in enumerate(('red', 'green', 'blue')):
      path = os.path.join(dev_dir, 'leds', inp+':'+c, 'brightness')
      with open(path, 'w') as f:
        f.write(str(color[i]))
    return True
  except (FileNotFoundError, TypeError):
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
  if effect_id is None:
    effect_id = -1
  max_duration = min(max_duration, MAX_FF_DURATION)
  capped_duration = min(duration, max_duration)
  if loop_to_fill_duration and duration > capped_duration:
    itr = duration / capped_duration
    ritr = round(itr)
    itr = (ritr + 1) if ritr < itr else ritr
    capped_duration = duration / itr
  else:
    itr = 1
  if replay_length is None:
    replay_length = round(1000 * capped_duration)
  buf = (
    kind.to_bytes(2, byteorder = sys.byteorder, signed = False) +
    effect_id.to_bytes(2, byteorder = sys.byteorder, signed = True) +
    b''.join((i.to_bytes(2,
                         byteorder = sys.byteorder,
                         signed = False) for i in (
      direction,
      trigger_button, trigger_interval,
      replay_length, round(1000 * replay_delay),
      0,
    )))
  )
  if kind == FF_RUMBLE:
    if strong_magnitude is None:
      strong_magnitude = magnitude
    if weak_magnitude is None:
      weak_magnitude = magnitude
    buf += b''.join((
      round((abs(i)*((2**16)-1))/100).to_bytes(2,
                                               byteorder = sys.byteorder,
                                               signed = False) for i in (
        strong_magnitude, weak_magnitude
    )))
  elif kind == FF_PERIODIC:
    if waveform == FF_CUSTOM:
      raise ValueError('FF_CUSTOM is not supported')
    buf += b''.join((i.to_bytes(2,
                                byteorder = sys.byteorder,
                                signed = s) for i,s in (
      (waveform, False),
      (round(1000 * period), False),
      (round((magnitude*((2**15)-1))/100), True),
      (round((offset*((2**15)-1))/100), True),
      (round(1000 * phase), False),      
    )))
  elif kind == FF_CONSTANT:
    buf += (round((magnitude*((2**15)-1))/100)
            .to_bytes(2, byteorder = sys.byteorder, signed = True))
  else:
    raise ValueError('Unsupported FF kind: {}'.format(kind))
  if kind in (FF_PERIODIC, FF_CONSTANT):
    if attack_length == 0:
      attack_level = magnitude
    if fade_length == 0:
      fade_level = magnitude
    buf += b''.join((i.to_bytes(2,
                                byteorder = sys.byteorder,
                                signed = False) for i in (
      round(1000 * min(attack_length, max_duration)),
      round((abs(attack_level)*((2**16)-1))/100),
      round(1000 * min(fade_length, max_duration)),
      round((abs(fade_level)*((2**16)-1))/100),
    )))
  buf = bytearray(buf + ((48 - len(buf)) * b'\x00'))
  device_read_fh = getattr(device, 'fh', device)
  if load_effect:
    try:
      __import__('fcntl').ioctl(device_read_fh, EVIOCSFF, buf)
    except OSError:
      return None
    effect_id = int.from_bytes(buf[2:4])
  ret = effect_id
  fh = getattr(device, 'fh', device)
  try:
    for _ in range(itr):
      if start_effect:
        emit(EV_FF, effect_id, 1, sync = False, device = fh)
      if capped_duration > 0 and start_effect and (stop_effect or remove_effect):
        __import__('time').sleep(capped_duration)
      if stop_effect:
        emit(EV_FF, effect_id, 0, sync = False, device = fh)
  except OSError:
    ret = None
  finally:
    if remove_effect:
      try:
        __import__('fcntl').ioctl(device_read_fh, EVIOCRMFF, effect_id)
      except OSError:
        return None
  return ret

def get_uid(user):
  if type(user) in (int, float):
    return int(user)
  if user.startswith('#'):
    return int(user[1:])
  for i in __import__('pwd').getpwall():
    if i.pw_name == user:
      return i.pw_uid
  return None

def get_user(uid_or_user):
  if type(uid_or_user) is str:
    if uid_or_user.startswith('#'):
      uid = int(uid_or_user[1:])
    else:
      return uid_or_user
  else:
    uid = uid_or_user
  for i in __import__('pwd').getpwall():
    if i.pw_uid == uid:
      return i.pw_name
  return None

def find_desktops(uid = None, user = None):
  # TODO
  return []

def find_x11_displays(uid = None, user = None):
  displays = []
  root = os.path.join(__import__('tempfile').gettempdir(), '.X11-unix')
  try:
    with os.scandir(root) as it:
      if uid is None and user is not None:
        uid = get_uid(user)
      for entry in it:
        if not entry.name.startswith('X'):
          continue
        if not (num := entry.name[1:]).isdigit():
          continue
        if uid is not None and entry.stat().st_uid != uid:
          continue
        if not __import__('stat').S_ISSOCK(entry.stat().st_mode):
          continue
        displays.append((int(num), ':' + num, entry))
  except FileNotFoundError:
    pass
  return [i[1:] for i in sorted(displays, key = lambda i: i[0])]

def find_xauthorities(uid = None, user = None, runtime_dir_roots = ('/run/user',)):
  if uid is None and user is not None:
    uid = get_uid(user)
  for root in runtime_dir_roots:
    try:
      f = os.listdir(root)
    except FileNotFoundError:
      f = []
    if uid is not None:
      try:
        f = f.remove(str(uid))
      except ValueError:
        pass
      f = [str(uid), *f]
    for u in f:
      try:
        with os.scandir(os.path.join(root, u)) as it:
          for entry in it:
            if not entry.name.startswith('xauth'):
              continue
            if uid is not None and entry.stat().st_uid != uid:
              continue
            yield entry
      except FileNotFoundError:
        pass

def start_gui_app(cmd,
                  env = None,
                  stdout = None,
                  stderr = None,
                  runtime_dir_roots = ('/run/user',),
                  display = None,
                  desktop = None,
                  qt_platform = 'xcb',
                  user = None):
  env = dict(os.environ if env is None else env)
  unset = object()
  uid = unset
  if xauth := env.get('XAUTHORITY'):
    try:
      uid = os.stat(xauth).st_uid
      if user is not None:
        uuser = get_user(uid)
        if user != uuser:
          uid = unset
          xauth = None
    except FileNotFoundError:
      xauth = None
  if not xauth:
    try:
      last_xauth = list(find_xauthorities(
        user = user,
        runtime_dir_roots = runtime_dir_roots
      ))[-1]
      env['XAUTHORITY'] = last_xauth.path
      uid = last_xauth.stat().st_uid
    except IndexError:
      pass
  if display:
    env['DISPLAY'] = display
  else:
    u = None if uid is unset else uid
    try:
      last_display = find_x11_displays(uid = u, user = user)[-1]
      env['DISPLAY'] = last_display[0]
    except IndexError:
      pass
  if qt_platform:
    env['QT_QPA_PLATFORM'] = qt_platform
  if type(cmd) is str:
    cmd = [cmd]
  if user is not None:
    if uid is unset:
      uid = get_uid(user)
    if uid is not None:
      which = __import__('shutil').which
      if (user := get_user(user)) and (runuser := which('runuser')):
        cmd = [runuser, '-u'+user, '--', *cmd]
      elif sudo := which('sudo'):
        cmd = [sudo, '-u', '#{}'.format(uid), *cmd]
      elif (user := get_user(user)) and (doas := which('doas')):
        cmd = [doas, '-u', user, *cmd]
  popen =__import__('subprocess').Popen
  return popen(cmd, env = env, stdout = stdout, stderr = stderr)

def toggle_osk(qt_platform = None,
               runtime_dir_roots = ('/run/user',),
               cmd = (sys.executable, '-m', 'gamepadify.osk'),
               env = None,
               stdout = None,
               stderr = None,
               user = None,
               display = None):
  with _lock:
    if (proc := _internal_state.pop('osk_proc', None)) and proc.poll() is None:
      proc.terminate()
    else:
      kw = {'qt_platform': qt_platform} if qt_platform else {}
      _internal_state['osk_proc'] = start_gui_app(
        cmd,
        runtime_dir_roots = runtime_dir_roots,
        display = display,
        env = env,
        stdout = stdout,
        stderr = stderr,
        **kw
      )

def get_lit_leds(name, root = '/sys/class/leds'):
  lit = []
  try:
    dirs = os.listdir(root)
  except FileNotFoundError:
    dirs = []
  for i in dirs:
    if name.lower() != i.split(':')[-1].lower():
      continue
    try:
      r = os.path.join(root, i)
      with open(os.path.join(r, 'brightness'), 'rb') as f:
        if int(f.read()) > 0:
          lit.append(r)
    except (FileNotFoundError, ValueError):
      pass
  return lit

def automatically_handle_controllers(callback, **kwargs):
  wait_for_controllers(
    lambda ct, cb=callback, **kw: _controller_connected_callback(ct, cb, **kw),
    **kwargs)

__all__ = list(filter(lambda i: i[0] != '_' and i not in _exclude,
                      locals().keys()))

if os.name == 'nt':
  from .nt import *

# TODO setup.py

