
from . import *
from time import time

def init():
  pass

commands = {}
default_command = init

def main(args, config):
  init_module(args, config)
  eval_command_type_a(commands, default_command, args, config)
