from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime
from geojson_pydantic.features import Feature, FeatureCollection
from geojson_pydantic.geometries import Point, Geometry
from geoalchemy2 import Geometry
# from sqlalchemy import DateTime

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


# class SearchOptions(BaseModel):
#     ne_lat: float = -36.53 
#     ne_lng: float = -72.75
#     sw_lat: float = -36.70
#     sw_lng: float = -73.12
#     start_date: datetime = "2023-02-19T00:00:00"
#     end_date: datetime = "2023-02-21T00:00:00"