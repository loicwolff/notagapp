#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class SubtitleFile(object):
  _subs = []
  _file = ""
  _sub_name = ""
  _sub_name_pattern = r"(.*)\.srt"
      
  def __init__(self, file=None):
    if file is not None:
      self._setFile(file)
    else:
      file = ""
      
  def toAss(self):
    """"""
    output_file = open("{file}.TAG.ass".format(file=self._sub_name), "w")
    
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
    
    ass_pattern = { "<i>":"{\i1}", "</i>":"{\i0}", "<u>":"{\u1}", "</u>":"{\u0}", "<b>":"{\b1}", "</b>":"{\b0}" }
    
    for sub in self._subs:
      [re.sub(key, value, sub.FirstLine) for key, value in ass_pattern.items()]
      [re.sub(key, value, sub.SecondLine) for key, value in ass_pattern.items()]
    
      output_file.write("Dialogue: 0,{start_time},{end_time},Default,,0000,0000,0000,,{first_line}{second_line}\r\n".format(
                          start_time=sub.StartTime.toAss(),
                          end_time=sub.EndTime.toAss(),
                          first_line=sub.FirstLine,
                          second_line="" if sub.SecondLine == "" else "\N{0}".format(sub.SecondLine)))
                
    output_file.close()
    
  def toTranscript(self):
    """"""
    output_file = open(u"{file}.TRANSCRIPT.txt".format(file=self._sub_name), 'w')
    
    pattern = "({.*?})|(<.*?>)"
    number_pattern = "^\d+\r\n$"
    timing_pattern = "^..:..:..\,... --> ..:..:..\,...\r\n$"
    
    with open(self._file, "r") as sub:
      for line in sub:
        if (not re.match(number_pattern, line)) and (not re.match(timing_pattern, line)) and (line.strip('\r\n') != ""):
          output_file.write(re.sub(pattern, "", line))

    output_file.close()
  
  def toSRT(self):
    """"""
    pass
    
  def removeTag(self):
    """"""
    output_file = open(u"{file}.NOTAG.srt".format(file=self._sub_name), "w")
    sub_pattern = u"({.*?})|(</?font.*?>)|(</?u>)|(</?b>)"

    noTagPattern = { "œ":"oe", "Œ":"Oe", "Æ":"Ae", "æ":"ae" }
    
    with open(self._file, "r") as sub:
      for line in sub:
        temp_line = re.sub(sub_pattern, "", line)
        for key, value in noTagPattern.items():
          re.sub(key, value, temp_line)
        output_file.write(temp_line)
      
    output_file.close()
    
  def _isSubtitle(self, file):
    return file[-4:] == u".srt"
      
  # getters
  def _getFile(self):
    return self._file
      
  def _getSubs(self):
    return self._subs
  
  # setters
  def _setFile(self, file):
    if not self._isSubtitle(file) or not open(file, "r"):
      raise ValueError(u"Unable to open file or not a SRT")
    else:
      self._file = file
      self._sub_name = re.match(re.compile(self._sub_name_pattern), file).group(1)
      
      is_first_line = True
      
      with open(file, "r") as sub:
        sub_entry = None
        for line in sub:
          line = line.strip("\r\n")
          if re.match("^\d+$", line):
            sub_entry = Subtitle()
            sub_entry.Index = int(line)
          elif re.match("\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", line):
            if sub_entry is not None:
              sub_entry.TimingLine = line
          elif line != "":
            if is_first_line:
              if sub_entry is not None:
                sub_entry.FirstLine = line
                is_first_line = False
            else:
              if sub_entry is not None:
                sub_entry.SecondLine = line
                is_first_line = True
                self._subs.append(sub_entry)
                sub_entry = None
          else:
            if sub_entry is not None:
              is_first_line = True
              self._subs.append(sub_entry)
              sub_entry = None

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
  
  def __init__(self):
    self._start_time = Timing()
    self._end_time = Timing()
  
  def __str__(self):
    return "{start} --> {end}\r\n{first_line}{second_line}".format(
        start=self._start_time, 
        end=self._end_time, 
        first_line=self._first_line, 
        second_line="" if self._second_line == "" else "\r\n{0}".format(self._second_line))
  
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
      
  def _getTimingLine(self):
    return "{first} --> {second}".format(
        first=self._start_time, 
        second=self._end_time)
          
  def _getLines(self):
    return "{first}\r\n{second}".format(self._first_line, self._second_line)
          
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
  TimingLine = property(_getTimingLine, _setTimingLine)
    
class Timing(object):
  _millis = 0
  _sec = 0
  _min = 0
  _hour = 0
  
  @staticmethod
  def parse(timing):
    m = re.match("(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})", timing)
    return (Timing(m.group(1), m.group(2), m.group(3), m.group(4)), 
            Timing(m.group(5), m.group(6), m.group(7), m.group(8)))
      
  def __init__(self, hour = 0, min = 0, sec = 0, millis = 0):
    self._millis = millis
    self._sec = sec
    self._min = min
    self._hour = hour
      
  def toAss(self):
    return "{0}:{1}:{2}.{3}".format(
          int(self._hour),
          self._min, 
          self._sec, 
          self._millis[0:2])
      
  def __str__(self):
    return "{0}:{1}:{2},{3}".format(self._hour, self._min, self._sec, self._millis)
      
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

if __name__ == "__main__":
  s = SubtitleFile()
  s.File = "/Users/dex/Desktop/scrubs.srt"
    
  s.toAss()
  s.toTranscript()
  s.removeTag()
  
  #for sub in s.Subs:
    #print("\n" + str(sub))
        