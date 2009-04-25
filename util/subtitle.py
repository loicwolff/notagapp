#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import re
import os

__author__ = "Loïc Wolff <loicwolff (at) gmail.com"

# tag constants
NTA_ITA_OPEN = "[i]"
NTA_ITA_CLOSE = "[/i]"
ASS_ITA_OPEN  = "{\i1}"
ASS_ITA_CLOSE = "{\i0}"
SRT_ITA_OPEN = "<i>"
SRT_ITA_CLOSE = "</i>"

NTA_BOLD_OPEN = "[b]"
NTA_BOLD_CLOSE = "[/b]"
ASS_BOLD_OPEN  = r"{\b1}"
ASS_BOLD_CLOSE = r"{\b0}"
SRT_BOLD_OPEN = "<b>"
SRT_BOLD_CLOSE = "</b>"

NTA_UNDER_OPEN = "[u]"
NTA_UNDER_CLOSE = "[/u]"
ASS_UNDER_OPEN  = "{\u1}"
ASS_UNDER_CLOSE = "{\u0}"
SRT_UNDER_OPEN = "<u>"
SRT_UNDER_CLOSE = "</u>"

# file extensions
SRT = "srt"
ASS = "ass"

def removeExoticChar(entry):
  """remove any exotic character from the text to make it more compatible"""
  no_tag_pattern = { "œ":"oe", "Œ":"Oe", "Æ":"Ae", "æ":"ae" }
  for key, value in no_tag_pattern.items():
    entry = re.sub(key, value, entry)
  return entry

def removeTag(entry, alltag=False):
  """remove SRT and ASS tags
  if alltag, NoTagApp specials tag are removed too
  """
  tag_pattern = r"{.*?}|</?font.*?>|</?.*?>%s" % (r"|\[/?.?\]" if alltag else "")
  
  return re.sub(tag_pattern, "", entry)

def toNoTagAppPattern(entry):
  """replace ASS and SRT specific tags by NoTagApp tags"""
  notagapp_pattern = { # italic tags
                       SRT_ITA_OPEN:NTA_ITA_OPEN,
                       SRT_ITA_CLOSE:NTA_ITA_CLOSE,
                       ASS_ITA_OPEN :NTA_ITA_OPEN,
                       ASS_ITA_CLOSE:NTA_ITA_CLOSE,
                       # bold tags
                       ASS_BOLD_OPEN :NTA_BOLD_OPEN,
                       ASS_BOLD_CLOSE:NTA_BOLD_CLOSE,
                       SRT_BOLD_OPEN:NTA_BOLD_OPEN,
                       SRT_BOLD_CLOSE:NTA_BOLD_CLOSE,
                       # underlined tags
                       ASS_UNDER_OPEN :NTA_UNDER_OPEN,
                       ASS_UNDER_CLOSE:NTA_UNDER_CLOSE,
                       SRT_UNDER_OPEN:NTA_UNDER_OPEN,
                       SRT_UNDER_CLOSE:NTA_UNDER_CLOSE }
  
  for key, value in notagapp_pattern.items():
    entry = entry.replace(key, value)
  
  return entry

def toSRTPattern(entry, keep_tag=True):
  """change the SSA tags into SRT tags"""
  to_srt_tagged_pattern = { # italics tags
                            NTA_ITA_OPEN:SRT_ITA_OPEN,
                            NTA_ITA_CLOSE:SRT_ITA_CLOSE,     
                            #bold tags                       
                            NTA_BOLD_OPEN:SRT_BOLD_OPEN,     
                            NTA_BOLD_CLOSE:SRT_BOLD_CLOSE,   
                            # underlined tags                
                            NTA_UNDER_OPEN:SRT_UNDER_OPEN,   
                            NTA_UNDER_CLOSE:SRT_UNDER_CLOSE  
  }
                     
  to_srt_pattern = { # italics tags
                     NTA_ITA_OPEN:SRT_ITA_OPEN,
                     NTA_ITA_CLOSE:SRT_ITA_CLOSE,
                     #bold tags
                     NTA_BOLD_OPEN:"",
                     NTA_BOLD_CLOSE:"",
                     # underlined tags
                     NTA_UNDER_OPEN:"",
                     NTA_UNDER_CLOSE:""
  }
  
  for key, value in to_srt_tagged_pattern.items() if keep_tag else to_srt_pattern.items():
    entry = entry.replace(key, value)
  return entry

def toSSAPattern(entry):
  """change the SRT tags into SSA tags"""
  to_ass_pattern = { # italics tags
                     NTA_ITA_OPEN:ASS_ITA_OPEN ,
                     NTA_ITA_CLOSE:ASS_ITA_CLOSE,
                     # bold tags
                     NTA_BOLD_OPEN:ASS_BOLD_OPEN ,
                     NTA_BOLD_CLOSE:ASS_BOLD_CLOSE,
                     # underlined tags
                     NTA_UNDER_OPEN:ASS_UNDER_OPEN ,
                     NTA_UNDER_CLOSE:ASS_UNDER_CLOSE
                     }
  
  for key, value in to_ass_pattern.items():
    entry = entry.replace(key, value)
  return entry

def parseSRTTiming(timing):
  """return a tuple of the start and end (hour, minute, sec and millis)
  of the timing matched from a SRT line
  """
  return re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})", timing).groups()

def parseSSATiming(timing):
  """return a tuple of the start and end (hour, minute, sec and millis)
  of the timing matched from an SSA line
  """
  return re.match(r"Dialogue: 0,(\d{1,2}):(\d{2}):(\d{2}).(\d{2})," +
                  r"(\d{1,2}):(\d{2}):(\d{2}).(\d{2}),Default,,0000,0000,0000,,\w*", timing).groups()

def parseWeirdTiming(timing):
  """return a tuple of the start time, the length of the subtitle"""
  return re.match(r"^TIMEIN: (.*):(.*):(.*):(.*)\tDURATION: (.*):(.*)\tTIMEOUT: .*:.*:.*:.*$", timing).groups()


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
    with open(self._file, "r") as sub:
      sub_entry = None
      index = 0
      
      for line in sub:
        line = re.sub("(\r\n|\n)", "", line).strip()
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
          line = removeExoticChar(line)
          line = toNoTagAppPattern(line)
          line = removeTag(line)
          
          sub_entry.addLine(line)
        else: # empty line
          if sub_entry is not None:
            self._subs.append(sub_entry)
            sub_entry = None
  
  def _parseSSA(self):
    """"""
    ass_line_pattern = re.compile(r"^Dialogue: 0,(\d):(\d{2}):(\d{2}).(\d{2})," +
                                  r"(\d):(\d{2}):(\d{2}).(\d{2}),Default,,0000,0000,0000,,(.*)$")
    with open(self._file, "r") as sub:
      index = 0
      for line in sub:
        line = line.strip("\r\n").strip("\n")
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
          text = toNoTagAppPattern(text)
          text = removeExoticChar(text)
          text = removeTag(text)
          
          sub_entry.StartTime = Timing(start_hour, start_min, start_sec, start_millis)
          sub_entry.EndTime = Timing(end_hour, end_min, end_sec, end_millis)
          
          for item in text.split("\N"):
            sub_entry.addLine(item)
          
          self._subs.append(sub_entry)
          
  
  def _parseWeird(self):
    """"""
    with open(self._file, "r") as sub:
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
              sub_entry.FirstLine = removeExoticChar(line)
              is_first_line = False
          else:
            if sub_entry is not None:
              sub_entry.SecondLine = removeExoticChar(line)
              is_first_line = True
              self._subs.append(sub_entry)
              sub_entry = None
        # match empty line
        else:
          if sub_entry is not None:
            is_first_line = True
            self._subs.append(sub_entry)
            sub_entry = None
  
  def toSSA(self):
    """"""
    with open("%s/%s.%s" % (self._sub_dir, self._sub_name, SSA), "w") as output_file:
      header = """[Script Info]
Title: <untitled>
Original Script: <unknown>
ScriptType: v4.00+
PlayResX: 384
PlayResY: 288
PlayDepth: 0
Timer: 100.0
WrapStyle: 0

[v4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H00000000,&H00000000,&H00000000,
0,0,0,0,100,100,0,0,1,2,0,2,15,15,15,0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"""
      output_file.write(header)
      
      for sub in self._subs:
        output_file.write("Dialogue: 0,%s,%s,Default,,0000,0000,0000,,%s%s%s\n" % (
                            sub.StartTime.toSSA(),
                            sub.EndTime.toSSA(),
                            "" if sub.Position is None else r"{\pos(%s,%s)}" % (sub.Position),
                            "" if sub.Fade is None else r"{\fad(%s,%s)}" % (sub.Fade),
                            toSSAPattern("\N".join(sub.Lines))))
  
  def toTranscript(self):
    """write the transcript of the subtitle"""

    to_join = False
    with open("%s/%s.TRANSCRIPT.txt" % (self._sub_dir, self._sub_name), "w") as output_file:
      for sub in self._subs:
        if to_join:
          transcript = transcript + " " + removeTag("\n".join(sub.Lines), True)
        else:
          transcript = removeTag("\n".join(sub.Lines), True)
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
        output_file.write(transcript + "\n")
        
  def toSRT(self, keep_tag):
    """generate an SRT file
    if keep_tag is False, the position and format tags, except the italics, are removed
    """
    
    with open("%s/%s.%s.%s" % (self._sub_dir, self._sub_name, "TAG" if keep_tag else "NOTAG", SRT), "w") as output_file:
      for sub in self._subs:
        output_file.write("%d\n%s --> %s\n%s%s%s\n\n" % (
          sub.Index,
          sub.StartTime.toSRT(),
          sub.EndTime.toSRT(),
          "" if sub.Position is None or not keep_tag else "{\pos(%s,%s)}" % (sub.Position),
          "" if sub.Fade is None or not keep_tag else "{\fad(%s,%s)}" % (sub.Fade),
          toSRTPattern("\n".join(sub.Lines), keep_tag)))
  
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
        if len(removeTag(line, True)) > 40:
          too_long_lines.append("sub.index: %s / sub.line: %s / sub.length: %s\n" % (sub.Index, index, len(line)))

    return len(self._subs), num_line, too_long_lines
  
  def _isSubtitle(self, filename):
    if filename[-4:] == u".srt":
      self._type = SRT_FILE
    elif filename[-4:] == u".ass":# or file[-4:] == u".ssa":
      self._type = SSA_FILE
    elif filename[-4:] == ".txt":
      self._type = WEIRD_FILE
    else:
      return False
    return True
  
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
    self._file = filename
    self._sub_name, self._type = os.path.splitext(filename)
    self._sub_name = os.path.basename(self._sub_name)
    self._sub_dir = os.path.dirname(self._file)
    self._subs = []
    
    if self._type == u".srt":
      self._parseSRT()
    elif self._type == u".ass":# or u".ssa":
      self._parseSSA()
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
    
  def addLine(self, line):
    self._lines.append(line)
  
  def __str__(self):
    return "from %s to %s%s%s\nlines:\n%s" % (
                self._start_time,
                self._end_time,
                "" if self._pos is None else "\npos: %s, %s" % (self._pos),
                "" if self._fade is None else "\nfade: %s, %s" % (self._fade),
                "\n".join(self._lines)
                )
  
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
    timings = parseSRTTiming(timing)
    return (Timing(timings[0], timings[1], timings[2], timings[3]),
            Timing(timings[4], timings[5], timings[6], timings[7]))
  
  @staticmethod
  def parseSSA(timing):
    timings = parseSSATiming(timing)
    return (Timing(timings[0], timings[1], timings[2], timings[3]),
            Timing(timings[4], timings[5], timings[6], timings[7]))
  
  @staticmethod
  def parseWeird(timing):
    timings = parseWeirdTiming(timing)
    
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
  
  def __init__(self, hour = 0, min = 0, sec = 0, millis = 0):
    self._millis = int(millis)
    self._sec = int(sec)
    self._min = int(min)
    self._hour = int(hour)
    self._type = type
  
  def toSSA(self):
    return "%d:%.2d:%.2d.%.2d" % (
          self._hour,
          self._min,
          self._sec,
          int(str(self._millis)[0:2]))
  
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
  ass_sub = toNoTagAppPattern("{\i1}italic{\i0}")
  srt_sub = toNoTagAppPattern("<i>italic</i>")
  tag = removeTag("{\font}<i>{\i0}</i>[i][/i][b][/b][u][/u]<u></u></b><b>", False)
  exotic = removeExoticChar("œŒÆæ")
  
  assert ass_sub == "[i]italic[/i]", ass_sub
  assert srt_sub == "[i]italic[/i]", srt_sub
  assert tag == "", tag
  assert exotic == "oeOeAeae", exotic

if __name__ == "__main__":
  SUBS_DIR = "/Users/dex/Development/Python/NoTagApp/subs"
  
  if True:
    s = SubtitleFile()
    s.File = "/Users/dex/Desktop/My.Name.Is.Earl.423.lol.VF.srt"
    
    for sub in s.Subs:
      print removeTag("".join(sub.Lines), True)
  
  if False:
    s = SubtitleFile()
    s.File = "%s/dollhouse.ass" % (SUBS_DIR)
    
    s.toTranscript()
    #s.toSRT(keep_tag=True)
    #s.toSRT(keep_tag=False)
    
    print(s.stats())
    
    #for sub in s.Subs:
    #  print(str(sub))
  
  if False:
    s = SubtitleFile()
    s.File = "%s/roe.srt" % (SUBS_DIR)
    
    s.toSSA()
    #s.toTranscript()
    
    print(s.stats())
    
    #for sub in s.Subs:
    #  print(str(sub))
  
  if False:
    test_lib()
    