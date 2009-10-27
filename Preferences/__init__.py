#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Loïc Wolff on 2009-06-22.
Copyright (c) 2009 loicwolff.eu. All rights reserved.
"""

import sys
import os
import wx

class PreferencesPane(wx.Frame):
  """Preferences pane entry"""
  def __init__(self):
    super(PreferencesPane, self).__init__(None, -1, u"Preferences", wx.DefaultPosition, wx.Size(550, 500))

if __name__ == '__main__':
  pass