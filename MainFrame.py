#/usr/bin/env python
# encoding: utf-8

# python lib
import os

# external lib
import wx

#from DropBox import DropBox
from AppMode import TinyMode, MaxiMode

class MainFrame(wx.Frame):
    """This is the main frame of the application.
    It should be designed to be as simple as possible.
    """
  
    def __init__(self):
        super(MainFrame, self).__init__(None, -1, u"NoTag", wx.DefaultPosition, wx.Size(510, 140), 
                            wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.CAPTION | wx.STAY_ON_TOP | wx.SYSTEM_MENU)
                
        wx.InitAllImageHandlers()
        self._initControls()

        self.SetMinSize(wx.Size(510, 140))
        #self.SetMaxSize(wx.Size(-1, 140))

        self.Center()
        self.Show(True)

    def _initControls(self):
        """create and initialize UI elements"""
    
        # Controls Initialization and showing of the form
        notebook = wx.Notebook(self)
        #TODO:
        notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNoteBookChangeTab)
        #notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnNoteBookChangeTab)
    
        tiny_mode = TinyMode(notebook)
        maxi_mode = MaxiMode(notebook)
    
        notebook.AddPage(tiny_mode, u'Tiny')
        notebook.AddPage(maxi_mode, u'Maxi')
    
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(notebook, 1, wx.EXPAND, 10)

        self.SetSizer(main_sizer)

    def OnNoteBookChangeTab(self, event):
        if event.GetSelection() == 0:
            self.SetSize(wx.Size(510, 140))
        elif event.GetSelection() == 1:
            self.SetSize(wx.Size(510, 400))
    
        #TODO: manage screen size
        #self.Center()
        if False:
            i = self.GetSize().GetHeight()
            if event.GetSelection() == 0:
                while i > 140:
                    i -= 10
                    self.SetSize(wx.Size(510, i))
                self._mainpanel.Show()
            elif event.GetSelection() == 1:
                self._mainpanel.Hide()
                while i < 400:
                    i += 10
                    self.SetSize(wx.Size(510, i))
        
        event.Skip()
    

def main():
    class App(wx.App):
        def OnInit(self):
            frame = MainFrame()
            return True
  
    app = App(False)
    app.MainLoop()
  
if __name__ == '__main__':
    main()
  