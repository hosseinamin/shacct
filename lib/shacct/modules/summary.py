from __future__ import print_function
from . import *
from shacct import config
from decimal import Decimal
import csv
import os.path
from util import money_as_dec, moneyfmt

def summary(history=None, until=None, section='DEFAULT'):
  result = {}
  def print_var(name, value):
    is_btc = name.lower().endswith('btc')
    print("%s = %s" % (name, moneyfmt(value, 8 if is_btc else 2)))
  def setres(name, op, inp, default):
    if name not in result:
      result[name] = default
    if op == '=':
      result[name] = inp
    elif op == '+=':
      result[name] += inp
    elif op == '-=':
      result[name] -= inp
    elif op == '*=':
      result[name] += inp
    else:
      raise AssertionError("unknown op")
    return result[name]
  if history is None:
    history = os.path.join(config.evalpath(config[section]['path']), "history")
  with open(history, 'r') as f:
    rows = list(csv.reader(f, delimiter='|'))
    rows.reverse()
    bafeq = False
    size=len(rows)
    for i in range(size):
      try:
        row = rows[i]
        if len(row) < 8 or row[0].startswith("#"):
          continue
        row = map(lambda a: a.strip(), row)
        if until is not None:
          if until == row[0]:
            bafeq = True
          elif bafeq:
            break
        setres("_count", "+=", Decimal(1), Decimal(0))
        if row[2] == 'conv':
          name = row[1]
          src_asset = row[5]
          src_amount = money_as_dec(row[3])
          dest_asset = row[6]
          dest_amount = money_as_dec(row[4])
          #setres("%s, recv, %s" % (name, dest_asset), "+=", dest_amount, Decimal(0))
          #setres("%s, sent, %s" % (name, src_asset), "+=", src_amount, Decimal(0))
          setres("%s, sum, %s" % (name, dest_asset), "+=", dest_amount, Decimal(0))
          setres("%s, sum, %s" % (name, src_asset), "-=", src_amount, Decimal(0))
          setres("_asset: sum, %s" % (src_asset), "-=", src_amount, Decimal(0))
          setres("_asset: sum, %s" % (dest_asset), "+=", dest_amount, Decimal(0))
          #setres("_asset: sent, %s" % (src_asset), "+=", src_amount, Decimal(0))
          #setres("_asset: recv, %s" % (dest_asset), "+=", dest_amount, Decimal(0))
        elif row[2] == 'push':
          name = row[1]
          asset = row[5]
          amount = money_as_dec(row[3])
          #setres("%s, recv, %s" % (name, asset), "+=", amount, Decimal(0))
          setres("%s, sum, %s" % (name, asset), "+=", amount, Decimal(0))
          #setres("_asset: recv, %s" % (asset), "+=", amount, Decimal(0))
          setres("_asset: sum, %s" % (asset), "+=", amount, Decimal(0))
          #setres("%s, %s, pushed" % (name, asset), "+=", amount, Decimal(0))
          #setres("_asset: %s, pushed" % (asset), "+=", amount, Decimal(0))
        elif row[2] == 'pull':
          name = row[1]
          asset = row[5]
          amount = money_as_dec(row[3])
          #setres("%s, sent, %s" % (name, asset), "+=", amount, Decimal(0))
          setres("%s, sum, %s" % (name, asset), "-=", amount, Decimal(0))
          #setres("_asset: sent, %s" % (asset), "+=", amount, Decimal(0))
          setres("_asset: sum, %s" % (asset), "-=", amount, Decimal(0))
          #setres("%s, %s, pulled" % (name, asset), "+=", amount, Decimal(0))
          #setres("_asset: %s, pulled" % (asset), "+=", amount, Decimal(0))
        else:
          raise AssertionError("undefined action, row[2], %s" % (row[2]))
      except:
        print("Error at row %d" % (size-i))
        raise
    for name, val in sorted(result.items(), key=lambda a:a[0]):
      print_var(name, val)

commands = { }
default_command = summary

def main(args):
  init_module(args)
  eval_command_type_a(commands, default_command, args)
