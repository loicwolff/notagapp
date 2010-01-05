#!/usr/bin/env python
# encoding: utf-8

import os
import zipfile

import wx

from subtitle import SubtitleFile


class QuickDropbox(wx.FileDropTarget):
  """class managing when files are dropped onto the application"""

  def __init__(self, get_files_func):
    """Constructor
    @get_files_func: the function to retrieve which files to generate
    """
    super(QuickDropbox, self).__init__()
    self._archive = ""
    self._generated_files = set()
    self.get_files = get_files_func

  def OnDropFiles(self, x, y, files):
    do_transcript, do_srt_tag, do_srt_notag, do_ass, do_zip = self.get_files()

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


class SmartDropbox(wx.FileDropTarget):
  """class managing the file dropped to be processed"""

  def __init__(self, drop_statictext):
    super(SmartDropbox, self).__init__()
    self._drop_statictext = drop_statictext

  def OnDropFiles(self, x, y, files):
    if len(files) == 1:
      print(files[0])
      self._drop_statictext.SetLabel(files[0])
      self._drop_statictext.Wrap(20)
    else:
      print('smart mode')
