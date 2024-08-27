import wx

class SelectImage(wx.Frame):
    def __init__(self, panel, sizer, event, *args, **kw):
        super().__init__(*args, **kw)

        self.image_path = None
        self.panel = panel
        self.sizer = sizer
        self.event = event

        self.select_image_button()

    def select_image_button(self):
        select_image_button = wx.Button(self.panel, label="Select Image")
        select_image_button.Bind(wx.EVT_BUTTON, self.select_image)
        self.sizer.Add(select_image_button)

    def select_image(self, event):
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file", wildcard=wildcard, style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.image_path = dialog.GetPath()
            self.sizer.Add(wx.StaticText(self.panel, label=self.image_path))
            self.panel.Layout()
            self.event()
        dialog.Destroy()

