import os, re, subprocess, json

SDDM_CONFD = '/etc/sddm.conf.d'

def get_sessions(user = None):
  out = subprocess.check_output(('loginctl', 'list-sessions', '-j'))
  js = json.loads(out)
  if not user:
    return js
  return list(filter(lambda i: (i.get('user') == user and
                                i.get('class') == 'user'), js))

def try_unlock(user):
  for session in get_sessions(user = user):
    ident = session.get('session')
    subprocess.check_call(('loginctl', 'unlock-session', ident))
    return True
  return False

def try_login(user, session = 'plasma', poll_delay = 1):
  entries = (
    ('Relogin', 'true'),
    ('Session', session),
    ('User', user),
  )
  try:
    for c in os.listdir(SDDM_CONFD):
      path = os.path.join(SDDM_CONFD, c)
      with open(path, 'r') as f:
        conf = f.read()
      if '[Autologin]' not in conf:
        continue
      missing_entry = False
      for k,v in entries:
        if '\n'+k+'=' not in conf:
          missing_entry = True
        conf = re.sub('\n'+k+'=.*', '\n'+k+'='+v, conf)
      if missing_entry:
        continue
      import tempfile
      tf = tempfile.NamedTemporaryFile(mode = 'w', prefix = 'sddm_conf_')
      tf.write(conf)
      tf.flush()
      os.chmod(tf.fileno(), os.stat(path).st_mode)
      subprocess.check_call(('mount', '--bind', tf.name, path))
      subprocess.check_call((
        'systemctl', 'restart', 'display-manager.service'
      ))
      import time
      while True:
        time.sleep(poll_delay)
        if len(get_sessions(user = user)) > 0:
          subprocess.check_call(('umount', path))
          tf.close()
          return True
  except FileNotFoundError:
    pass
  return False

def try_login_or_unlock(user, **kwargs):
  if try_unlock(user):
    return True
  return try_login(user, **kwargs)
