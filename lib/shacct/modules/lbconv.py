from __future__ import print_function
from . import *
from shacct import config
import csv
from sys import stdin, stdout
from util import centerify, prependn, money_as_dec, moneyfmt

def _conv_val(amount, name):
  if name == "IRR":
    return moneyfmt(money_as_dec(amount) / 10, 0)
  return amount

def lbconv(btcname, nonbtcname, owner="", description="", section='DEFAULT'):
  writer = csv.writer(stdout, delimiter="|")
  for row in csv.reader(stdin, delimiter="|"):
    if row[2].strip().lower() == 'buy':
      writer.writerow([
        row[0].strip()[:16],
        centerify(row[1] if row[1].strip() != "" or owner == "" else owner, 9), "  conv  ",
        prependn(_conv_val(row[3].strip(), nonbtcname), 12),
        prependn(_conv_val(row[5].strip(), btcname), 12),
        centerify(nonbtcname, 9),
        centerify(btcname, 9),
        " %s" % description 
      ])
    else:
      writer.writerow([
        row[0].strip()[:16],
        centerify(row[1] if row[1].strip() != "" or owner == "" else owner, 9), "  conv  ",
        prependn(_conv_val(row[3].strip(), btcname), 12),
        prependn(_conv_val(row[5].strip(), nonbtcname), 12),
        centerify(btcname, 9),
        centerify(nonbtcname, 9),
        " %s" % description 
      ])

commands = { }
default_command = lbconv

def main(args):
  init_module(args)
  eval_command_type_a(commands, default_command, args)
