#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import wx


class GeneralPref(wx.Panel):
  """Panel containing the general preferences"""

  def __init__(self, parent):
    super(GeneralPref, self).__init__(parent)
    self._initControls()

  def _initControls(self):
    """docstring for initControls"""
    cb_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    self._to_srt_checkbox = wx.CheckBox(self, wx.ID_ANY, u"Tag")
    self._to_notag_srt_checkbox = wx.CheckBox(self, wx.ID_ANY, u"NoTag")
    self._to_ass_checkbox = wx.CheckBox(self, wx.ID_ANY, u".ASS")
    self._to_transcript_checkbox = wx.CheckBox(self, wx.ID_ANY, u"Transcript")
    self._to_zip_checkbox = wx.CheckBox(self, wx.ID_ANY, u"Zip it!")

    self._to_transcript_checkbox.SetValue(False)
    self._to_srt_checkbox.SetValue(True)
    self._to_notag_srt_checkbox.SetValue(True)
    self._to_ass_checkbox.SetValue(True)
    self._to_zip_checkbox.SetValue(True)

    cb_boxsizer.AddSpacer(20)
    cb_boxsizer.Add(self._to_transcript_checkbox)
    cb_boxsizer.AddSpacer(20)
    cb_boxsizer.Add(self._to_srt_checkbox)
    cb_boxsizer.AddSpacer(20)
    cb_boxsizer.Add(self._to_notag_srt_checkbox)
    cb_boxsizer.AddSpacer(20)
    cb_boxsizer.Add(self._to_ass_checkbox)
    cb_boxsizer.AddSpacer(20)
    cb_boxsizer.Add(self._to_zip_checkbox)
    
    destination_sizer = wx.BoxSizer(wx.HORIZONTAL)
    
    destination_choices = ["Same folder as subtitle", "Desktop", "Ask everytime", "Other..."]
    self._dropdown_destination = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, destination_choices)

    destination_sizer.Add(wx.StaticText(self, wx.ID_ANY, u"Create subtitles in: "))
    destination_sizer.Add(self._dropdown_destination)

    general_boxsizer = wx.BoxSizer(wx.VERTICAL)
    general_boxsizer.Add(wx.StaticText(self, wx.ID_ANY, u"Choose default"))
    general_boxsizer.AddSpacer(10)
    general_boxsizer.Add(cb_boxsizer)
    general_boxsizer.AddSpacer(30)
    general_boxsizer.Add(destination_sizer)

    self.SetSizer(general_boxsizer)


class AssPref(wx.Panel):
  """Stylechooser for Ass files"""

  def __init__(self, parent):
    super(AssPref, self).__init__(parent)

    self.initControls()

  def initControls(self):
    """init the controls"""

    self.fontSizer = wx.BoxSizer(wx.HORIZONTAL)

    self.fontSizer.AddSpacer(5)
    self.fontSizer.Add(wx.StaticText(self, wx.ID_ANY, u"Font: "))
    self.fontChooser = wx.Choice(self,
                                 wx.ID_ANY,
                                 wx.DefaultPosition,
                                 wx.DefaultSize,
                                 [u"Arial", u"Comic Sans MS", u"Verdana"])
    self.fontSizer.Add(self.fontChooser)

    self.fontSizer.AddSpacer(20)
    self.fontSizer.Add(wx.StaticText(self, wx.ID_ANY, u"Font Size: "))
    self.fontSizeChooser = wx.TextCtrl(self,
                                       wx.ID_ANY,
                                       wx.EmptyString,
                                       wx.DefaultPosition,
                                       wx.Size(30, -1))

    self.fontSizer.Add(self.fontSizeChooser)

    self.styleSizer = wx.BoxSizer(wx.HORIZONTAL)

    self.boldCB = wx.CheckBox(self, wx.ID_ANY, u"Bold")
    self.itaCB = wx.CheckBox(self, wx.ID_ANY, u"Italic")
    self.underCB = wx.CheckBox(self, wx.ID_ANY, u"Underline")
    self.strikeCB = wx.CheckBox(self, wx.ID_ANY, u"Strike")
    self.outlineCB = wx.CheckBox(self, wx.ID_ANY, u"Outline")
    self.shadowCB = wx.CheckBox(self, wx.ID_ANY, u"Shadow")

    self.styleSizer.Add(self.boldCB)
    self.styleSizer.Add(self.itaCB)
    self.styleSizer.Add(self.underCB)
    self.styleSizer.Add(self.strikeCB)
    self.styleSizer.Add(self.outlineCB)
    self.styleSizer.Add(self.shadowCB)


    #PrimaryColour, SecondaryColour, OutlineColour, BackColour, ScaleX, ScaleY,
    #Spacing, Angle, BorderStyle, Outline, Alignment,
    #MarginL, MarginR, MarginV, Encoding

    self.wrapper = wx.BoxSizer(wx.VERTICAL)
    self.wrapper.AddSpacer(20)
    self.wrapper.Add(self.fontSizer, 20)
    self.wrapper.AddSpacer(20)
    self.wrapper.Add(self.styleSizer, 20)

    self.SetSizer(self.wrapper)


def main():
  pass

if __name__ == '__main__':
  main()
