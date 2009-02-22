#/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from tool.SubtitleLibOld import SubtitleFile

class MainFrame(wx.Frame):
  """This is the main frame of the application.
  It should be designed to be as simple as possible.
  """
  
  MAIN_FRAME_ID = wx.NewId()
  DROPBOX_ID = wx.NewId()
  DROP_TEXT_ID = wx.NewId()
    
  def __init__(self):
    wx.Frame.__init__(self, None, -1, u"NoTagApp", wx.DefaultPosition, wx.Size(400, 300), 
                        wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.CAPTION | wx.STAY_ON_TOP, u"MainFrame")
    
    wx.InitAllImageHandlers()
    self.initControls()

  def initControls(self):
    """create and initialize UI elements"""
    
    # Controls Initialization and showing of the form
    mainpanel = wx.Panel(self, self.MAIN_FRAME_ID)
    s_box = wx.StaticBox(mainpanel)
    
    drop_text = wx.StaticText(mainpanel, self.DROP_TEXT_ID, u"Drop file(s) here", 
                                      wx.DefaultPosition, wx.DefaultSize, wx.CENTRE)    
    drop_text.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    
    static_sizer = wx.StaticBoxSizer(s_box, wx.VERTICAL)
    static_sizer.Add(drop_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    
    mainpanel.SetSizer(static_sizer)
    
    target1 = DropFile()
    s_box.SetDropTarget(target1)
    target2 = DropFile()
    drop_text.SetDropTarget(target2)

    self.SetMinSize(wx.Size(320, 100))
    self.SetMaxSize(wx.Size(320, 100))

    self.Center()
    self.Show(True)


class DropFile(wx.FileDropTarget):
  """"""
    
  def __init__(self):
    wx.FileDropTarget.__init__(self)
        
  def OnDropFiles(self, x, y, files):
    srt = SubtitleFile()
    for file in files:
      srt.File = file
      srt.toAss()
      srt.toTranscript()
      srt.removeTag()
