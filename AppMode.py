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

class TinyMode(wx.Panel):
    """Panel to show inside the tiny mode"""
    def __init__(self, parent):
        super(TinyMode, self).__init__(parent)
    
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
    
        drop_text_target = QuickDropbox(self.getFilesToBuild)
        drop_text.SetDropTarget(drop_text_target)
    
        mainpanel_target = QuickDropbox(self.getFilesToBuild)
        self.SetDropTarget(mainpanel_target)
    
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

class MaxiMode(wx.Panel):
    """Panel to show inside the maxi mode"""
    def __init__(self, parent):
        super(MaxiMode, self).__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        #main_sizer.Add(drop_sizer, 1, wx.EXPAND, 10)
        #main_sizer.Add(cb_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetSizer(main_sizer)
    