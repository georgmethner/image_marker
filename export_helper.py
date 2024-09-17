import wx
import os
import json
from geojson import LineString, Feature, FeatureCollection, Polygon

def export_helper(path, models, window_size):
    features = []
    width, height = window_size

    # Group models by name
    grouped_models = {}
    for model in models:
        name = model["name"]
        if name not in grouped_models:
            grouped_models[name] = []
        grouped_models[name].append(model)

    for name, group in grouped_models.items():
        polygons = []
        for model in group:
            all_points = model["points"]
            # Calculate fractional coordinates
            fractional_points = [(x / width, y / height) for x, y in all_points]
            if len(fractional_points) >= 3:
                fractional_points.append(fractional_points[0])  # Close the polygon
                polygons.append(fractional_points)
            else:
                # Remove 'type' property if it exists
                if "type" in model["custom_properties"]:
                    del model["custom_properties"]["type"]
                model["custom_properties"]["name"] = name
                cur_feature = Feature(geometry=LineString(fractional_points), properties=model["custom_properties"])
                features.append(cur_feature)

        if polygons:
            # Remove 'type' property if it exists
            if "type" in group[0]["custom_properties"]:
                del group[0]["custom_properties"]["type"]
            group[0]["custom_properties"]["name"] = name
            cur_feature = Feature(geometry=Polygon(polygons), properties=group[0]["custom_properties"])
            features.append(cur_feature)

    feature_collection = FeatureCollection(features)
    file_path = path + ".json"

    # Initialize wx App
    app = wx.App(False)

    # Check if file exists
    if os.path.exists(file_path):
        dialog = wx.MessageDialog(None, f"The file {file_path} already exists. Are you sure you want to replace it?", "Confirm Replace", wx.YES_NO | wx.ICON_WARNING)
        result = dialog.ShowModal()
        dialog.Destroy()
        if result != wx.ID_YES:
            app.MainLoop()
            return

    # Write to file
    with open(file_path, "w") as f:
        f.write(json.dumps(feature_collection, indent=4))

    # Show success message dialog
    dialog = wx.MessageDialog(None, f"Exported to {file_path}", "Export Successful", wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    app.MainLoop()