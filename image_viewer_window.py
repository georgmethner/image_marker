import wx


class ImageViewerWindow(wx.Frame):
    def __init__(self, image_path):
        wx.Frame.__init__(self, None, title=image_path, style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)
        self.image_path = image_path
        self.cur_color = wx.Colour(87, 227, 137, 128)

        self.load_image()
        self.add_editing_options()

        self.bmp.Bind(wx.EVT_LEFT_DOWN, self.add_point)
        self.bmp.Bind(wx.EVT_RIGHT_DOWN, self.clear_point)

        self.cur_points = []

        self.panel.Layout()  # Recalculate the layout
        self.panel.Fit()  # Adjust the panel size to fit the sizer's contents
        self.Fit()  # Adjust the frame size to fit the panel's contents

    def add_point(self, event):
        self.cur_points.append((event.GetX(), event.GetY()))
        if len(self.cur_points) > 1:
            self.draw_polygon(event)

    def clear_point(self, event):
        # test if mouse pos is near a point
        for point in self.cur_points:
            if abs(event.GetX() - point[0]) < 10 and abs(event.GetY() - point[1]) < 10:
                self.cur_points.remove(point)
                break
        self.draw_polygon(event)


    def load_image(self):
        self.img = wx.Image(self.image_path, wx.BITMAP_TYPE_ANY)

        scale_factor = 480 / self.img.GetHeight()
        scale = wx.Size(int(scale_factor * self.img.GetWidth()), 480)

        print(scale)

        self.img = self.img.Scale(scale[0], scale[1], wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.bmp = wx.StaticBitmap(self.panel, bitmap=self.img)

        self.sizer.Add(self.bmp)

    def draw_polygon(self, event):
        self.load_image()

        dc = wx.MemoryDC(self.img)
        dc.SetPen(wx.Pen(self.cur_color, 0))
        dc.SetBrush(wx.Brush(self.cur_color))
        dc.DrawPolygon(self.cur_points)
        del dc
        self.bmp.SetBitmap(self.img)

    def add_editing_options(self):
        horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)

        color_picker = wx.ColourPickerCtrl(self.panel, wx.ID_ANY, wx.Colour(87, 227, 137))
        color_picker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.color_picker_changed)
        horizontal_sizer.Add(color_picker)

        self.sizer.Add(horizontal_sizer)

    def color_picker_changed(self, event):
        self.cur_color = event.GetColour()
        self.cur_color = wx.Colour(self.cur_color[0], self.cur_color[1], self.cur_color[2], 128)
        print(self.cur_color)
