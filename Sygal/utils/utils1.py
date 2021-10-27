import sys

def is_devmode():
  t = 'pydevd' in sys.modules
  return t
