PROXIMITY_THRESHOLD = 10
import math_helper
import random

def random_color():
    levels = range(8, 256, 8)
    return [random.choice(levels) for _ in range(3)]


class ModelHelper:
    def __init__(self, draw_polygon):
        self.model_index = 0
        self.models = []
        self.draw_polygon = draw_polygon

    def add_point(self, event):
        x, y = event.GetX(), event.GetY()
        current_model = self.models[self.model_index]

        if current_model["custom_properties"].get("type") == "line" and len(current_model["points"]) == 2:
            return

        current_model["points"].append((x, y))

        if len(current_model["points"]) > 1:
            self.draw_polygon()

    def clear_point(self, event):
        x, y = event.GetX(), event.GetY()
        current_model = self.models[self.model_index]

        for point in current_model["points"]:
            if abs(x - point[0]) < PROXIMITY_THRESHOLD and abs(y - point[1]) < PROXIMITY_THRESHOLD:
                current_model["points"].remove(point)
                break

        self.draw_polygon()

    def add_model(self, name=None):
        new_model_index = len(self.models)
        self.models.append({
            "name": name + str(new_model_index) if name else f"Polygon {new_model_index}",
            "points": [],
            "custom_properties" : {
                "type": "polygon",
                "color": random_color()
            }
        })

        self.model_index = new_model_index

    def add_line(self):
        self.add_model("Line ")
        self.models[self.model_index]["custom_properties"]["type"] = "line"
