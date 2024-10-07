from deprecated import deprecated
from typing import List, Union

from domain.utils import Place, SafetyMethod, Asset

"""
The old AreaOfInterest is deprecated.
now you should use AssetOfInterest
"""

@deprecated(version='1.0', reason="You should use AssetsOfInterest")
class AreaOfInterest:
    def __init__(self, places: List[Place], safety_methods: Union[List[SafetyMethod], None] = None):
        # basically an area is a list of places, not a polygon because we can have separate points.
        self.places: List[Place] = places
        self.safety_methods: Union[List[SafetyMethod], None] = safety_methods


class AssetsOfInterest:
    def __init__(self, assets: List[Asset]):
        # basically an area is a list of places, not a polygon because we can have separate points.
        self.assets: List[Asset] = assets
