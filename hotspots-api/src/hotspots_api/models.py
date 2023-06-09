from sqlalchemy import Column, Integer, String, TIMESTAMP
from geoalchemy2 import Geometry, functions

from .database import Base


class Hotspot(Base):
    __tablename__ = "hotspots"

    hotspot_id = Column(Integer, primary_key=True, index=True)
    geometry = Column(Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', spatial_index=True))
    radius = Column(Integer)
    tz = Column(TIMESTAMP(timezone=False))
    satellite = Column(String)

    def to_dict(self):
        coords = functions.ST_AsGeoJSON(self.geometry)
        return coords