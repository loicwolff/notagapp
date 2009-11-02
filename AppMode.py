#!/usr/bin/env python
# encoding: utf-8

import sys
import os

import wx

from Dropbox import QuickDropbox, SmartDropbox


class QuickMode(wx.Panel):
  """Panel to show inside the quick mode"""

  def __init__(self, parent):
    super(QuickMode, self).__init__(parent)

    drop_text = wx.StaticText(self, wx.ID_ANY, u"Drop file(s) here")
    drop_text.SetWindowStyle(wx.CENTRE)
    drop_text.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT,
                                wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

    drop_sizer = wx.BoxSizer(wx.VERTICAL)
    drop_sizer.Add(drop_text, 0,
                    wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)

    self._to_srt_tag_checkbox = wx.CheckBox(self, label=u"Tag")
    self._to_srt_notag_checkbox = wx.CheckBox(self, label=u"NoTag")
    self._to_ass_checkbox = wx.CheckBox(self, label=u".ASS")
    self._to_transcript_checkbox = wx.CheckBox(self, label=u"Transcript")
    self._to_zip_checkbox = wx.CheckBox(self, label=u"Zip it!")

    cb_sizer = wx.BoxSizer(wx.HORIZONTAL)
    cb_sizer.Add(self._to_transcript_checkbox, 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_srt_tag_checkbox, 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_srt_notag_checkbox, 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_ass_checkbox, 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_zip_checkbox, 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)

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
  """Panel to show inside the smart mode"""

  def __init__(self, parent):
    super(SmartMode, self).__init__(parent)

    main_sizer = wx.BoxSizer(wx.VERTICAL)

    # dropboxes
    dropbox_sizer = wx.BoxSizer(wx.HORIZONTAL)

    DROPBOX_STYLE = wx.EXPAND |\
                    wx.ALIGN_CENTER_VERTICAL |\
                    wx.ALIGN_CENTER_HORIZONTAL

    DROPBOX_FONT = wx.Font(20, wx.DEFAULT, wx.FONTSTYLE_NORMAL,
                                                    wx.FONTWEIGHT_BOLD)

    sd_vf_box = wx.StaticBox(self)
    sd_vf_drop_text = wx.StaticText(parent=self,
                                    label=u'SD VF',
                                    size=wx.Size(100, 100),
                                    style=DROPBOX_STYLE)
    sd_vf_drop_text.SetFont(DROPBOX_FONT)
    sd_vf_static_boxsizer = wx.StaticBoxSizer(sd_vf_box, wx.HORIZONTAL)
    sd_vf_static_boxsizer.Add(sd_vf_drop_text, 1, DROPBOX_STYLE, 0)

    sd_vo_box = wx.StaticBox(self)
    sd_vo_drop_text = wx.StaticText(parent=self,
                                    label=u'SD VO',
                                    size=wx.Size(100, 100),
                                    style=wx.ALIGN_CENTRE)
    sd_vo_drop_text.SetFont(DROPBOX_FONT)
    sd_vo_static_boxsizer = wx.StaticBoxSizer(sd_vo_box, wx.HORIZONTAL)
    sd_vo_static_boxsizer.Add(sd_vo_drop_text, 1, DROPBOX_STYLE, 0)

    hd_vo_box = wx.StaticBox(self)
    hd_vo_drop_text = wx.StaticText(parent=self,
                                    label=u'HD VO',
                                    size=wx.Size(100, 100),
                                    style=wx.ALIGN_CENTRE)
    hd_vo_drop_text.SetFont(DROPBOX_FONT)
    hd_vo_static_boxsizer = wx.StaticBoxSizer(hd_vo_box, wx.HORIZONTAL)
    hd_vo_static_boxsizer.Add(hd_vo_drop_text, 1, DROPBOX_STYLE, 0)

    # checkboxes
    self._to_srt_tag_checkbox = wx.CheckBox(self, label=u"Tag")
    self._to_srt_notag_checkbox = wx.CheckBox(self, label=u"NoTag")
    self._to_ass_checkbox = wx.CheckBox(self, label=u".ASS")
    self._to_transcript_checkbox = wx.CheckBox(self, label=u"Transcript")
    self._to_zip_checkbox = wx.CheckBox(self, label=u"Zip it!")
    self.submitBtn = wx.Button(self, label=u"¡Vamos!")

    self._to_transcript_checkbox.SetValue(False)
    self._to_srt_tag_checkbox.SetValue(True)
    self._to_srt_notag_checkbox.SetValue(True)
    self._to_ass_checkbox.SetValue(True)
    self._to_zip_checkbox.SetValue(True)

    cb_sizer = wx.BoxSizer(wx.HORIZONTAL)
    cb_sizer.Add(self._to_transcript_checkbox, 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_srt_tag_checkbox, 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_srt_notag_checkbox, 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_ass_checkbox, 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self._to_zip_checkbox, 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    cb_sizer.AddSpacer(20)
    cb_sizer.Add(self.submitBtn)
    cb_sizer.AddSpacer(20)

    self._sd_vf_droptarget = SmartDropbox(self.updateUI)
    sd_vf_box.SetDropTarget(self._sd_vf_droptarget)
    self._sd_vo_droptarget = SmartDropbox(self.updateUI)
    sd_vo_box.SetDropTarget(self._sd_vo_droptarget)
    self._hd_vo_droptarget = SmartDropbox(self.updateUI)
    hd_vo_box.SetDropTarget(self._hd_vo_droptarget)

    dropbox_sizer.AddSpacer(20)
    dropbox_sizer.Add(sd_vf_static_boxsizer, 1, DROPBOX_STYLE, 100)
    dropbox_sizer.AddSpacer(20)
    dropbox_sizer.Add(sd_vo_static_boxsizer, 1, DROPBOX_STYLE, 100)
    dropbox_sizer.AddSpacer(20)
    dropbox_sizer.Add(hd_vo_static_boxsizer, 1, DROPBOX_STYLE, 100)
    dropbox_sizer.AddSpacer(20)
    
    main_sizer.AddSpacer(20)
    main_sizer.Add(dropbox_sizer, 0, wx.EXPAND, 100)
    main_sizer.AddSpacer(20)
    main_sizer.Add(cb_sizer)
    main_sizer.AddSpacer(20)

    self.SetSizer(main_sizer)

  def updateUI(self):
    """Update GUI when a file is dropped"""
    print(self._sd_vf_droptarget.SubDropped)
    print(self._sd_vo_droptarget.SubDropped)
    print(self._hd_vo_droptarget.SubDropped)
