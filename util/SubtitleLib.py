#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import re

class SubtitleType(object):
  SRT = 1
  ASS = 2
  
  def __init__(self):
    pass

class SubtitleFile(object):
  _subs = []
  _file = ""
  _sub_name = ""
  _sub_name_pattern = r"(.*)\.srt"
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
        if re.match("^\d+$", line):
          sub_entry = Subtitle()
          sub_entry.Index = int(line)
        # match timing line
        elif re.match("\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", line):
          if sub_entry is not None:
            sub_entry.StartTime, sub_entry.EndTime = Timing.parseSRT(line)
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

  def _parseAss(self):
    pass

  def toAss(self, keep_tag):
    """"""
    output_file = open("%s.%s.ass" % (self._sub_name, "TAG" if keep_tag else "NOTAG"), "w")
    
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

    with open("%s.%s.ass" % (self._sub_name, "TAG" if keep_tag else "NOTAG"), "w") as output_file:
      for sub in self._subs:
        output_file.write("Dialogue: 0,%s,%s,Default,,0000,0000,0000,,%s%s\r\n" % (
                            sub.StartTime,
                            sub.EndTime,
                            toAssPattern(sub.FirstLine),
                            "" if sub.SecondLine == "" else "\N%s" % (toAssPattern(sub.SecondLine))))
    
  def toTranscript(self):
    """write the transcript of the subtitle"""
    
    with open("%s.TRANSCRIPT.txt" % (self._sub_name), "w") as output_file:
      for sub in self._subs:
       output_file.write("%s%s\r\n" % (
                          removeTag(sub.FirstLine, False), 
                          "" if sub.SecondLine == "" else "\r\n%s" % (removeTag(sub.SecondLine, False))))
  
  def toSRT(self, keep_tag):
    """"""
    with open("%s.%s.srt" % (self._sub_name, "TAG" if keep_tag else "NOTAG"), "w") as output_file:
      for sub in self._subs:
        output_file.write("%s --> %s\r\n%s%s\r\n" % (
          sub.StartTime,
          sub.EndTime,
          sub.FirstLine if keep_tag else removeTag(sub.FirstLine, True),
          "" if sub.SecondLine == "" else "\r\n%s" % (sub.SecondLine if keep_tag else removeTag(sub.SecondLine, True)))) 

  def _isSubtitle(self, file):
    if file[-4:] == u".srt":
      self._type = SubtitleType.SRT
    elif file[-4:] == u".ass":
      self._type = SubtitleType.ASS
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
      self._sub_name = re.match(re.compile(self._sub_name_pattern), file).group(1)
      self._subs = []
      if self._type == Subtitle.SRT:
        self._parseSRT()
      else:
        pass
    

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
  _type = None
  
  def __init__(self, type = SubtitleType.SRT):
    self._start_time = Timing()
    self._end_time = Timing()
    self._type = type
  
  def __str__(self):
    if self._type == SubtitleType.SRT:
      return "%s --> %s\r\n%s%s" % (
          self._start_time, 
          self._end_time, 
          self._first_line, 
          "" if self._second_line == "" else "\r\n%s" % (self._second_line))
    else: #if self._type == SubtitleType.ASS:
      return "Dialogue: 0,%s:%s:%s.%s,%s:%s:%s.%s,Default,,0000,0000,0000,,%s%s" % (
          self._start_time, 
          self._end_time, 
          self._first_line, 
          "" if self._second_line == "" else "\N%s" % (self._second_line))
  
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
          
  def _getLines(self):
    if self._type == SubtitleType.SRT:
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
      
  # properties
  Index = property(_getIndex, _setIndex)
  StartTime = property(_getStartTime, _setStartTime)
  EndTime = property(_getEndTime, _setEndTime)
  Lines = property(_getLines)
  FirstLine = property(_getFirstLine, _setFirstLine)
  SecondLine = property(_getSecondLine, _setSecondLine)
  #TimingLine = property(_getTimingLine, _setTimingLine)

class Timing(object):
  _millis = 0
  _sec = 0
  _min = 0
  _hour = 0
  _type = SubtitleType.SRT
  
  @staticmethod
  def parseSRT(timing):
    m = re.match("(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})", timing)
    return (Timing(m.group(1), m.group(2), m.group(3), m.group(4)), 
            Timing(m.group(5), m.group(6), m.group(7), m.group(8)))
            
  @staticmethod
  def parseAss(timing):
    m = re.match("^Dialogue: 0,(\d{1,2}):(\d{2}):(\d{2}).(\d{2}),(\d{1,2}):(\d{2}):(\d{2}).(\d{2}),Default,,0000,0000,0000,,\w*$", 
                  timing)
    
    return (Timing(m.group(1), m.group(2), m.group(3), m.group(4)), 
            Timing(m.group(5), m.group(6), m.group(7), m.group(8)))
      
  def __init__(self, hour = 0, min = 0, sec = 0, millis = 0, type = SubtitleType.SRT):
    self._millis = int(millis)
    self._sec = int(sec)
    self._min = int(min)
    self._hour = int(hour)
    self._type = SubtitleType.SRT
      
  def toAss(self):
    return "%s:%s:%s.%s" % (
          str(int(self._hour)),
          self._min, 
          self._sec, 
          self._millis[0:2])
      
  def __str__(self):
    if self._type == SubtitleType.SRT:
      return "%.2d:%.2d:%.2d,%.3d" % (self._hour, self._min, self._sec, self._millis)
    else:# self._type == SubtitleType.ASS:
      return "%d:%.2d:%.2d.%.2d" % (
              self._hour,
              self._min, 
              self._sec, 
              self._millis)    
      
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


def removeExoticChar(entry):
  """remove any exotic character from the text to make it more compatible"""
  noTagPattern = { "œ":"oe", "Œ":"Oe", "Æ":"Ae", "æ":"ae" }
  for key, value in noTagPattern:
    entry = re.sub(key, value, entry)
  return entry
  
def removeTag(entry, keep_italics):
  """remove SRT and ASS tags
  if <code>keep_italics>, italics tags are not removed
  """
  tag_pattern = "{.*?}|</?font.*?>|</?u>|</?b>" if keep_italics else "{.*?}|</?font.*?>|</?u>|</?b>|</?i>"
  return re.sub(tag_pattern, "", entry)
  
def toAssPattern(entry):
  """"""
  ass_pattern = { "<i>":"{\i1}", "</i>":"{\i0}", "<u>":"{\u1}", "</u>":"{\u0}", "<b>":"{\b1}", "</b>":"{\b0}" }
  for key, value in ass_pattern:
    entry = re.sub(key, value, entry) 
  return entry



if __name__ == "__main__":
  s = SubtitleFile()
  s.File = "/Users/dex/Desktop/himym.srt"
 
  #s.toAss()
  #s.toTranscript()
  #s.removeTag()
  s.toSRT(True)
  
  #for sub in s.Subs:
    #print("\n" + str(sub))
        
