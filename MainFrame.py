#/usr/bin/env python
# encoding: utf-8

# python lib
import os

# external lib
import wx

from DropBox import DropBox

class MainFrame(wx.Frame):
  """This is the main frame of the application.
  It should be designed to be as simple as possible.
  """
  
  _MAIN_FRAME_ID = wx.NewId()
  _TO_ASS_CHECKBOX_ID = wx.NewId()
  _TO_SRT_TAG_CHECKBOX_ID = wx.NewId()
  _TO_SRT_NOTAG_CHECKBOX_ID = wx.NewId()
  _TO_TRANSCRIPT_CHECKBOX_ID = wx.NewId()
  _TO_ZIP_CHECKBOX_ID = wx.NewId()
  
  _main_notebook = None
  
  _to_ass_checkbox = None
  _to_srt_checkbox = None
  _to_transcript_checkbox = None
  _to_zip_checkbox = None
  
  def __init__(self):
    super(MainFrame, self).__init__(None, -1, u"NoTagApp", wx.DefaultPosition, wx.Size(510, 140), 
                        wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.CAPTION | wx.STAY_ON_TOP | wx.SYSTEM_MENU)
                        
    wx.InitAllImageHandlers()
    self._initControls()
    
    self._to_transcript_checkbox.SetFocus()
    self.SetMinSize(wx.Size(510, 140))
    #self.SetMaxSize(wx.Size(-1, 140))

    self.Center()
    self.Show(True)

  def _initControls(self):
    """create and initialize UI elements"""
    
    # Controls Initialization and showing of the form
    self._main_notebook = wx.Notebook(self, wx.ID_ANY)
    
    mainpanel = wx.Panel(self._main_notebook, self._MAIN_FRAME_ID)
    
    drop_text = wx.StaticText(mainpanel, wx.ID_ANY, u"Drop file(s) here")
    drop_text.SetWindowStyle(wx.CENTRE)
    drop_text.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    
    drop_sizer = wx.BoxSizer(wx.VERTICAL)
    drop_sizer.Add(drop_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    
    self._to_srt_tag_checkbox = wx.CheckBox(mainpanel, self._TO_SRT_TAG_CHECKBOX_ID, u"Tag")
    self._to_srt_notag_checkbox = wx.CheckBox(mainpanel, self._TO_SRT_NOTAG_CHECKBOX_ID, u"NoTag")
    self._to_ass_checkbox = wx.CheckBox(mainpanel, self._TO_ASS_CHECKBOX_ID, u".ASS")
    self._to_transcript_checkbox = wx.CheckBox(mainpanel, self._TO_TRANSCRIPT_CHECKBOX_ID, u"Transcript")
    self._to_zip_checkbox = wx.CheckBox(mainpanel, self._TO_ZIP_CHECKBOX_ID, u"Zip it!")
    
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
    
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    main_sizer.Add(drop_sizer, 1, wx.EXPAND, 10)
    main_sizer.Add(cb_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

    mainpanel.SetSizer(main_sizer)
    
    self._main_notebook.AddPage(mainpanel, u'Tiny')
    self._main_notebook.AddPage(wx.Panel(self._main_notebook), u'Maxi')
    
    drop_text_target = DropBox(self)
    drop_text.SetDropTarget(drop_text_target)
    
    mainpanel_target = DropBox(self)
    mainpanel.SetDropTarget(mainpanel_target)
    
  def getFilesToBuild(self):
    """Return a tuple of the checkboxes values"""
    return (self._to_transcript_checkbox.IsChecked(), 
            self._to_srt_tag_checkbox.IsChecked(),
            self._to_srt_notag_checkbox.IsChecked(),
            self._to_ass_checkbox.IsChecked(), 
            self._to_zip_checkbox.IsChecked())
  
def main():
  class App(wx.App):
    def OnInit(self):
      frame = MainFrame()
      return True
  
  app = App(False)
  app.MainLoop()
  
if __name__ == '__main__':
  main()
  