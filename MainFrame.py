#/usr/bin/env python
# -*- coding: utf-8 -*-

# python lib
import zipfile
import os

# external lib
import wx
from util.subtitle import SubtitleFile

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
    
  _to_ass_checkbox = None
  _to_srt_checkbox = None
  _to_transcript_checkbox = None
  _to_zip_checkbox = None
  
  def __init__(self):
    super(MainFrame, self).__init__(None, -1, u"NoTagApp", wx.DefaultPosition, wx.Size(510, 300), 
                        wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.CAPTION | wx.STAY_ON_TOP | wx.SYSTEM_MENU)
                        
    wx.InitAllImageHandlers()
    self._initControls()
    
    self._to_transcript_checkbox.SetFocus()
    self.SetMinSize(wx.Size(-1, 110))
    self.SetMaxSize(wx.Size(-1, 110))

    self.Center()
    self.Show(True)

  def _initControls(self):
    """create and initialize UI elements"""
    
    # Controls Initialization and showing of the form
    mainpanel = wx.Panel(self, self._MAIN_FRAME_ID)
    
    drop_text = wx.StaticText(mainpanel, wx.ID_ANY, u"Drop file(s) here")
    drop_text.SetWindowStyle(wx.CENTRE)
    drop_text.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    
    static_box = wx.StaticBox(mainpanel)
    drop_sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
    drop_sizer.Add(drop_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20)
    
    self._to_srt_tag_checkbox = wx.CheckBox(mainpanel, self._TO_SRT_TAG_CHECKBOX_ID, u"Tag")
    self._to_srt_notag_checkbox = wx.CheckBox(mainpanel, self._TO_SRT_NOTAG_CHECKBOX_ID, u"NoTag")
    self._to_ass_checkbox = wx.CheckBox(mainpanel, self._TO_ASS_CHECKBOX_ID, u"To ASS")
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
    
    static_box_target = DropFile(self)
    static_box.SetDropTarget(static_box_target)
    
    drop_text_target = DropFile(self)
    drop_text.SetDropTarget(drop_text_target)
    
  def getFilesToBuild(self):
    """Return a tuple of the checkboxes values"""
    return (self._to_transcript_checkbox.IsChecked(), 
            self._to_srt_tag_checkbox.IsChecked(),
            self._to_srt_notag_checkbox.IsChecked(),
            self._to_ass_checkbox.IsChecked(), 
            self._to_zip_checkbox.IsChecked())


class DropFile(wx.FileDropTarget):
  """class managing when files are dropped onto the application"""
  
  def __init__(self, parent):
    super(DropFile, self).__init__()
    self._parent = parent
    self._archive = ""
    self._generated_files = set()
      
  
  def OnDropFiles(self, x, y, files):
    do_transcript, do_srt_tag, do_srt_notag, do_ass, do_zip = self._parent.getFilesToBuild()
    
    for sub in files:
      srt = SubtitleFile(sub)
      
      # creating folder
      try:
        sub_dir = "%s/%s" % (srt.SubDir, srt.SubName)
        os.mkdir(sub_dir)
      except OSError:
        #TODO: print error to user
        pass

      if self._archive == "":
        self._archive = "%s/%s.zip" % (srt.SubDir, srt.SubName)
      
      if do_ass:
        srt.toASS(output_dir=sub_dir)
        self._generated_files.add(u"%s/%s.ass" % (sub_dir, srt.SubName))
      
      if do_srt_tag:
        srt.toSRT(keep_tag=True, output_dir=sub_dir)
        self._generated_files.add(u"%s/%s.TAG.srt" % (sub_dir, srt.SubName))
      
      if do_srt_notag:
        srt.toSRT(keep_tag=False, output_dir=sub_dir)
        self._generated_files.add(u"%s/%s.NOTAG.srt" % (sub_dir, srt.SubName))
          
      if do_transcript:
        srt.toTranscript(output_dir=sub_dir)
        self._generated_files.add(u"%s/%s." % (sub_dir, srt.SubName))
      
    if do_zip:
      zip_file = zipfile.ZipFile(self._archive, "w", zipfile.ZIP_DEFLATED)
      for gen in self._generated_files:
        if os.path.exists(gen):
          zip_file.write(str(gen), str(os.path.basename(gen)))
      zip_file.close()  
  
def main():
  class App(wx.App):
    def OnInit(self):
      frame = MainFrame()
      return True
  
  app = App(False)
  app.MainLoop()
  
if __name__ == '__main__':
  main()
  