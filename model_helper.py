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

        if len(current_model["points"]) < 2:
            current_model["points"].append((x, y))
        else:
            min_distance = float('inf')
            insert_index = 0

            for i in range(len(current_model["points"])):
                p = current_model["points"][i]
                d = math_helper.distance((x, y), p)

                if d < min_distance:
                    min_distance = d
                    insert_index = i

            # Handle edge case where insert_index is the last element
            if insert_index == len(current_model["points"]) - 1:
                current_model["points"].append((x, y))
            else:
                ad = math_helper.distance((x, y), current_model["points"][insert_index + 1])
                bc = math_helper.distance((x, y), current_model["points"][insert_index - 1])

                if ad < bc:
                    insert_index += 1

                # Check for line crossings
                # Check for line crossings
                new_point = (x, y)
                for i in range(len(current_model["points"]) - 1):
                    if i != insert_index and i != insert_index - 1:
                        if math_helper.lines_intersect(current_model["points"][i], current_model["points"][i + 1],
                                                       current_model["points"][insert_index], new_point):
                            # Adjust the insert_index to avoid intersection
                            insert_index = i + 1
                            break

                current_model["points"].insert(insert_index, new_point)


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
