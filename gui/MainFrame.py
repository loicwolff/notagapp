#/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from gui.DropBox import DropBox

class MainFrame(wx.Frame):
  """This is the main frame of the application.
  It should be designed to be as simple as possible.
  """
  
  MAIN_FRAME_ID = wx.NewId()
  DROPBOX_ID = wx.NewId()
  DROP_TEXT_ID = wx.NewId()
    
  def __init__(self):
    wx.Frame.__init__(self, None, -1, u"NoTagApp", wx.DefaultPosition, wx.Size(400, 300), 
                        wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.CAPTION, u"MainFrame")
    
    wx.InitAllImageHandlers()
    self.initControls()

  def initControls(self):
    """create and initialize UI elements"""
    
    # Controls Initialization and showing of the form
    self.mainpanel = wx.Panel(self, self.MAIN_FRAME_ID)
    self.SetMinSize(wx.Size(320, 240))
    
    self.static_sizer = wx.StaticBoxSizer(wx.StaticBox(self.mainpanel), wx.VERTICAL)

    self.v_sizer = wx.BoxSizer(wx.VERTICAL)

    self.drop_text = wx.StaticText(self.mainpanel, self.DROP_TEXT_ID, u"Drop file(s) here", 
                                       wx.DefaultPosition, wx.DefaultSize, wx.CENTRE)
    self.dropbox = DropBox(self.mainpanel, self.DROPBOX_ID)
    
    self.drop_text.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    
    self.v_sizer.Add(self.drop_text, 0, wx.ALIGN_CENTRE, 20)
    self.v_sizer.Add(self.dropbox, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    
    self.static_sizer.Add(self.v_sizer, 0, wx.EXPAND, 20)
    
    self.mainpanel.SetSizer(self.static_sizer)
    
    self.Center()
    self.Show(True)
