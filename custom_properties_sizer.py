import wx

class CustomPropertiesSizer(wx.BoxSizer):
    def __init__(self, parent):
        super().__init__(wx.VERTICAL)

        self.parent = parent
        self.properties = {}

        # Expand button
        self.add_property_button = wx.Button(self.parent, label="Add Property")
        self.add_property_button.Bind(wx.EVT_BUTTON, self.add_property)
        self.Add(self.add_property_button, 0, wx.EXPAND, 0)

        self.remove_property_button = wx.Button(self.parent, label="Remove Property")
        self.remove_property_button.Bind(wx.EVT_BUTTON, self.remove_property)
        self.Add(self.remove_property_button, 0, wx.EXPAND, 0)

        self.property_list = wx.ListCtrl(self.parent, style=wx.LC_REPORT)
        self.property_list.InsertColumn(0, "Name")
        self.property_list.InsertColumn(1, "Value")
        self.Add(self.property_list, 1, wx.EXPAND, 1)

    def add_property(self, event):
        name = wx.GetTextFromUser("Enter property name", "Add Property", parent=self.parent)
        if not name:
            return
        value = wx.GetTextFromUser("Enter property value", "Add Property", parent=self.parent)

        index = self.property_list.InsertItem(self.property_list.GetItemCount(), name)
        self.property_list.SetItem(index, 1, value)

        self.properties[name] = value

    def reload_properties(self, properties):
        self.properties = properties
        self.property_list.DeleteAllItems()

        for name, value in properties.items():
            index = self.property_list.InsertItem(self.property_list.GetItemCount(), name)
            self.property_list.SetItem(index, 1, str(value))

    def clear_properties(self, event):
        self.properties = {}
        self.property_list.DeleteAllItems()

    def remove_property(self, event):
        focused_item = self.property_list.GetFocusedItem()
        if focused_item == -1:
            return

        name = self.property_list.GetItemText(focused_item)
        self.properties.pop(name)
        self.property_list.DeleteItem(focused_item)
