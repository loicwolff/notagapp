#/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from tool.SubtitleLib import SubtitleFile

class DropBox(wx.Panel):
  """The widget where the subtitle file will be dropped"""
  
  def __init__(self, parent, id): 
    wx.StaticText.__init__(self, parent, id, u"Drop files here", wx.Point(-100, 100), wx.DefaultSize, wx.ALIGN_CENTRE)
    
    #self.img = wx.Image("resource/drop_img2.png", wx.BITMAP_TYPE_ANY)
    #height, width = self.img.GetSize()
    #self.SetSize(wx.Size(height, width))

    #print("img size = {width}x{height}".format(width=width, height=height))
    #panel_height, panel_width = self.GetClientSizeTuple()
    #print("panel size = {width}x{height}".format(width=panel_width, height=panel_height))
    
    target = DropFile()
    self.SetDropTarget(target)
    
    #wx.EVT_PAINT(self, self.onPaint)
    
  def onPaint(self, event):
    dc = wx.PaintDC(self)
    dc = wx.BufferedDC(dc)
    
    height, width = self.img.GetSize()
    dc.DrawRectangle(0, 0, height, width)
    dc.DrawBitmap(wx.BitmapFromImage(self.img), 0, 0, True)
    self.SetBackgroundColour(wx.Colour(255, 255, 255))
        
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
