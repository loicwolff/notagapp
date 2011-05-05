#/usr/bin/env python2.5
# encoding: utf-8

# python lib
import os

# external lib
import wx

print(wx.__version__)

from AppMode import QuickMode, SmartMode


class MainFrame(wx.Frame):
  """This is the main frame of the application.
  It should be designed to be as simple as possible.
  """

  def __init__(self, title):
    super(MainFrame, self).__init__(None, -1, title, wx.DefaultPosition,
                                    wx.Size(510, 140),
                                    wx.CLOSE_BOX | wx.MINIMIZE_BOX |
                                    wx.CAPTION | wx.STAY_ON_TOP |
                                    wx.SYSTEM_MENU)

    wx.InitAllImageHandlers()
    self._initControls()

    self.SetMinSize(wx.Size(510, 140))
    #self.SetMaxSize(wx.Size(-1, 140))

    self.Center()
    self.Show(True)

  def _initControls(self):
    """create and initialize UI elements"""

    # Controls Initialization and showing of the form
    notebook = wx.Notebook(self)
    notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnNoteBookTabChanging)

    quick_mode = QuickMode(notebook)
    #smart_mode = SmartMode(notebook)

    notebook.AddPage(quick_mode, u'Quick')
    #notebook.AddPage(smart_mode, u'Smart')
    #notebook.SetSelection(1)

    main_sizer = wx.BoxSizer(wx.VERTICAL)
    main_sizer.Add(notebook, 1, wx.EXPAND, 10)

    self.SetSizer(main_sizer)

  def OnNoteBookTabChanging(self, event):
    smartmode_size = 400
    tinymode_size = 140
    
    if event.GetSelection() == 0: # go to tiny mode
      for height in range(smartmode_size, tinymode_size, -15):
        self.SetSize(wx.Size(510, height))
    elif event.GetSelection() == 1: # go to smart mode
      for height in range(tinymode_size, smartmode_size, 15):
        self.SetSize(wx.Size(510, height))

    event.Skip()


def main():
  class App(wx.App):
    def OnInit(self):
      frame = MainFrame()
      return True

  app = App(False)
  app.MainLoop()

if __name__ == '__main__':
  main()
