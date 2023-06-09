from typing import List
from pydantic import BaseModel
from datetime import datetime
from geojson_pydantic.features import Feature, FeatureCollection
from geojson_pydantic.geometries import Point

# class HotspotBase(BaseModel):
#     hotspot_id: int

# class HotspotCreate(HotspotBase):
#     gemetry: Point
#     radius: int
#     tz: datetime
#     satellite: str

# class Hotspot(HotspotBase):
#     hotspot_id: int
#     geometry: Point
#     radius: int
#     tz: datetime
#     satellite: str

#     class Config:
#         orm_mode = True

class HotspotProperties(BaseModel):
    hotspot_id: int
    radius: int
    tz: datetime
    satellite: str

class HotspotFeature(Feature):
    geometry: Point
    properties: HotspotProperties


class HotspotCollection(FeatureCollection):
    features: List[HotspotFeature]
    # features: HotspotFeature
    
class HotspotJsonFeatureCollection(BaseModel):
    hotspots: dict
