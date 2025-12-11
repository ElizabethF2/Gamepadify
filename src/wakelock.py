import sys, os, ctypes, ctypes.util

SD_BUS_TYPE_UNIX_FD = 104

class sd_bus_error(ctypes.Structure):
  _fields_ = [
    ('name', ctypes.c_char_p),
    ('message', ctypes.c_char_p),
    ('_', 100 * ctypes.c_void_p),
  ]

class WakeLock(object):
  def __init__(self,
               who = 'Gamepadify',
               why = 'no reason given',
               what = 'idle:sleep',
               mode = 'block'):
    libsystemd = ctypes.CDLL(ctypes.util.find_library('systemd'))
    self.libsystemd = libsystemd
    bus = ctypes.c_void_p(None)
    self.bus = bus
    reply = ctypes.c_void_p(None)
    self.reply = reply
    try:
      r = libsystemd.sd_bus_open_system(ctypes.byref(bus))
      if r < 0:
        raise RuntimeError(r, 'Unable to open system bus')
      error = sd_bus_error()
      ctypes.memset(ctypes.addressof(error), 0, ctypes.sizeof(error))
      r = libsystemd.sd_bus_call_method(bus,
                                        b'org.freedesktop.login1',
                                        b'/org/freedesktop/login1',
                                        b'org.freedesktop.login1.Manager',
                                        b'Inhibit',
                                        ctypes.byref(error),
                                        ctypes.byref(reply),
                                        b'ssss',
                                        what.encode(),
                                        who.encode(),
                                        why.encode(),
                                        mode.encode())
      libsystemd.sd_bus_error_free(ctypes.byref(error))
      if r < 0:
        raise RuntimeError(r, 'Unable to call inhibit')
      fd = ctypes.c_uint()
      if hasattr(sys, 'pypy_version_info'):
        sd_bus_type = ctypes.c_uint(SD_BUS_TYPE_UNIX_FD)
      else:
        sd_bus_type = ctypes.c_byte(SD_BUS_TYPE_UNIX_FD)
      r = libsystemd.sd_bus_message_read_basic(reply,
                                               sd_bus_type,
                                               ctypes.byref(fd))
      if r < 0:
        raise RuntimeError(r, 'Unable to read inhibit reply')
    except:
      self.__del__()
      raise

  def __del__(self):
    libsystemd = self.libsystemd
    libsystemd.sd_bus_message_unref(self.reply)
    libsystemd.sd_bus_flush_close_unref(self.bus)

def try_get_wakelock(**kwargs):
  try:
    return WakeLock(**kwargs)
  except (RuntimeError, AttributeError):
    return None
