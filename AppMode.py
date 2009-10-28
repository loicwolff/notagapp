#!/usr/bin/env python
# encoding: utf-8
"""
TinyMode.py

Created by Loïc Wolff on 2009-10-26.
Copyright (c) 2009 . All rights reserved.
"""

import sys
import os

import wx

from Dropbox import QuickDropbox

_TO_ASS_CHECKBOX_ID = wx.NewId()
_TO_SRT_TAG_CHECKBOX_ID = wx.NewId()
_TO_SRT_NOTAG_CHECKBOX_ID = wx.NewId()
_TO_TRANSCRIPT_CHECKBOX_ID = wx.NewId()
_TO_ZIP_CHECKBOX_ID = wx.NewId()

class QuickMode(wx.Panel):
  """Panel to show inside the tiny mode"""
  def __init__(self, parent):
    super(QuickMode, self).__init__(parent)
    
    drop_text = wx.StaticText(self, wx.ID_ANY, u"Drop file(s) here")
    drop_text.SetWindowStyle(wx.CENTRE)
    drop_text.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
  
    drop_sizer = wx.BoxSizer(wx.VERTICAL)
    drop_sizer.Add(drop_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
  
    self._to_srt_tag_checkbox = wx.CheckBox(self, _TO_SRT_TAG_CHECKBOX_ID, u"Tag")
    self._to_srt_notag_checkbox = wx.CheckBox(self, _TO_SRT_NOTAG_CHECKBOX_ID, u"NoTag")
    self._to_ass_checkbox = wx.CheckBox(self, _TO_ASS_CHECKBOX_ID, u".ASS")
    self._to_transcript_checkbox = wx.CheckBox(self, _TO_TRANSCRIPT_CHECKBOX_ID, u"Transcript")
    self._to_zip_checkbox = wx.CheckBox(self, _TO_ZIP_CHECKBOX_ID, u"Zip it!")
  
    cb_sizer = wx.BoxSizer(wx.HORIZONTAL)
    cb_sizer.Add(self._to_transcript_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_srt_tag_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_srt_notag_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_ass_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_zip_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
  
    self._to_transcript_checkbox.SetValue(False)
    self._to_srt_tag_checkbox.SetValue(True)
    self._to_srt_notag_checkbox.SetValue(True)
    self._to_ass_checkbox.SetValue(True)
    self._to_zip_checkbox.SetValue(True)
  
    drop_target = QuickDropbox(self.getFilesToBuild)
    drop_text.SetDropTarget(drop_target)
    drop_target = QuickDropbox(self.getFilesToBuild)
    self.SetDropTarget(drop_target)
  
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    main_sizer.Add(drop_sizer, 1, wx.EXPAND, 10)
    main_sizer.Add(cb_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
    self.SetSizer(main_sizer)

  def getFilesToBuild(self):
    """Return a tuple of the checkboxes values"""
    return (self._to_transcript_checkbox.IsChecked(),
        self._to_srt_tag_checkbox.IsChecked(),
        self._to_srt_notag_checkbox.IsChecked(),
        self._to_ass_checkbox.IsChecked(),
        self._to_zip_checkbox.IsChecked())

class SmartMode(wx.Panel):
  """Panel to show inside the maxi mode"""
  def __init__(self, parent):
    super(SmartMode, self).__init__(parent)
    
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    
    # dropboxes
    dropbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
    sd_vf_box = wx.StaticBox(self)
    sd_vf_box.SetSize(wx.Size(100, 100))

    sd_vo_box = wx.StaticBox(self)
    sd_vo_box.SetSize(wx.Size(100, 100))

    hd_vo_box = wx.StaticBox(self)
    hd_vo_box.SetSize(wx.Size(100, 100))
    
    dropbox_sizer.AddSpacer(20)
    dropbox_sizer.Add(sd_vf_box, 0, wx.ALIGN_CENTER, 10)
    dropbox_sizer.AddSpacer(20)
    dropbox_sizer.Add(sd_vo_box, 0, wx.ALIGN_CENTER, 10)
    dropbox_sizer.AddSpacer(20)
    dropbox_sizer.Add(hd_vo_box, 0, wx.ALIGN_CENTER, 10)
    
    # checkboxes
    self._to_srt_tag_checkbox = wx.CheckBox(self, _TO_SRT_TAG_CHECKBOX_ID, u"Tag")
    self._to_srt_notag_checkbox = wx.CheckBox(self, _TO_SRT_NOTAG_CHECKBOX_ID, u"NoTag")
    self._to_ass_checkbox = wx.CheckBox(self, _TO_ASS_CHECKBOX_ID, u".ASS")
    self._to_transcript_checkbox = wx.CheckBox(self, _TO_TRANSCRIPT_CHECKBOX_ID, u"Transcript")
    self._to_zip_checkbox = wx.CheckBox(self, _TO_ZIP_CHECKBOX_ID, u"Zip it!")
  
    cb_sizer = wx.BoxSizer(wx.HORIZONTAL)
    cb_sizer.Add(self._to_transcript_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_srt_tag_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_srt_notag_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_ass_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_zip_checkbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
  
    self._to_transcript_checkbox.SetValue(False)
    self._to_srt_tag_checkbox.SetValue(True)
    self._to_srt_notag_checkbox.SetValue(True)
    self._to_ass_checkbox.SetValue(True)
    self._to_zip_checkbox.SetValue(True)
    
    main_sizer.AddSpacer(20)
    main_sizer.Add(dropbox_sizer)
    main_sizer.AddSpacer(20)
    main_sizer.Add(cb_sizer)
    main_sizer.AddSpacer(20)

    self.SetSizer(main_sizer)
    