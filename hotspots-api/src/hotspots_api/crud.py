from datetime import datetime
from sqlalchemy.orm import Session
from shapely.geometry import Polygon, Point
from geoalchemy2.comparator import CONTAINS

from . import models, schemas


def get_hotspot(db: Session, hotspot_id: int):
    return db.query(models.Hotspot).filter(models.Hotspot.hotspot_id == hotspot_id).first()


def get_hotspots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hotspot).offset(skip).limit(limit).all()

def get_all_hotspots(db: Session):
    return db.query(models.Hotspot).all()

# def get_hotspots_datetime_bbox(db: Session, search_options):
def get_hotspots_datetime_bbox(db: Session, start_date, end_date, bbox):
    search_options_lst = bbox.split(',')
    search_options = [float(i) for i in search_options_lst]
    
    p1 = Point(search_options[3], search_options[2])
    p2 = Point(search_options[1], search_options[2])
    p3 = Point(search_options[1], search_options[0])
    p4 = Point(search_options[3], search_options[0])
    points = [p1,p2,p3,p4,p1]
    bbox = Polygon([[p.x,p.y] for p in points])
    bbox = bbox.wkt
    # start_date = search_options.start_date
    # end_date = search_options.end_date
    # start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    # end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S")
    # bbox = 'POLYGON((-73.24214851996301 -36.50752705827534,-72.86037361761926 -36.50752705827534,-72.86037361761926 -36.782990226719456,-73.24214851996301 -36.782990226719456,-73.24214851996301 -36.50752705827534))'
# def get_hotspots_datetime_bbox(db: Session, start_date, end_date, bbox):

    # return db.query(models.Hotspot).filter(models.Hotspot.tz >= req_datetime).order_by(models.Hotspot.geometry.contains(bbox)).all()
    return db.query(models.Hotspot).filter(models.Hotspot.tz >= start_date, models.Hotspot.tz < end_date, models.Hotspot.geometry.intersects(bbox)).all()
    # return db.query(models.Hotspot).filter(models.Hotspot.tz >= req_datetime, models.Hotspot.geometry.contains(bbox)).all()
    # return db.query(models.Hotspot).filter(models.Hotspot.tz >= req_datetime).all()``
# def create_user(db: Session, hotspot: schemas.HotspotCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db_hotspot = models.Hotspot(geom)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

