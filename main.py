import wx

from image_viewer_window import ImageViewerWindow
from select_image import SelectImage


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="OpenCV and wxPython", size=(800, 600))

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        self.select_image = SelectImage(self.panel, self.sizer, self.add_image)

        self.debug_button(self.select_image.image_path)

        self.sizer.Add(wx.StaticText(self.panel, label="Image Path:"))

    def add_image(self):
        ImageViewerWindow(self.select_image.image_path).Show()



    def debug_button(self, x):
        debug_button = wx.Button(self.panel, label="Debug")
        debug_button.Bind(wx.EVT_BUTTON, self.debug)
        self.sizer.Add(debug_button)

    def debug(self, event):
        print(self.select_image.image_path)




if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()