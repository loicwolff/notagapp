#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""subtitle management lib"""

from __future__ import with_statement
import re
import os
import codecs

import util.chardet as chardet  # character detection lib
import k  # constants

__author__ = u"dex <loicwolff (at) gmail.com>, bean <bean (at) subtitles.toh.info>"

# misc constants
NEWLINE = u"\r\n"
ENCODING = "windows-1252"
DEBUG_MODE = False


def remove_exotic_char(entry):
  ret = ""
  for c in entry:
    if ord(c) < 255:
      ret += c

def replace_exotic_char(entry):
  """remove any exotic character from the text to make it more compatible"""
  no_tag_pattern = {u"œ": u"oe", u"": u"oe", u"Œ": u"Oe", u"Æ": u"Ae", u"æ": u"ae"}
  for key, value in no_tag_pattern.items():
    entry = entry.replace(key, value)
  return entry


def remove_tag(entry, alltag=False):
  """remove SRT and ASS tags
  if alltag, NoTagApp specials ([b]/[i]/[u]) tag are removed too
  """
  tag_pattern = r"{\\.*?}|</?font.*?>|</?.*?>"

  if alltag:
    tag_pattern += r"|\[/?.?\]"

  return re.sub(tag_pattern, "", entry)


def strip_line_ending(line):
  return line.strip('\r\n').strip('\n')


def to_nta_pattern(entry):
  """replace ASS and SRT specific tags by NoTagApp tags"""
  notagapp_pattern = {  # italic tags
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


def to_srt_pattern(entry, notag=False):
  """change the NTA tags into SRT tag
  if <code>notag</code>, bold and underlined tags are not added
  """
  to_srt_pattern = {  # italics tags
                      k.NTA_ITA_OPEN: k.SRT_ITA_OPEN,
                      k.NTA_ITA_CLOSE: k.SRT_ITA_CLOSE,
                      #bold tags
                      k.NTA_BOLD_OPEN: '' if notag else k.SRT_BOLD_OPEN,
                      k.NTA_BOLD_CLOSE: '' if notag else k.SRT_BOLD_CLOSE,
                      # underlined tags
                      k.NTA_UNDER_OPEN: '' if notag else k.SRT_UNDER_OPEN,
                      k.NTA_UNDER_CLOSE: '' if notag else k.SRT_UNDER_CLOSE}

  for key, value in to_srt_pattern.items():
    entry = entry.replace(key, value)

  return entry if notag else replace_exotic_char(entry)


def to_ass_pattern(entry):
  """change the SRT tags into ASS tags"""
  to_ass_pattern = {  # italics tags
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
  return re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> " +
                  r"(\d{2}):(\d{2}):(\d{2}),(\d{3})", timing).groups()


def parse_ass_timing(timing):
  """return a tuple of the start and end (hour, minute, sec and millis)
  of the timing matched from an ASS line
  """
  return re.match(r"Dialogue: 0,(\d{1,2}):(\d{2}):(\d{2}).(\d{2})," +
                  r"(\d{1,2}):(\d{2}):(\d{2}).(\d{2})," +
                  "Default,,0000,0000,0000,,\\w*", timing).groups()


def srt_to_ass_color(srt_color):
  return ""


def build_ass_header(font="Arial", fontsize=20, bold=False, italic=False, underlined=False):
  """return a custom .ass header"""
  return k.ASS_HEADER % (font, fontsize, bold, italic, underlined)


class SubtitleFile(object):
  """"""

  _subs = []
  _file = "" # full name
  _sub_name = "" # file name
  _sub_type = "" # .ext
  _sub_dir = "" # file directory

  _pos_pattern = r"\{\\pos\((\d{1,4}),(\d{1,4})\)\}"
  _pos_screen_pattern = r"{\\a(1|2|3|5|11)}"
  _fade_pattern = r"{\\fad\((\d{1,4}),(\d{1,4})\)}"

  def __init__(self, filename=None):
    if filename:
      self._setFile(filename)

  def _parseSRT(self):
    """"""
    with codecs.open(self._file, "r", 'windows-1252') as sub:
      sub_entry = None
      index = 0

      for line in sub:
        line = strip_line_ending(line)
        if re.match(r"^[0-9]+$", line):
          # index
          debug('index: "%s"' % line)
          sub_entry = Subtitle()
        elif re.match(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", line):
          # timing
          debug('timing: "%s"' % line)
          index += 1
          sub_entry.Index = index
          sub_entry.StartTime, sub_entry.EndTime = Timing.parseSRT(line)
        elif line != "":
          # text
          debug('text: "%s"' % line)
          if re.search(self._pos_pattern, line):
            sub_entry.Position = re.search(self._pos_pattern, line).groups()

          if re.search(self._pos_screen_pattern, line):
            sub_entry.ScreenPosition = re.search(self._pos_screen_pattern, line).group(1)

          if re.search(self._fade_pattern, line):
            sub_entry.Fade = re.search(self._fade_pattern, line).groups()

          #cleaning up the processed line
          line = to_nta_pattern(line)
          line = remove_tag(line)
          if not sub_entry:
            sub_entry = Subtitle()
            sub_entry.addLine(line)
            
        else:
          # empty line
          debug('empty line')
          if sub_entry is not None:
            self._subs.append(sub_entry)
            sub_entry = None

  def _parseASS(self):
    ass_pattern = r"^Dialogue: 0,(\d):(\d{2}):(\d{2}).(\d{2}),(\d):(\d{2}):(\d{2}).(\d{2}),Default,,0000,0000,0000,,(.*)$"
    ass_line_pattern = re.compile(ass_pattern)

    with codecs.open(self._file, u"r", 'windows-1252') as sub:
      index = 0
      for line in sub:
        line = line.strip(r"\r\n").strip(r"\n")
        if re.search(ass_line_pattern, line):
          sub_entry = Subtitle()
          index += 1
          sub_entry.Index = index

          m = re.search(ass_line_pattern, line)
          start_hour, start_min, start_sec, start_millis, end_hour, end_min, end_sec, end_millis, text = m.groups()

          if re.search(self._pos_pattern, text):
            sub_entry.Position = re.search(self._pos_pattern, text).groups()

          if re.search(self._pos_screen_pattern, line):
            sub_entry.ScreenPosition = re.search(self._pos_screen_pattern, line).group(1)

          if re.search(self._fade_pattern, text):
            sub_entry.Fade = re.search(self._fade_pattern, text).groups()

          # cleaning up
          text = to_nta_pattern(text)
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

    debug(enc['encoding'])
    # windows-1255 and ISO-8859-2 are wrongfully detected for windows-1252
    if enc['encoding'] == 'windows-1255' or enc['encoding'] == 'ISO-8859-2' or enc['encoding'] == 'ISO-8859-1':
      return 'windows-1252'
    else:
      return enc['encoding']

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
    else:
      if not os.path.exists(output_dir):
        debug("creating directory: %s" % output_dir)
        os.makedirs(output_dir)

    if output_file is None:
      output_file = self._sub_name

    with codecs.open(u"%s/%s.ass" % (output_dir, output_file), "w", "windows-1252") as ass_file: #ISO-8859-1
      header = build_ass_header()
      ass_file.write(header)

      for sub in self._subs:
        if not sub.isEmpty():
          ass_file.write(sub.toASS() + u"\r\n")

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
    else:
      if not os.path.exists(output_dir):
        debug("creating directory: %s" % output_dir)
        os.makedirs(output_dir)

    if output_file is None:
      output_file = self._sub_name

    out = u"%s/%s.%s.srt" % (output_dir, output_file, "TAG" if keep_tag else "NOTAG")

    with codecs.open(out, "w", 'windows-1252') as output_file:
      sub_index = 1
      for sub in self._subs:
        if not sub.isEmpty():
          sub.Index = sub_index
          output_file.write(sub.toSRT(keep_tag) + NEWLINE + NEWLINE)
          sub_index += 1

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
    with codecs.open("%s/%s.TRANSCRIPT.txt" % (output_dir, output_file), "w", 'windows-1252') as transcript_file:
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

  def sanitize(self, input_file, output_file, outdir):
    """remove any character not in the extended ASCII table
    """
    print("%s/%s.CLEAN.srt" % (outdir, output_file))
    print(input_file)
    
    with codecs.open("%s/%s.CLEAN.srt" % (outdir, output_file), "w", 'utf-8') as sanitized:
      with codecs.open(input_file, 'r', 'utf-8') as to_sanitize:
        for line in to_sanitize:
          for c in line:
            if ord(c) <= 255:
              sanitized.write(c)

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

  # properties
  File = property(lambda self: self._file, _setFile)
  SubName = property(lambda self: self._sub_name)
  SubExt = property(lambda self: self._sub_type)
  SubDir = property(lambda self: self._sub_dir)
  Subs = property(lambda self: self._subs)


class Subtitle(object):
  """Representes a subtitle
  > The Index
  > 2 Timing (Start / End)
  > The Text
  """

  def __init__(self):
    self._index = 0
    self._start_time = Timing()
    self._end_time = Timing()
    self._lines = []
    self._pos = None
    self._screen_pos = None
    self._fade = None

  def __del__(self):
    self._index = 0
    self._start_time = None
    self._end_time = None
    self._lines = []
    self._pos = None
    self._fade = None

  def __str__(self):
    return u"from %s to %s%s%s\nlines:\r\n%s" % (
                self._start_time,
                self._end_time,
                "" if self._pos is None else u"\npos: %s, %s" % (self._pos),
                "" if self._fade is None else u"\nfade: %s, %s" % (self._fade),
                u"\n".join(self._lines))

  def __unicode__(self):
    return u"from %s to %s%s%s\nlines:\r\n%s" % (
                self._start_time,
                self._end_time,
                "" if self._pos is None else u"\npos: %s, %s" % (self._pos),
                "" if self._fade is None else u"\nfade: %s, %s" % (self._fade),
                u"\n".join(self._lines))

  def toSRT(self, keep_tag=True):
    """return the .SRT version of the sub"""
    ret = u"%s\r\n" % self._index
    ret += u"%s --> %s\r\n" % (self._start_time.toSRT(), self._end_time.toSRT())
    if keep_tag:
      if self._screen_pos:
        ret += u"{\\a%s}" % self._screen_pos
      if self._pos:
        ret += u"{\\pos(%s,%s)}" % self._pos
      if self._fade:
        ret += u"{\\fad(%s,%s)}" % self._fade
    ret += to_srt_pattern("\r\n".join(self._lines), keep_tag)
    return ret

  def toASS(self):
    """return the .ASS version of the sub"""
    ret = u"Dialogue: 0,"
    ret += self._start_time.toASS()
    ret += u","
    ret += self._end_time.toASS()
    ret += u",Default,,0000,0000,0000,,"
    if self._screen_pos:
      ret += u"{\\a%s}" % self._screen_pos
    if self._pos:
      ret += u"{\\pos(%s,%s)}" % self._pos
    if self._fade:
      ret += u"{\\fad(%s,%s)}" % self._fade
    ret += to_ass_pattern(u"\\N".join(self._lines))
    return ret

  def addLine(self, line):
    self._lines.append(line)

  def isEmpty(self):
    return not self._lines or remove_tag(self._lines[0], True) == ""

  # properties

  def Index():
    def fget(self):
      return self._index
    def fset(self, value):
      self._index = value
    def fdel(self):
      del self._index
    return locals()
  Index = property(**Index())

  def StartTime():
    def fget(self):
      return self._start_time
    def fset(self, value):
      self._start_time = value
    def fdel(self):
      del self._start_time
    return locals()
  StartTime = property(**StartTime())

  def EndTime():
    def fget(self):
      return self._end_time
    def fset(self, value):
      self._end_time = value
    def fdel(self):
      del self._end_time
    return locals()
  EndTime = property(**EndTime())

  def Position():
    def fget(self):
      return self._pos
    def fset(self, value):
      self._pos = value
    def fdel(self):
      del self._pos
    return locals()
  Position = property(**Position())

  def ScreenPosition():
    def fget(self):
      return self._screen_pos
    def fset(self, value):
      self._screen_pos = value
    def fdel(self):
      del self._screen_pos
    return locals()
  ScreenPosition = property(**ScreenPosition())

  def Fade():
    doc = "The Fade property."
    def fget(self):
      return self._fade
    def fset(self, value):
      self._fade = value
    def fdel(self):
      del self._fade
    return locals()
  Fade = property(**Fade())

  Lines = property(lambda self: self._lines)


class Timing(object):
  """Represent a subtitle start or end time.
  Stores the Hour, Minute, Sec and Millis.
  Can convert itself from SRT to SRT and vice versa.
  """

  def __init__(self, hour=0, minute=0, sec=0, millis=0):
    self._millis = int(millis)
    self._sec = int(sec)
    self._min = int(minute)
    self._hour = int(hour)

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

  def toASS(self):
    """build the ass timing line"""
    millis = str("%.3d" % self._millis) if self._millis < 100 else str(self._millis)

    return "%1d:%02d:%02d.%s" % (
          self._hour,
          self._min,
          self._sec,
          millis[0:2])

  def toSRT(self):
    """build the srt timing line"""
    return "%02d:%02d:%02d,%03d" % (
          self._hour,
          self._min,
          self._sec,
          self._millis)

  def __str__(self):
    return "%d:%d:%d,%d" % (self._hour, self._min, self._sec, self._millis)

  def __add__(a, b):
    """add two timing together, taking care of incrementing the next property"""
    hour = a._hour + b._hour
    minute = a._min + b._min
    sec = a._sec + b._sec
    millis = a._millis + b._millis

    if millis > 999:
      sec += 1
      millis = millis % 1000
    if sec > 59:
      minute += 1
      sec = sec % 60
    if minute > 59:
      hour += 1
      minute = minute % 60
    return Timing(hour, minute, sec, millis)

  def __sub__(a, b):
    """substract two timing together, flooring to zero when necessary"""
    hour = a._hour - b._hour
    minute = a._min - b._min
    sec = a._sec - b._sec
    millis = a._millis - b._millis

    if millis < 0:
      millis = 1000 - abs(millis)
      sec -= 1
    if sec < 0:
      sec = 60 - abs(sec)
      minute -= 1
    if minute < 0:
      minute = 60 - abs(minute)
      hour -= 1
    if hour < 0:
      hour = minute = sec = millis = 0
    return Timing(hour, minute, sec, millis)

  def __lt__(a, b):
    """return True if a < b, False, otherwise"""
    if a._hour < b._hour:
      return True
    if a._hour > b._hour:
      return False
    if a._min < b._min:
      return True
    if a._min > b._min:
      return False
    if a._sec < b._sec:
      return True
    if a._sec > b._sec:
      return False
    if a._millis < b._millis:
      return True
    return False

  def values(self):
    return self._hour, self._min, self._sec, self._millis

  # properties

  def Hour():
    def fget(self):
      return self._hour
    def fset(self, value):
      self._hour = str('%02d' % int(value))
    def fdel(self):
      del self._hour
    return locals()
  Hour = property(**Hour())

  def Minute():
    def fget(self):
      return self._min
    def fset(self, value):
      self._min = str('%02d' % int(value))
    def fdel(self):
      del self._min
    return locals()
  Minute = property(**Minute())

  def Second():
    def fget(self):
      return self._sec
    def fset(self, value):
      self._sec = str('%02d' % int(value))
    def fdel(self):
      del self._sec
    return locals()
  Second = property(**Second())

  def Millis():
    def fget(self):
      return self._millis
    def fset(self, value):
      self._millis = str('%03d' % int(value))
    def fdel(self):
      del self._millis
    return locals()
  Millis = property(**Millis())

  Time = property(lambda self: list(self._hour, self._min, self._sec, self._millis))


def debug(out):
  if DEBUG_MODE:
    print(out)


def test_lib():
  ass_sub = to_nta_pattern(u"{\i1}italic{\i0}")
  srt_sub = to_nta_pattern(u"<i>italic</i>")
  tag = remove_tag(u'{\\font}<i>{\\a1}{\\i0}</i>[i][/i][b][/b][u][/u]<u></u></b><b>', True)
  exotic = replace_exotic_char(u"œŒÆæ")

  assert ass_sub == u"[i]italic[/i]", ass_sub
  assert srt_sub == u"[i]italic[/i]", srt_sub
  assert tag == u"", tag
  assert exotic == u"oeOeAeae", exotic


def test_timing():
  t = Timing(hour=123, minute=12, sec=13, millis=14)
  print "t.values() ->", t.values()
  print "toASS ->", t.toASS()
  print "toSRT ->", t.toSRT()
  t1 = Timing(hour=001, minute=10, sec=10, millis=100)
  t2 = Timing(hour=001, minute=5, sec=5, millis=50)
  t2 = Timing(hour=001, minute=5, sec=55, millis=950)
  print "t1 ->", t1
  print "t2 ->", t2
  print "t1 + t2 ->", (t1 + t2).toSRT()
  print "t1 - t2 ->", (t1 - t2).toSRT()
  print "t1 < t2 ->", (t1 < t2)

if __name__ == "__main__":
  test_timing()
  test_lib()
