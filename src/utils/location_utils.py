from typing import Any
import random

import pointpats
from shapely import Point, Polygon, buffer

def get_location_category(feature_count: dict[str, Any], location: str) -> str:
    for category, items in feature_count.items():
        if location in items.keys():
            return category
    raise ValueError(f"Unknown location {location}")

def weighted_random_selection(data: dict[str, Any]) -> tuple[str,str]:
    weighted_choices = []

    for category, items in data.items():
        for key, weight in items.items():
            weighted_choices.append((category, key, weight))

    categories, keys, weights = zip(*weighted_choices)
    selected_index = random.choices(range(len(categories)), weights=weights, k=1)[0]
    return categories[selected_index], keys[selected_index]

def random_point_in_polygon(geometry: Polygon):
    # A buffer is added because the method hangs if the polygon is too small
    return Point(
        pointpats.random.poisson(
            buffer(geometry=geometry, distance=0.000001), size=1
        )
    )