import wx.adv
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
                cur_feature = Feature(geometry=LineString(fractional_points), properties=model["custom_properties"])
                features.append(cur_feature)

        if polygons:
            cur_feature = Feature(geometry=Polygon(polygons), properties=group[0]["custom_properties"])
            features.append(cur_feature)

    feature_collection = FeatureCollection(features)
    with open(path + ".json", "w") as f:
        f.write(str(feature_collection))
        wx.adv.NotificationMessage("Export Successful", f"Exported to {path}.json").Show()