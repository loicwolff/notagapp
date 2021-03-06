#/usr/bin/env python2.5
# encoding: utf-8

import sys

import wx

from MainFrame import MainFrame
from subtitle import SubtitleFile


class NoTagApp(wx.App):
  """Main class to launch NoTag"""
  
  def OnInit(self):
    main = MainFrame(u'NoTag')
    return True

  def BringWindowToFront(self):
    try:
      self.GetTopWindow().Raise()
    except:
      pass

  def OnActivate(self, event):
    if event.GetActive():
      self.BringWindowToFront()
    else:
      event.Skip()

  def OpenFileMessage(self, filename):
    pass

  def MacOpenFile(self, filename):
    """Called for files droped on dock icon,
    or opened via finders context menu"""
    sub = SubtitleFile()
    print filename
    print "%s dropped on app" % (filename)
    #self.OpenFileMessage(filename)

  def MacReopenApp(self):
    """Called when the doc icon is clicked"""
    self.BringWindowToFront()

  def MacNewFile(self):
    pass

  def MacPrintFile(self, file_path):
    pass


if __name__ == '__main__':
  app = NoTagApp(False)
  app.MainLoop()
