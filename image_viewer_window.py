import wx
import wx.adv

from custom_properties_sizer import CustomPropertiesSizer
from export_helper import export_helper
from image_helper import ImageHelper
from model_helper import ModelHelper

class ImageViewerWindow(wx.Frame):
    def __init__(self, image_path):
        super().__init__(None, title=image_path, style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
        self.panel = wx.Panel(self)
        self.sizer = wx.FlexGridSizer(2, 2, 0, 0)
        self.panel.SetSizer(self.sizer)
        self.image_path = image_path

        self.image_helper = ImageHelper(image_path, self.panel)
        self.image_helper.load_image()

        self.model_helper = ModelHelper(self.draw_polygon)

        self.image_helper.bmp.Bind(wx.EVT_LEFT_DOWN, self.model_helper.add_point)
        self.image_helper.bmp.Bind(wx.EVT_RIGHT_DOWN, self.model_helper.clear_point)

        self.sizer.Add(self.image_helper.bmp)
        self.sizer.Add(self.add_model_list(), 0, wx.EXPAND, 0)
        self.sizer.Add(self.editing_options(), 0, wx.EXPAND, 0)
        self.sizer.Add(self.ctrl_buttons(), 0, wx.EXPAND, 0)

        self.panel.Layout()
        self.panel.Fit()
        self.Fit()

    def draw_polygon(self):
        self.image_helper.draw_polygons(self.model_helper.models, self.model_helper.model_index)

    def add_model_list(self):
        self.model_list = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.model_list.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.set_model_index)
        self.model_list.InsertColumn(0, "Name")
        return self.model_list

    def ctrl_buttons(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        add_model_button = wx.Button(self.panel, label="Add Polygon")
        add_model_button.Bind(wx.EVT_BUTTON, self.add_model)
        sizer.Add(add_model_button, 1, wx.EXPAND, 0)

        add_line_button = wx.Button(self.panel, label="Add Line")
        add_line_button.Bind(wx.EVT_BUTTON, self.add_line)
        sizer.Add(add_line_button, 1, wx.EXPAND, 0)

        export_button = wx.Button(self.panel, label="Export")
        export_button.Bind(wx.EVT_BUTTON, self.export)
        sizer.Add(export_button, 1, wx.EXPAND, 0)

        sizer.SetSizeHints(self.panel)
        return sizer

    def editing_options(self):
        horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        settings_sizer = wx.BoxSizer(wx.VERTICAL)

        self.rename_input = wx.TextCtrl(self.panel, wx.ID_ANY, "")
        settings_sizer.Add(self.rename_input, 1, wx.EXPAND, 0)

        self.color_picker = wx.ColourPickerCtrl(self.panel, wx.ID_ANY, wx.Colour(87, 227, 137))
        settings_sizer.Add(self.color_picker, 0, wx.EXPAND, 0)

        self.custom_properties_sizer = CustomPropertiesSizer(self.panel)

        remove_button = wx.Button(self.panel, label="Remove")
        remove_button.Bind(wx.EVT_BUTTON, self.remove_model)
        button_sizer.Add(remove_button, 1, wx.EXPAND, 0)

        save_button = wx.Button(self.panel, label="Save")
        save_button.Bind(wx.EVT_BUTTON, self.save_model_options)
        button_sizer.Add(save_button, 1, wx.EXPAND, 0)

        horizontal_sizer.Add(settings_sizer, 1, wx.EXPAND, 0)
        horizontal_sizer.Add(self.custom_properties_sizer, 2, wx.EXPAND, 0)
        horizontal_sizer.Add(button_sizer, 1, wx.EXPAND, 0)

        horizontal_sizer.SetSizeHints(self.panel)
        return horizontal_sizer

    def save_model_options(self, event):
        new_name = self.rename_input.GetValue()
        self.model_helper.models[self.model_helper.model_index]["name"] = new_name

        duplicate_count = 0
        duplicate_indexes = []
        for model in self.model_helper.models:
            if model["name"] == new_name:
                duplicate_count += 1
                duplicate_indexes.append(self.model_helper.models.index(model))

        if duplicate_count > 1:
            self.group_duplicate_names(duplicate_indexes)

        color = [self.color_picker.GetColour().Red(), self.color_picker.GetColour().Green(), self.color_picker.GetColour().Blue()]
        self.model_helper.models[self.model_helper.model_index]["custom_properties"]["color"] = color

        self.model_list.SetItem(self.model_helper.model_index, 0, new_name)
        self.custom_properties_sizer.reload_properties(self.model_helper.models[self.model_helper.model_index]["custom_properties"])

        self.draw_polygon()

    def add_model(self, event):
        self.model_helper.add_model()
        self.model_list.Append([str(self.model_helper.models[self.model_helper.model_index]["name"])])
        self.model_list.Focus(self.model_helper.model_index)

    def add_line(self, event):
        self.model_helper.add_line()
        self.model_list.Append([str(self.model_helper.models[self.model_helper.model_index]["name"])])
        self.model_list.Focus(self.model_helper.model_index)

    def remove_model(self, event):
        self.model_helper.models.pop(self.model_helper.model_index)
        self.model_list.DeleteItem(self.model_helper.model_index)
        self.model_helper.model_index = 0
        self.draw_polygon()

    def set_model_index(self, event):
        self.model_helper.model_index = event.GetIndex()
        self.color_picker.SetColour(self.model_helper.models[self.model_helper.model_index]["custom_properties"]["color"])
        self.rename_input.SetValue(self.model_helper.models[self.model_helper.model_index]["name"])
        self.custom_properties_sizer.reload_properties(self.model_helper.models[self.model_helper.model_index]["custom_properties"])
        self.draw_polygon()

    def export(self, event):
        export_helper(self.image_path, self.model_helper.models, self.image_helper.original_bitmap.GetSize())

    def group_duplicate_names(self, duplicate_indexes):
        for index in duplicate_indexes:
            self.model_helper.models[index]["custom_properties"] = self.model_helper.models[duplicate_indexes[0]]["custom_properties"]
            self.custom_properties_sizer.reload_properties(self.model_helper.models[index]["custom_properties"])
        # get all duplicate names and show a notification
        names = [self.model_helper.models[index]["name"] for index in duplicate_indexes]
        wx.adv.NotificationMessage("Grouped", f"Duplicate names grouped: {names}").Show()