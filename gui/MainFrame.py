#/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from util.subtitle import SubtitleFile
import zipfile
import os

class MainFrame(wx.Frame):
  """This is the main frame of the application.
  It should be designed to be as simple as possible.
  """
  
  _MAIN_FRAME_ID = wx.NewId()
  _TO_ASS_CHECKBOX_ID = wx.NewId()
  _TO_SRT_CHECKBOX_ID = wx.NewId()
  _TO_TRANSCRIPT_CHECKBOX_ID = wx.NewId()
  _TO_ZIP_CHECKBOX_ID = wx.NewId()
  _ASS_COMBO_ID = wx.NewId()
  _SRT_COMBO_ID = wx.NewId()
  _ZIP_COMBO_ID = wx.NewId()
  
  _to_ass_checkbox = None
  _to_srt_checkbox = None
  _to_transcript_checkbox = None
  _to_zip_checkbox = None
  
  #_ass_combo = None
  _srt_combo = None
  _zip_combo = None
  
  def __init__(self):
    wx.Frame.__init__(self, None, -1, u"NoTagApp", wx.DefaultPosition, wx.Size(510, 300), 
                        wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.CAPTION | wx.STAY_ON_TOP | wx.SYSTEM_MENU)
    
    wx.InitAllImageHandlers()
    self.initControls()
    
    self._to_transcript_checkbox.SetFocus()
    self.SetMinSize(wx.Size(-1, 110))
    self.SetMaxSize(wx.Size(-1, 110))

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
    
    self._to_ass_checkbox = wx.CheckBox(mainpanel, self._TO_ASS_CHECKBOX_ID, u"To SSA")
    self._to_srt_checkbox = wx.CheckBox(mainpanel, self._TO_SRT_CHECKBOX_ID, u"")
    self._to_transcript_checkbox = wx.CheckBox(mainpanel, self._TO_TRANSCRIPT_CHECKBOX_ID, u"Transcript")
    self._to_zip_checkbox = wx.CheckBox(mainpanel, self._TO_ZIP_CHECKBOX_ID, u"")
    
    self._srt_combo = wx.Choice(mainpanel, self._SRT_COMBO_ID, wx.DefaultPosition, wx.Size(130, -1), 
                                [u"tag.srt", u"notag.srt", u"tag&notag.srt"])
    self._srt_combo.SetSelection(2)
    
    self._zip_combo = wx.Choice(mainpanel, self._ZIP_COMBO_ID, wx.DefaultPosition, wx.Size(105, -1),
                                [u"zip&keep", u"zip&delete"])
    
    cb_sizer = wx.BoxSizer(wx.HORIZONTAL)
    cb_sizer.Add(self._to_transcript_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_srt_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.Add(self._srt_combo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 10)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_ass_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_zip_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.Add(self._zip_combo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    
    self._to_transcript_checkbox.SetValue(False)
    self._to_srt_checkbox.SetValue(True)
    self._to_ass_checkbox.SetValue(True)
    self._to_zip_checkbox.SetValue(True)

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
            self._to_srt_checkbox.IsChecked(), self._srt_combo.GetCurrentSelection(),
            self._to_ass_checkbox.IsChecked(), 
            self._to_zip_checkbox.IsChecked(), self._zip_combo.GetCurrentSelection() == 0)

class DropFile(wx.FileDropTarget):
  """"""
  
  def __init__(self, parent):
    wx.FileDropTarget.__init__(self)
    self._parent = parent
    self._generated_files = set()
        
  def OnDropFiles(self, x, y, files):
    do_transcript, do_srt, srt_choice, do_ssa, do_zip, keep_zip = self._parent.getGenerateFiles()

    srt = SubtitleFile()
    for file in files:
      srt.File = file
      self._generated_files.add(srt.File)
      
      if do_ssa:
        srt.toSSA()
        self._generated_files.add(u"%s.ssa" % (srt.SubName))
      
      if do_srt:
        if srt_choice == 0:
          srt.toSRT(keep_tag=True)
          self._generated_files.add(u"%s.TAG.srt" % (srt.SubName))
        elif srt_choice == 1:
          srt.toSRT(keep_tag=False)
          self._generated_files.add(u"%s.NOTAG.srt" % (srt.SubName))
        else:
          srt.toSRT(keep_tag=True)
          srt.toSRT(keep_tag=False)
          self._generated_files.add(u"%s.TAG.srt" % (srt.SubName))
          self._generated_files.add(u"%s.NOTAG.srt" % (srt.SubName))
          
      if do_transcript:
        srt.toTranscript()
      
      if do_zip:
        zip_file = zipfile.ZipFile("%s.zip" % (srt.SubName), "w")
        for gen in self._generated_files:
          zip_file.write(gen, os.path.basename(gen))
        zip_file.close()  
        
        if not keep_zip:
          for gen in self._generated_files:
            os.remove(gen)
            
      print("%s subtitle(s) and %s line(s) processed" % (srt.stats()))
