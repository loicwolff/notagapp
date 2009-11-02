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
    general_boxsizer = wx.BoxSizer(wx.HORIZONTAL)

    self._to_ass_checkbox = wx.CheckBox(self, wx.ID_ANY, u"To ASS")
    self._to_srt_checkbox = wx.CheckBox(self, wx.ID_ANY, u"")
    self._to_transcript_checkbox = wx.CheckBox(self, wx.ID_ANY, u"Transcript")
    self._to_zip_checkbox = wx.CheckBox(self, wx.ID_ANY, u"")

    self._srt_combo = wx.Choice(self,
                                wx.ID_ANY,
                                wx.DefaultPosition,
                                wx.Size(130, -1),
                                [u"tag.srt", u"notag.srt", u"tag&notag.srt"])
    self._srt_combo.SetSelection(2)

    self._zip_combo = wx.Choice(self,
                                wx.ID_ANY,
                                wx.DefaultPosition,
                                wx.Size(105, -1),
                                [u"zip&keep", u"zip&delete"])
    self._zip_combo.SetSelection(0)

    self._to_transcript_checkbox.SetValue(False)
    self._to_srt_checkbox.SetValue(True)
    self._to_ass_checkbox.SetValue(True)
    self._to_zip_checkbox.SetValue(True)

    general_boxsizer.AddSpacer(20)
    general_boxsizer.Add(wx.TextCtrl(self, wx.ID_ANY, 'tezt'))
    general_boxsizer.AddSpacer(20)
    general_boxsizer.Add(self._to_srt_checkbox)
    general_boxsizer.Add(self._srt_combo)
    general_boxsizer.AddSpacer(20)
    general_boxsizer.Add(self._to_ass_checkbox)
    general_boxsizer.AddSpacer(20)
    general_boxsizer.Add(self._to_zip_checkbox)
    general_boxsizer.Add(self._zip_combo)
           #, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)

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
