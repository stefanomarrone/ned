from typing import List, Union

from domain.utils import Place, SafetyMethod


class AreaOfInterest:
    def __init__(self, places: List[Place], safety_methods: Union[List[SafetyMethod], None] = None):
        # basically an area is a list of places, not a polygon because we can have separate points.
        self.places: List[Place] = places
        self.safety_methods: Union[List[SafetyMethod], None] = safety_methods
