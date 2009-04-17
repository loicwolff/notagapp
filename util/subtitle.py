#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import re

# filetype constants
SRT_FILE = 1
SSA_FILE = 2
WEIRD_FILE = 3

# tag constants
ITA_OPEN = r"[i]"
ITA_CLOSE = r"[/i]"
SSA_OPEN = r"{\i1}"
SSA_CLOSE = r"{\i0}"
SRT_OPEN = r"<i>"
SRT_CLOSE = r"</i>"

# file extensions
SRT = "srt"
SSA = "ssa" # "ass"?

def removeExoticChar(entry):
  """remove any exotic character from the text to make it more compatible"""
  no_tag_pattern = { "œ":"oe", "Œ":"Oe", "Æ":"Ae", "æ":"ae" }
  for key, value in no_tag_pattern.items():
    entry = re.sub(key, value, entry)
  return entry
  
def removeTag(entry, alltag=False):
  """remove SRT and SSA tags
  if alltag, NoTagApp specials tag are removed too
  """
  tag_pattern = r"{.*?}|</?font.*?>|</?.*?>%s" % (r"|\[/?.?\]" if alltag else "")
  
  return re.sub(tag_pattern, "", entry)
  
def toNoTagAppPattern(entry):
  """replace SSA and SRT specific tags by NoTagApp tags"""
  notagapp_pattern = { SRT_OPEN:ITA_OPEN,
                       SRT_CLOSE:ITA_CLOSE,
                       SSA_OPEN:ITA_OPEN, 
                       SSA_CLOSE:ITA_CLOSE }
                       
  for key, value in notagapp_pattern.items():
    entry = entry.replace(key, value)

  return entry
  
def toSRTPattern(entry):
  """change the SSA tags into SRT tags"""
  to_srt_pattern = { ITA_OPEN:SRT_OPEN, 
                     ITA_CLOSE:SRT_CLOSE#, 
                     #r"{\u1}":r"<u>", 
                     #r"{\u0}":r"</u>", 
                     #r"{\b1}":r"<b>", 
                     #r"{\b0}":r"</b>" 
                     }
  
  for key, value in to_srt_pattern.items():
    entry = entry.replace(key, value) 
  return entry
  
def toSSAPattern(entry):
  """change the SRT tags into SSA tags"""
  to_ssa_pattern = { ITA_OPEN:SSA_OPEN, 
                     ITA_CLOSE:SSA_CLOSE#, 
                     #r"<u>":r"{\u1}", 
                     #r"</u>":r"{\u0}", 
                     #r"<b>":r"{\b1}", 
                     #r"</b>":r"{\b0}" 
                     }
  
  for key, value in to_ssa_pattern.items():
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
  _file = ""
  _sub_name = ""
  _type = None

  def __init__(self, file=None):
    if file is not None:
      self._setFile(file)
    
  def _parseSRT(self):
    """"""
    
    with open(self._file, "r") as sub:
      sub_entry = None
      is_first_line = True

      for line in sub:
        line = line.strip("\r\n")
        # match index line
        if re.match(r"^\d+$", line):
          sub_entry = Subtitle()
          sub_entry.Index = int(line)
        # match timing line
        elif re.match(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", line):
          if sub_entry is not None:
            sub_entry.StartTime, sub_entry.EndTime = Timing.parseSRT(line)
        # match text line
        elif line != "":
          if re.search(r"\{\\pos\(\d{1,4},\d{1,4}\)\}", line):
            sub_entry.Position = re.match(r"\{\\pos\((\d{1,4}),(\d{1,4})\)\}", line).groups()
          
            if re.search(r"{(?:\\fad|fade)\((\d{1,4}),(\d{1,4})\)}", line):
              sub_entry.Fade = re.search(r"{(?:\\fad|fade)\((\d{1,4}),(\d{1,4})\)}", line).groups()
          
          #cleaning up the processed line
          line = toNoTagAppPattern(line)
          line = removeTag(line)
          
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

  def _parseSSA(self):
    """"""
    ssa_line_pattern = re.compile(r"^Dialogue: 0,(\d):(\d{2}):(\d{2}).(\d{2})," + 
                                  r"(\d):(\d{2}):(\d{2}).(\d{2}),Default,,0000,0000,0000,,(.*)$")
    with open(self._file, "r") as sub:
      index = 0
      for line in sub:
        line = line.strip("\r\n")
        if re.search(ssa_line_pattern, line):
          sub_entry = Subtitle()
          index += 1
          sub_entry.Index = index
          
          m = re.search(ssa_line_pattern, line)
          start_hour, start_min, start_sec, start_millis, end_hour, end_min, end_sec, end_millis, text = m.groups()
          
          if re.search(r"{\\pos\(\d{1,4},\d{1,4}\)}", text):
            sub_entry.Position = re.search(r"{\\pos\((\d{1,4}),(\d{1,4})\)}", text).groups()
          
          if re.search(r"{\\(?:fad|fade)\((\d{1,4}),(\d{1,4})\)}", text):
            sub_entry.Fade = re.search(r"{\\(?:fad|fade)\((\d{1,4}),(\d{1,4})\)}", text).groups()

          text = toNoTagAppPattern(text)
          text = removeExoticChar(text)
          text = removeTag(text)
          
          sub_entry.StartTime = Timing(start_hour, start_min, start_sec, start_millis)
          sub_entry.EndTime = Timing(end_hour, end_min, end_sec, end_millis)

          if (text.find("\N")) != -1:
            sub_entry.FirstLine, sub_entry.SecondLine = text.split("\N")
          else:
            sub_entry.FirstLine = text
          
          self._subs.append(sub_entry)
          
          
  def _parseWeird(self):
    """"""
    with open(self._file, "r") as sub:
      sub_entry = None
      is_first_line = True
      index = 0

      for line in sub:
        line = line.strip("\r\n")
        
        # match timing line
        if re.match("^TIMEIN: (.*):(.*):(.*):(.*)\tDURATION: (.*):(.*)\tTIMEOUT: (.*):(.*):(.*):(.*)$", line):
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
    with open("%s.%s" % (self._sub_name, SSA), "w") as output_file:
      output_file.write("[Script Info]\r\n")
      output_file.write("Title: <untitled>\r\n")
      output_file.write("Original Script: <unknown>\r\n")
      output_file.write("ScriptType: v4.00+\r\n")
      output_file.write("PlayResX: 384\r\n")
      output_file.write("PlayResY: 288\r\n")
      output_file.write("PlayDepth: 0\r\n")
      output_file.write("Timer: 100.0\r\n")
      output_file.write("WrapStyle: 0\r\n")
      output_file.write("\r\n")
      output_file.write("[v4+ Styles]\r\n")
      output_file.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, ")
      output_file.write("Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, ")
      output_file.write("Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\r\n")
      output_file.write("Style: Default,Arial,20,&H00FFFFFF,&H00000000,&H00000000,&H00000000,")
      output_file.write("0,0,0,0,100,100,0,0,1,2,0,2,15,15,15,0\r\n")
      output_file.write("\r\n")
      output_file.write("[Events]\r\n")
      output_file.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\r\n")

      for sub in self._subs:
        output_file.write("Dialogue: 0,%s,%s,Default,,0000,0000,0000,,%s%s%s%s\r\n" % (
                            sub.StartTime.toSSA(),
                            sub.EndTime.toSSA(),
                            "" if sub.Position is None else r"{\pos(%s,%s)}" % (sub.Position),
                            "" if sub.Fade is None else r"{\fad(%s,%s)}" % (sub.Fade),
                            toSSAPattern(sub.FirstLine),
                            "" if sub.SecondLine == "" else "\N%s" % (toSSAPattern(sub.SecondLine))))
    
  def toTranscript(self):
    """write the transcript of the subtitle"""
    
    with open("%s.TRANSCRIPT.txt" % (self._sub_name), "w") as output_file:
      for sub in self._subs:
       output_file.write("%s%s\r\n" % (
                          removeTag(sub.FirstLine, True), 
                          "" if sub.SecondLine == "" else "\r\n%s" % (removeTag(sub.SecondLine, True))))
  
  def toSRT(self, keep_tag):
    """generate an SRT file
    if keep_tag is at False, the position tags, 
    except the italics, are removed
    """
    
    with open("%s.%s.%s" % (self._sub_name, "TAG" if keep_tag else "NOTAG", SRT), "w") as output_file:
      for sub in self._subs: 
        output_file.write("%d\r\n%s --> %s\r\n%s%s%s%s\r\n\r\n" % (
          sub.Index,
          sub.StartTime.toSRT(),
          sub.EndTime.toSRT(),
          "" if sub.Position is None or not keep_tag else r"{\pos(%s,%s)}" % (sub.Position),
          "" if sub.Fade is None or not keep_tag else r"{\fad(%s,%s)}" % (sub.Fade),
          toSRTPattern(sub.FirstLine) if keep_tag else removeTag(sub.FirstLine, True),
          "" if sub.SecondLine == "" else "\r\n%s" % (toSRTPattern(sub.SecondLine) if keep_tag else removeTag(sub.SecondLine, True)))) 


  def stats(self):
    """return a tuple with:
    > the number of subs
    > the number of lines
    """
    
    num_line = 0
    for sub in self._subs:
      num_line += 1
      if sub.SecondLine != "":
        num_line += 1
    
    return len(self._subs), num_line

  def _isSubtitle(self, file):
    if file[-4:] == u".srt":
      self._type = SRT_FILE
    elif file[-4:] == u".ass" or file[-4:] == u".ssa":
      self._type = SSA_FILE
    elif file[-4:] == ".txt":
      self._type = WEIRD_FILE
    else:  
      return False
    return True
      
  # getters
  def _getFile(self):
    return self._file
      
  def _getSubs(self):
    return self._subs
  
  # setters
  def _setFile(self, file):
    if not self._isSubtitle(file) or not open(file, "r"):
      raise ValueError(u"Unable to open file or not a subtitle")
    else:
      self._file = file
      self._subs = []
      if self._type == SRT_FILE:
        self._sub_name = re.match(re.compile(r"(.*).srt"), file).group(1)
        self._parseSRT()
      elif self._type == SSA_FILE:
        self._sub_name = re.match(re.compile(r"(.*).ass|ssa"), file).group(1)
        self._parseSSA()
      elif self._type == WEIRD_FILE:
        self._sub_name = re.match(re.compile(r"(.*).txt"), file).group(1)
        self._parseWeird()

  # properties
  File = property(_getFile, _setFile)
  Subs = property(_getSubs)

class Subtitle(object):
  _index = 0
  _start_time = None
  _end_time = None
  _lines = ""
  _first_line = ""
  _second_line = ""
  _pos = None
  _fade = None
  
  def __init__(self):
    self._start_time = Timing()
    self._end_time = Timing()
  
  def __str__(self):
    return "from %s to %s%s%s\nline 1: %s%s" % (
                self._start_time,
                self._end_time,
                "" if self._pos is None else "\npos: %s, %s" % (self._pos),
                "" if self._fade is None else "\nfade: %s, %s" % (self._fade),
                self._first_line,
                "" if self._second_line == "" else "\nline 2: %s" % (self._second_line)
                )
  
  # getters
  def _getIndex(self):
    return self._index
      
  def _getStartTime(self):
    return self._start_time
  
  def _getEndTime(self):
    return self._end_time

  def _getFirstLine(self):
    return self._first_line
  
  def _getSecondLine(self):
    return self._second_line
    
  def _getPosition(self):
    return self._pos
  
  def _getFade(self):
    return self._fade
    
  def _getLines(self):
    if self._type == SRT_FILE:
      return "%s\r\n%s" % (self._first_line, self._second_line)
    else:
      return "%s\N%s" % (self._first_line, self._second_line)
          
  # setters
  def _setIndex(self, index):
    self._index = index
      
  def _setStartTime(self, timing):
    self._start_time = timing
  
  def _setEndTime(self, timing):
    self._end_time = timing
  
  def _setFirstLine(self, line):
    self._first_line = line
  
  def _setSecondLine(self, line):
    self._second_line = line
      
  def _setTimingLine(self, line):
    self._start_time, self._end_time = Timing.parse(line)
    
  def _setPosition(self, pos):
    self._pos = pos
    
  def _setFade(self, fad):
    self._fade = fad
    
  def raw(self):
    print("index:" + str(self._index))
    print("start: " + str(self._start_time))
    print("end: " + str(self._end_time))
    print("firstline: " + self._first_line)
    if self._second_line:
      print("secondline: " + self._second_line)
    print("pos: " + str(self._pos))
    print("fade: " + str(self._fade))
      
  # properties
  Index = property(_getIndex, _setIndex)
  StartTime = property(_getStartTime, _setStartTime)
  EndTime = property(_getEndTime, _setEndTime)
  Lines = property(_getLines)
  FirstLine = property(_getFirstLine, _setFirstLine)
  SecondLine = property(_getSecondLine, _setSecondLine)
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
    
  def raw(self):
    print("millis:" + str(self._millis))
    print(self._sec)
    print(self._min)
    print(self._hour)

  # properties
  Millis = property(_getMillis, _setMillis)
  Sec = property(_getSec, _setSec)
  Min = property(_getMin, _setMin)
  Hour = property(_getHour, _setHour)
  Time = property(_getTime)

def test_lib():
  ssa_sub = toNoTagAppPattern("{\i1}italic{\i0}")
  srt_sub = toNoTagAppPattern("<i>italic</i>")
  tag = removeTag("{\font}<i>{\i0}</i>[i][/i]", True)
  exotic = removeExoticChar("œŒÆæ")
  
  assert ssa_sub == "[i]italic[/i]", ssa_sub
  assert srt_sub == "[i]italic[/i]", srt_sub
  assert tag == "", tag
  assert exotic == "oeOeAeae", exotic
  
if __name__ == "__main__":
  SUBS_DIR = "/Users/dex/Development/Python/NoTagApp/subs"
  if True:
    s = SubtitleFile()
    s.File = "%s/dollhouse.ass" % (SUBS_DIR)

    #s.toTranscript() 
    s.toSRT(keep_tag=True)
    s.toSRT(keep_tag=False)
  
    #for sub in s.Subs:
    #  print(str(sub))
    #  sub.raw()

  if False:
    s = SubtitleFile()
    s.File = "%s/roe.srt" % (SUBS_DIR)

    s.toSSA(True)
    s.toTranscript() 
    #s.toSRT(keep_tag=True)
    s.toSRT(keep_tag=False)
  
    #for sub in s.Subs:
    #  print(str(sub) + "\n")
      
  if False:
    test_lib()
    
  if False:
    with open(SUBS_DIR + "/dollhouse.ass") as f:
      for line in f:
        print line
        if re.search(r"\{\\fad\(\d{1,4},\d{1,4}\)\}", line.strip("\r\n")):
          print("found")
        #else:
        #  print("not found")
        
        
  if False:
    text = r"{\fade(200,200)}Épisode 101 : {\i1}The Ghost{\i0}\Nv. 1.03"
    if re.search(r"{\\(?:fad|fade)\((\d{1,4}),(\d{1,4})\)}", text):
      print(re.search(r"{\\(?:fad|fade)\((\d{1,4}),(\d{1,4})\)}", text).groups())
      