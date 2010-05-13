#!/usr/bin/env python
# encoding: utf-8
"""
debug.py

Created by Loïc Wolff on 2010-05-13.
Copyright (c) 2010 Loïc Wolff. All rights reserved.
"""

is_enabled = False

def out(arg):
  """print the result to the console"""
  if is_enabled:
    print(arg)


if __name__ == '__main__':
  out('testing debug module')