from __future__ import print_function
from . import *
from shacct import config

# getter and setter for shacct config

def config_set(var_name, value, section='DEFAULT'):
  config[section][var_name] = value
  config.save()

def config_unset(var_name):
  del shacct.CONFIG[section][var_name]
  shacct.save_config()

def config_print(var_name=None, section='DEFAULT'):
  def print_var(name, value):
    print("%s = %s" % (name, value))
  if var_name == None:
    for name in config[section]:
      print_var(name, config[section][name])
  else:
    try:
      print_var(var_name, config[section][name])
    except KeyError:
      print("No such key!")

commands = { 'set': config_set, 'unset': config_unset }
default_command = config_print

def main(args):
  init_module(args)
  eval_command_type_a(commands, default_command, args)
