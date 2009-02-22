#/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from tool.SubtitleLibOld import SubtitleFile
#import sys
#if sys.version_info[0:2] == (2, 6) or sys.version_info[0] == 3:
#  print("importing py3k-ready version")
#  from tool.SubtitleLib import SubtitleFile
#else:
#  print "import py2.5 legacy version"
#  from tool.SubtitleLibOld import SubtitleFile

class MainFrame(wx.Frame):
  """This is the main frame of the application.
  It should be designed to be as simple as possible.
  """
  
  _MAIN_FRAME_ID = wx.NewId()
  _TO_ASS_CHECKBOX_ID = wx.NewId()
  _REMOVE_TAG_CHECKBOX_ID = wx.NewId()
  _TO_TRANSCRIPT_CHECKBOX_ID = wx.NewId()
  
  _to_ass_checkbox = None
  _remove_tag_checkbox = None
  _to_transcript_checkbox = None
  
  def __init__(self):
    wx.Frame.__init__(self, None, -1, u"NoTagApp", wx.DefaultPosition, wx.Size(400, 300), 
                        wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.CAPTION | wx.STAY_ON_TOP | wx.SYSTEM_MENU)
    
    wx.InitAllImageHandlers()
    self.initControls()
    
    self._to_transcript_checkbox.SetFocus()
    self.SetMinSize(wx.Size(-1, 100))
    self.SetMaxSize(wx.Size(-1, 100))

    self.Center()
    self.Show(True)

  def initControls(self):
    """create and initialize UI elements"""
    
    # Controls Initialization and showing of the form
    mainpanel = wx.Panel(self, self._MAIN_FRAME_ID)
    
    drop_text = wx.StaticText(mainpanel, wx.ID_ANY, u"Drop file(s) here")
    drop_text.SetWindowStyle(wx.CENTRE)
    drop_text.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    
    static_box = wx.StaticBox(mainpanel)
    drop_sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
    drop_sizer.Add(drop_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    
    self._to_ass_checkbox = wx.CheckBox(mainpanel, self._TO_ASS_CHECKBOX_ID, u"Generate .ass")
    self._remove_tag_checkbox = wx.CheckBox(mainpanel, self._REMOVE_TAG_CHECKBOX_ID, u"Remove tags")
    self._to_transcript_checkbox = wx.CheckBox(mainpanel, self._TO_TRANSCRIPT_CHECKBOX_ID, u"Transcript")
    
    cb_sizer = wx.BoxSizer(wx.HORIZONTAL)
    cb_sizer.Add(self._to_transcript_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._remove_tag_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_ass_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    
    self._to_transcript_checkbox.SetValue(False)
    self._remove_tag_checkbox.SetValue(True)
    self._to_ass_checkbox.SetValue(True)

    main_sizer = wx.BoxSizer(wx.VERTICAL)
    main_sizer.Add(drop_sizer, 1, wx.EXPAND, 10)
    main_sizer.Add(cb_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

    mainpanel.SetSizer(main_sizer)
    
    static_box_target = DropFile(self)
    static_box.SetDropTarget(static_box_target)
    
    drop_text_target = DropFile(self)
    drop_text.SetDropTarget(drop_text_target)
    
  def getGenerateFiles(self):
    """Return a tuble of the checkboxes values"""
    return (self._to_transcript_checkbox.IsChecked(), 
            self._remove_tag_checkbox.IsChecked(),
            self._to_ass_checkbox.IsChecked())

class DropFile(wx.FileDropTarget):
  """"""
  
  def __init__(self, parent):
    wx.FileDropTarget.__init__(self)
    self._parent = parent
        
  def OnDropFiles(self, x, y, files):
    _to_transcript, _remove_tag, _to_ass = self._parent.getGenerateFiles()
  
    srt = SubtitleFile()
    for file in files:
      srt.File = file
      if _to_ass:
        srt.toAss()
      if _to_transcript:
        srt.toTranscript()
      if _remove_tag:
        srt.removeTag()
