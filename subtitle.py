#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
subtitle.py

Created by Loïc Wolff on 2009-04-28.
"""

from __future__ import with_statement
import re
import os
import codecs

import util.chardet as chardet # character detection lib

import k # constants

__author__ = u"Loïc Wolff <loicwolff (at) gmail.com>"


def remove_exotic_char(entry):
  """remove any exotic character from the text to make it more compatible"""
  no_tag_pattern = {u"œ": u"oe", u"Œ": u"Oe", u"Æ": u"Ae", u"æ": u"ae"}
  for key, value in no_tag_pattern.items():
    entry = entry.replace(key, value)
  return entry


def remove_tag(entry, alltag=False):
  """remove SRT and ASS tags
  if alltag, NoTagApp specials tag are removed too
  """
  tag_pattern = r"{.*?}|</?font.*?>|</?.*?>%s" % (r"|\[/?.?\]"
                  if alltag else "")

  return re.sub(tag_pattern, "", entry)


def to_nta_pattern(entry):
  """replace ASS and SRT specific tags by NoTagApp tags"""
  notagapp_pattern = { # italic tags
                       k.SRT_ITA_OPEN: k.NTA_ITA_OPEN,
                       k.SRT_ITA_CLOSE: k.NTA_ITA_CLOSE,
                       k.ASS_ITA_OPEN: k.NTA_ITA_OPEN,
                       k.ASS_ITA_CLOSE: k.NTA_ITA_CLOSE,
                       # bold tags
                       k.ASS_BOLD_OPEN: k.NTA_BOLD_OPEN,
                       k.ASS_BOLD_CLOSE: k.NTA_BOLD_CLOSE,
                       k.SRT_BOLD_OPEN: k.NTA_BOLD_OPEN,
                       k.SRT_BOLD_CLOSE: k.NTA_BOLD_CLOSE,
                       # underlined tags
                       k.ASS_UNDER_OPEN: k.NTA_UNDER_OPEN,
                       k.ASS_UNDER_CLOSE: k.NTA_UNDER_CLOSE,
                       k.SRT_UNDER_OPEN: k.NTA_UNDER_OPEN,
                       k.SRT_UNDER_CLOSE: k.NTA_UNDER_CLOSE}

  for key, value in notagapp_pattern.items():
    entry = entry.replace(key, value)

  return entry


def to_srt_pattern(entry, keep_tag=True):
  """change the ASS tags into SRT tags"""
  #entry = remove_exotic_char(entry)
  to_srt_tagged_pattern = { # italics tags
                            k.NTA_ITA_OPEN: k.SRT_ITA_OPEN,
                            k.NTA_ITA_CLOSE: k.SRT_ITA_CLOSE,
                            #bold tags
                            k.NTA_BOLD_OPEN: k.SRT_BOLD_OPEN,
                            k.NTA_BOLD_CLOSE: k.SRT_BOLD_CLOSE,
                            # underlined tags
                            k.NTA_UNDER_OPEN: k.SRT_UNDER_OPEN,
                            k.NTA_UNDER_CLOSE: k.SRT_UNDER_CLOSE}

  to_srt_pattern = { # italics tags
                     k.NTA_ITA_OPEN: k.SRT_ITA_OPEN,
                     k.NTA_ITA_CLOSE: k.SRT_ITA_CLOSE,
                     #bold tags
                     k.NTA_BOLD_OPEN: "",
                     k.NTA_BOLD_CLOSE: "",
                     # underlined tags
                     k.NTA_UNDER_OPEN: "",
                     k.NTA_UNDER_CLOSE: ""}

  for key, value in to_srt_tagged_pattern.items() if keep_tag \
                    else to_srt_pattern.items():
    entry = entry.replace(key, value)
  return entry


def to_ass_pattern(entry):
  """change the SRT tags into ASS tags"""
  to_ass_pattern = { # italics tags
                     k.NTA_ITA_OPEN: k.ASS_ITA_OPEN,
                     k.NTA_ITA_CLOSE: k.ASS_ITA_CLOSE,
                     # bold tags
                     k.NTA_BOLD_OPEN: k.ASS_BOLD_OPEN,
                     k.NTA_BOLD_CLOSE: k.ASS_BOLD_CLOSE,
                     # underlined tags
                     k.NTA_UNDER_OPEN: k.ASS_UNDER_OPEN,
                     k.NTA_UNDER_CLOSE: k.ASS_UNDER_CLOSE}

  for key, value in to_ass_pattern.items():
    entry = entry.replace(key, value)
  return entry


def parse_srt_timing(timing):
  """return a tuple of the start and end (hour, minute, sec and millis)
  of the timing matched from a SRT line
  """
  return re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> \
  (\d{2}):(\d{2}):(\d{2}),(\d{3})", timing).groups()


def parse_ass_timing(timing):
  """return a tuple of the start and end (hour, minute, sec and millis)
  of the timing matched from an ASS line
  """
  return re.match(r"Dialogue: 0,(\d{1,2}):(\d{2}):(\d{2}).(\d{2})," +
                  r"(\d{1,2}):(\d{2}):(\d{2}).(\d{2})," +
                  "Default,,0000,0000,0000,,\\w*", timing).groups()


def srt_to_ass_color(srt_color):
  return ""


def build_ass_header(font="Arial", fontsize="20"):
  """return a custom .ass header"""
  return u"""[Script Info]
Title: <untitled>
Original Script: <unknown>
ScriptType: v4.00+
PlayResX: 384
PlayResY: 288
PlayDepth: 0
Timer: 100.0
WrapStyle: 0

[v4+ Styles]
Format: Name, Fontname, Fontsize, \
PrimaryColour, SecondaryColour, OutlineColour, BackColour, \
Bold, Italic, Underline, StrikeOut, \
ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, \
MarginL, MarginR, MarginV, Encoding
Style: Default,%s,%s,&H00FFFFFF,&H00000000,&H00000000,&H00000000,\
0,0,0,0,100,100,0,0,1,2,0,2,15,15,15,0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" % (font, fontsize)


class SubtitleFile(object):
  """"""
  _subs = []
  _file = "" # full name
  _sub_name = "" # file name
  _sub_type = "" # .ext
  _sub_dir = "" # file directory

  def __init__(self, filename=None):
    if filename is not None:
      self._setFile(filename)

  def _parseSRT(self):
    """"""
    with codecs.open(self._file, "r", self._detectEncoding()) as sub:
      sub_entry = None
      index = 0

      for line in sub:
        line = re.sub(r"(\r\n|\n)", "", line).strip()
        if re.match(r"^\d+$", line): # index
          sub_entry = Subtitle()
        elif re.match(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", line): # timing
          index += 1
          sub_entry.Index = index
          sub_entry.StartTime, sub_entry.EndTime = Timing.parseSRT(line)
        elif line != "": # text
          if re.search(r"\{\\pos\(\d{1,4},\d{1,4}\)\}", line):
            sub_entry.Position = re.search(r"\{\\pos\((\d{1,4}),(\d{1,4})\)\}", line).groups()

          if re.search(r"{\\(?:fad|fade)\((\d{1,4}),(\d{1,4})\)}", line):
            sub_entry.Fade = re.search(r"{\\(?:fad|fade)\((\d{1,4}),(\d{1,4})\)}", line).groups()

          #cleaning up the processed line
          line = remove_exotic_char(line)
          line = to_nta_pattern(line)
          line = remove_tag(line)

          sub_entry.addLine(line)
        else: # empty line
          if sub_entry is not None:
            self._subs.append(sub_entry)
            sub_entry = None

  def _parseASS(self):
    """"""
    ass_line_pattern = re.compile(r"^Dialogue: 0,(\d):(\d{2}):(\d{2}).(\d{2})," +
                                  r"(\d):(\d{2}):(\d{2}).(\d{2}),Default,,0000,0000,0000,,(.*)$")
    with codecs.open(self._file, u"r", self._detectEncoding()) as sub:
      index = 0
      for line in sub:
        line = line.strip(r"\r\n").strip(r"\n")
        if re.search(ass_line_pattern, line):
          sub_entry = Subtitle()
          index += 1
          sub_entry.Index = index

          m = re.search(ass_line_pattern, line)
          start_hour, start_min, start_sec, start_millis, end_hour, end_min, end_sec, end_millis, text = m.groups()

          if re.search(r"{\\pos\(\d{1,4},\d{1,4}\)}", text):
            sub_entry.Position = re.search(r"{\\pos\((\d{1,4}),(\d{1,4})\)}", text).groups()

          if re.search(r"{\\(?:fad|fade)\((\d{1,4}),(\d{1,4})\)}", text):
            sub_entry.Fade = re.search(r"{\\(?:fad|fade)\((\d{1,4}),(\d{1,4})\)}", text).groups()

          # cleaning up
          text = to_nta_pattern(text)
          #text = remove_exotic_char(text)
          text = remove_tag(text)

          sub_entry.StartTime = Timing(start_hour, start_min, start_sec, start_millis)
          sub_entry.EndTime = Timing(end_hour, end_min, end_sec, end_millis)

          for item in text.split(r"\N"):
            sub_entry.addLine(item)

          self._subs.append(sub_entry)

  def _detectEncoding(self):
    """return the encoding of the file"""
    with open(self._file, 'r') as f:
      enc = chardet.detect("".join(f.readlines()))

    print enc['encoding']
    # windows-1255 is wrongfully detected when it's actually ISO-8859-1
    # same goes for ISO-8859-2
    if enc['encoding'] == 'windows-1255' or enc['encoding'] == 'ISO-8859-2':
      return 'ISO-8859-1'
    else:
      return enc['encoding']

  def _parseWeird(self):
    """"""
    with open(self._file, "r", ) as sub:
      sub_entry = None
      index = 0

      for line in sub:
        line = line.strip("\r\n").strip("\n")

        # match timing line
        if re.match(r"^TIMEIN: (.*):(.*):(.*):(.*)\tDURATION: (.*):(.*)\tTIMEOUT: (.*):(.*):(.*):(.*)$", line):
          index += 1
          sub_entry = Subtitle()
          sub_entry.Index = index
          sub_entry.StartTime, sub_entry.EndTime = Timing.parseWeird(line)
        # match text line
        elif line != "":
          if is_first_line:
            if sub_entry is not None:
              sub_entry.FirstLine = remove_exotic_char(line)
              is_first_line = False
          else:
            if sub_entry is not None:
              sub_entry.SecondLine = remove_exotic_char(line)
              is_first_line = True
              self._subs.append(sub_entry)
              sub_entry = None
        # match empty line
        else:
          if sub_entry is not None:
            is_first_line = True
            self._subs.append(sub_entry)
            sub_entry = None

  def toASS(self, output_file=None, output_dir=None):
    """Write the ASS file.
    The .ass extension is automaticaly added

    @output_file: the name of the file.
      if null, the name of the sub is used.
      -> default is None
    @output_dir: the name of the directory to put the subs,
      if empty, the current sub directory is used
      -> default is None
    """

    if output_dir is None:
      output_dir = self._sub_dir

    if output_file is None:
      output_file = self._sub_name

    with codecs.open(u"%s/%s.ass" % (output_dir, output_file), "w", "ISO-8859-1") as ass_file:
      header = build_ass_header()
      ass_file.write(header)

      for sub in self._subs:
        ass_file.write(u"Dialogue: 0,%s,%s,Default,,0000,0000,0000,,%s%s%s\n" %
                       (sub.StartTime.toASS(),
                        sub.EndTime.toASS(),
                        u"" if sub.Position is None else u"{\pos(%s,%s)}" % (sub.Position),
                        u"" if sub.Fade is None else u"{\fad(%s,%s)}" % (sub.Fade),
                        to_ass_pattern(r"\N".join(sub.Lines))))

  def toSRT(self, keep_tag=True, output_file=None, output_dir=None):
    """Write the SRT file.
    The TAG.srt or NOTAG.srt extensions are added automaticaly
    @keep_tag: specify if you want to remove the tags
    (except for <i>italics</i>)
      -> default is True
    @output_file: the name of the file.
      if null, the name of the sub is used.
      -> default is None
    @output_dir: the name of the directory to put the subs,
      if empty, the current sub directory is used
      -> default is None
    """

    if output_dir is None:
      output_dir = self._sub_dir

    if output_file is None:
      output_file = self._sub_name

    with codecs.open(u"%s/%s.%s.srt" % (
                        output_dir,
                        output_file,
                        "TAG" if keep_tag else "NOTAG"),
                        "w",
                        'ISO-8859-1') as output_file:

      for sub in self._subs:
        output_file.write(u"%d\n%s --> %s\n%s%s%s\n\n" % (
          sub.Index,
          sub.StartTime.toSRT(),
          sub.EndTime.toSRT(),
          "" if sub.Position is None or not keep_tag else u"{\pos(%s,%s)}" % (sub.Position),
          "" if sub.Fade is None or not keep_tag else u"{\fad(%s,%s)}" % (sub.Fade),
          to_srt_pattern("\n".join(sub.Lines), keep_tag)))

  def toTranscript(self, output_file=None, output_dir=None):
    """write the transcript of the subtitle
    the TRANSCRIPT.txt extension is added automaticaly
    @output_file: the name of the file.
      if null, the name of the sub is used.
      -> default is None
    @output_dir: the name of the directory to put the subs,
      if empty, the current sub directory is used
      -> default is None
    """

    if output_file is None:
      output_file = self._sub_name

    if output_dir is None:
      output_dir = self._sub_dir

    to_join = False
    with codecs.open("%s/%s.TRANSCRIPT.txt" % (output_dir, output_file), "w", 'ISO-8859-1') as transcript_file:
      for sub in self._subs:
        if to_join:
          transcript = transcript + " " + remove_tag("\n".join(sub.Lines), True)
        else:
          transcript = remove_tag("\n".join(sub.Lines), True)
        transcript = re.sub('^- ', '', transcript) # removing dialog
        transcript = re.sub('\n- ', '\n', transcript) # removing dialog on second line
        local_join = re.compile('[\w,]\n').search(transcript)
        if local_join:
          transcript = re.sub('\n', ' ', transcript)
        join = re.compile('[\w,]$').search(transcript)
        if join:
          to_join = True
          continue
        else:
          to_join = False
        transcript_file.write(transcript + "\n")

  def stats(self):
    """return a tuple with:
    > the number of subs
    > the number of lines
    > a report of too long lines:
      "sub.index: 1 / sub.line: 1 / sub.length: 42"
    """

    num_line = 0
    too_long_lines = []

    for sub in self._subs:
      num_line += len(sub.Lines)
      index = 0
      for line in sub.Lines:
        index += 1
        if len(remove_tag(line, True)) > 40:
          too_long_lines.append({'sub.index': sub.Index, 'sub.line': index, 'sub.length': len(line)})

    return {'num_subs': len(self._subs), 'num_line': num_line, 'too_long_lines': too_long_lines}

  # getters
  def _getFile(self):
    return self._file

  def _getSubs(self):
    return self._subs

  def _getSubName(self):
    return self._sub_name

  def _getSubType(self):
    return self._type

  def _getSubDir(self):
    return self._sub_dir

  # setters
  def _setFile(self, filename):
    if not os.path.exists(filename):
      raise IOError(u'File does not exist')
    self._file = filename
    self._sub_name, self._type = os.path.splitext(filename)
    self._sub_name = os.path.basename(self._sub_name)
    self._sub_dir = os.path.dirname(self._file)
    self._subs = []

    if self._type == u".srt":
      self._parseSRT()
    elif self._type == u".ass":
      self._parseASS()
    elif self._type == u".txt":
      self._parseWeird()

  # properties
  File = property(_getFile, _setFile)
  SubName = property(_getSubName)
  SubExt = property(_getSubType)
  SubDir = property(_getSubDir)
  Subs = property(_getSubs)


class Subtitle(object):
  """
  """

  def __init__(self):
    self._index = 0
    self._start_time = Timing()
    self._end_time = Timing()
    self._lines = []
    self._pos = None
    self._fade = None

  def __del__(self):
    self._index = 0
    self._start_time = None
    self._end_time = None
    self._lines = []
    self._pos = None
    self._fade = None

  def __str__(self):
    return u"from %s to %s%s%s\nlines:\n%s" % (
                self._start_time,
                self._end_time,
                "" if self._pos is None else u"\npos: %s, %s" % (self._pos),
                "" if self._fade is None else u"\nfade: %s, %s" % (self._fade),
                u"\n".join(self._lines))

  def addLine(self, line):
     self._lines.append(line)

  # getters
  def _getIndex(self):
    return self._index

  def _getStartTime(self):
    return self._start_time

  def _getEndTime(self):
    return self._end_time

  def _getPosition(self):
    return self._pos

  def _getFade(self):
    return self._fade

  def _getLines(self):
    return self._lines

  # setters
  def _setIndex(self, index):
    self._index = index

  def _setStartTime(self, timing):
    self._start_time = timing

  def _setEndTime(self, timing):
    self._end_time = timing

  def _setTimingLine(self, line):
    self._start_time, self._end_time = Timing.parse(line)

  def _setPosition(self, pos):
    self._pos = pos

  def _setFade(self, fade):
    self._fade = fade

  # properties
  Index = property(_getIndex, _setIndex)
  StartTime = property(_getStartTime, _setStartTime)
  EndTime = property(_getEndTime, _setEndTime)
  Lines = property(_getLines)
  Position = property(_getPosition, _setPosition)
  Fade = property(_getFade, _setFade)


class Timing(object):
  _millis = 0
  _sec = 0
  _min = 0
  _hour = 0

  @staticmethod
  def parseSRT(timing):
    timings = parse_srt_timing(timing)
    return (Timing(timings[0], timings[1], timings[2], timings[3]),
            Timing(timings[4], timings[5], timings[6], timings[7]))

  @staticmethod
  def parseASS(timing):
    timings = parse_ass_timing(timing)
    return (Timing(timings[0], timings[1], timings[2], timings[3]),
            Timing(timings[4], timings[5], timings[6], timings[7]))

  @staticmethod
  def parseWeird(timing):
    timings = parse_weird_timing(timing)

    start_time = end_time = Timing(timings[0], timings[1], timings[2], timings[3])
    millis, sec = timings[4:6]
    end_time.Millis += int(millis)
    if end_time.Millis >= 100:
      end_time.Sec += 1

    end_time.Sec += int(sec)
    if end_time.Sec >= 60:
      end_time.Min += 1

    if end_time.Min >= 60:
      end_time.Hour += 1

    return start_time, end_time

  def __init__(self, hour=0, min=0, sec=0, millis=0):
    self._millis = int(millis)
    self._sec = int(sec)
    self._min = int(min)
    self._hour = int(hour)
    self._type = type

  def toASS(self):
    return "%d:%.2d:%.2d.%s" % (
          self._hour,
          self._min,
          self._sec,
          str(self._millis)[0:2])

  def toSRT(self):
    return "%.2d:%.2d:%.2d,%.3d" % (
          self._hour,
          self._min,
          self._sec,
          self._millis)

  def __str__(self):
    return "%d:%d:%d,%d" % (self._hour, self._min, self._sec, self._millis)

  def values(self):
    return self._hour, self._min, self._sec, self._millis

  # getters
  def _getMillis(self):
    return self._millis

  def _getSec(self):
    return self._sec

  def _getMin(self):
    return self._min

  def _getHour(self):
    return self._hour

  def _getTime(self):
    """Return the timing in a tuple form"""
    return self._hour, self._min, self._sec, self._millis

  # setters
  def _setMillis(self, millis):
    self._millis = millis

  def _setSec(self, sec):
    self._sec = sec

  def _setMin(self, min):
    self._min = min

  def _setHour(self, hour):
    self._hour = hour

  # properties
  Millis = property(_getMillis, _setMillis)
  Sec = property(_getSec, _setSec)
  Min = property(_getMin, _setMin)
  Hour = property(_getHour, _setHour)
  Time = property(_getTime)


def test_lib():
  ass_sub = to_nta_pattern(u"{\i1}italic{\i0}")
  srt_sub = to_nta_pattern(u"<i>italic</i>")
  tag = remove_tag(u"{\font}<i>{\i0}</i>[i][/i][b][/b][u][/u]<u></u></b><b>", True)
  exotic = remove_exotic_char(u"œŒÆæ")

  assert ass_sub == u"[i]italic[/i]", ass_sub
  assert srt_sub == u"[i]italic[/i]", srt_sub
  assert tag == u"", tag
  assert exotic == u"oeOeAeae", exotic

if __name__ == "__main__":
  test_lib()
