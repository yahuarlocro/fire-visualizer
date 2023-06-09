from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import func, select
from geoalchemy2 import Geometry, functions, Geography

from .database import Base


class Hotspot(Base):
    __tablename__ = "hotspots"

    hotspot_id = Column(Integer, primary_key=True, index=True)
    # geometry = Column(Geometry(geometry_type='POINT', srid=4326))
    geometry = Column(Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', spatial_index=True))
    # geometry = Column(Geography(geometry_type='POINT', srid=4326, from_text='ST_GeogFromText'))
    radius = Column(Integer)
    tz = Column(TIMESTAMP(timezone=False))
    satellite = Column(String)

    def to_dict(self):
        coords = functions.ST_AsGeoJSON(self.geometry)
        # data = {
    #         "hotspot_id": self.hotspot_id,
    #         "radius": self.radius,
    #         "tz": self.tz,
    #         "satellite": self.satellite,
            # "geometry": functions.ST_AsGeoJSON(self.geometry, 4326)
            # "geometry": Hotspot.query

        # }

        return coords