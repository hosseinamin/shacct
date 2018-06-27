import re
from os import environ
import os.path
from configparser import ConfigParser

config=None

class ShaactConfigParser(ConfigParser):
  aspath_pttrn01 = re.compile(r"\$([a-z_][0-9a-z_]*)", re.I)  
  aspath_pttrn02 = re.compile(r"\$\{([a-z_][0-9a-z_]*)\}", re.I)  
  def __init__(self, configPath=None):
    super(ShaactConfigParser, self).__init__()
    self.__file__ = configPath
    self.default_section = 'DEFAULT'

  def evalpath(self, val):
    def repl(match):
      name = match.group(1)
      return environ[name] if name in environ else ""
    val = ShaactConfigParser.aspath_pttrn01.sub(repl, val)
    val = ShaactConfigParser.aspath_pttrn02.sub(repl, val)
    return val
  
  def save(self):
    with open(self.__file__, 'w') as f:
      print("WRITE", self.__file__)
      self.write(f)

__dir__ = os.path.dirname(__file__)

def load_config(configPath):
  global config
  try:
    config = ShaactConfigParser(configPath)
    config.read(configPath)
    return config
  except IOError:
    return None



