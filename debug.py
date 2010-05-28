#!/usr/bin/env python
# encoding: utf-8

from __future__ import with_statement

is_enabled = False

def out(info):
  """print the result to the console"""
  if is_enabled:
    print(info)

def write(info):
  with open('debug.txt', 'a') as debug_file:
    debug_file.write(info + '\n')

def clear():
  """clear the content of the debug.txt file"""
  pass

if __name__ == '__main__':
  is_enabled = True
  out('testing debug module')