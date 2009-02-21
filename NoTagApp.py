#/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from gui.MainFrame import MainFrame

class NoTagApp(wx.App):
  def OnInit(self):
    main = MainFrame()
    return True
  
if __name__ == '__main__':
  import sys
  app = NoTagApp(False)
  app.MainLoop()

