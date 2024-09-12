import wx


class ImageHelper():
    def __init__(self, image_path, panel):
        self.image_path = image_path
        self.panel = panel
        self.bmp = None

    def load_image(self):
        img = wx.Image(self.image_path, wx.BITMAP_TYPE_ANY)

        scale_factor = 480 / img.GetHeight()
        scale = wx.Size(int(scale_factor * img.GetWidth()), 480)

        img = img.Scale(scale[0], scale[1], wx.IMAGE_QUALITY_HIGH)
        self.original_bitmap = img.ConvertToBitmap()
        self.bmp = wx.StaticBitmap(self.panel, bitmap=self.original_bitmap)

        return self.bmp  # Return the StaticBitmap object

    def draw_polygons(self, models, model_index):
        if self.bmp is None:
            raise ValueError("StaticBitmap is not initialized. Ensure load_image is called successfully.")

        bitmap_copy = wx.Bitmap(self.original_bitmap.GetWidth(), self.original_bitmap.GetHeight())
        dc = wx.MemoryDC(bitmap_copy)
        gc = wx.GraphicsContext.Create(dc)
        gc.DrawBitmap(self.original_bitmap, 0, 0, self.original_bitmap.GetWidth(), self.original_bitmap.GetHeight())

        for i, model in enumerate(models):
            cur_points = model["points"]
            if not cur_points:
                continue  # Skip if cur_points is empty

            cur_color = model["custom_properties"]["color"]

            transparency = 153 if i == model_index else 51  # 60% for current, 20% for others
            transparent_color = wx.Colour(cur_color[0], cur_color[1], cur_color[2], transparency)

            dc.SetPen(wx.Pen(transparent_color, 5))
            dc.SetBrush(wx.Brush(transparent_color))

            dc.DrawPolygon(cur_points)


        del gc
        del dc

        self.bmp.SetBitmap(bitmap_copy)
        self.panel.Layout()
        self.panel.Fit()

        return bitmap_copy