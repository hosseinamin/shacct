from __future__ import print_function
from . import *
from shacct import config
from decimal import Decimal
import csv
import os.path

def summary(until=None, section='DEFAULT'):
  result = {}
  def print_var(name, value):
    print("%s = %s" % (name, value))
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
  with open(os.path.join(config.evalpath(config[section]['path']), "history"), 'r') as f:
    rows = list(csv.reader(f, delimiter='|'))
    rows.reverse()
    bafeq = False
    size=len(rows)
    for i in range(size):
      try:
        row = rows[i]
        if len(row) < 9 or row[0].startswith("#"):
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
          src_storage = row[3]
          src_asset = src_storage + "_" + row[4]
          src_amount = Decimal(row[5])
          dest_storage = row[6]
          dest_asset = dest_storage + "_" + row[7]
          dest_amount = Decimal(row[8])
          setres("%s, %s, recv" % (name, dest_asset), "+=", dest_amount, Decimal(0))
          setres("%s, %s, sent" % (name, src_asset), "+=", src_amount, Decimal(0))
          setres("%s, %s, sum" % (name, dest_asset), "+=", dest_amount, Decimal(0))
          setres("%s, %s, sum" % (name, src_asset), "-=", src_amount, Decimal(0))
          setres("_asset: %s, sum" % (src_asset), "-=", src_amount, Decimal(0))
          setres("_asset: %s, sum" % (dest_asset), "+=", dest_amount, Decimal(0))
          setres("_asset: %s, sent" % (src_asset), "+=", src_amount, Decimal(0))
          setres("_asset: %s, recv" % (dest_asset), "+=", dest_amount, Decimal(0))
        elif row[2] == 'push':
          name = row[1]
          storage = row[6]
          asset = storage + "_" + row[7]
          amount = Decimal(row[8])
          setres("%s, %s, recv" % (name, asset), "+=", amount, Decimal(0))
          setres("%s, %s, sum" % (name, asset), "+=", amount, Decimal(0))
          setres("_asset: %s, recv" % (asset), "+=", amount, Decimal(0))
          setres("_asset: %s, sum" % (asset), "+=", amount, Decimal(0))
          #setres("%s, %s, pushed" % (name, asset), "+=", amount, Decimal(0))
          #setres("_asset: %s, pushed" % (asset), "+=", amount, Decimal(0))
        elif row[2] == 'pull':
          name = row[1]
          storage = row[6]
          asset = storage + "_" + row[7]
          amount = Decimal(row[8])
          setres("%s, %s, sent" % (name, asset), "+=", amount, Decimal(0))
          setres("%s, %s, sum" % (name, asset), "-=", amount, Decimal(0))
          setres("_asset: %s, sent" % (asset), "+=", amount, Decimal(0))
          setres("_asset: %s, sum" % (asset), "-=", amount, Decimal(0))
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
