#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import wx

from TabPrefs import AssPref, GeneralPref


class Preferences(wx.Frame):
  """Preferences pages"""
  _MAINFRAME_ID = wx.NewId()

  _CONFIG_FILE = os.path.expanduser('~/.notagapp.conf')

  def __init__(self):
    super(Preferences, self).__init__(None,
                                      -1,
                                      u"Preferences",
                                      wx.DefaultPosition,
                                      wx.Size(550, 500))#,
                                      #wx.CLOSE_BOX | wx.CAPTION |
                                      #wx.STAY_ON_TOP | wx.SYSTEM_MENU)

    self.initControls()
    self.Center()
    self.Show(True)

  def initControls(self):
    """docstring for initControls"""
    notebook = wx.Notebook(self, wx.ID_ANY)
    notebook.AddPage(GeneralPref(notebook), u"General")
    notebook.AddPage(AssPref(notebook), u"ASS")


def main():

  class App(wx.App):
    def OnInit(self):
      pref = Preferences()
      return True

  app = App(False)
  app.MainLoop()


if __name__ == '__main__':
  main()
