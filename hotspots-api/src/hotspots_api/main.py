from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import DateTime
from datetime import datetime
import redis
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import os
from typing import Annotated, Literal
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
import csv, json
from geojson_pydantic import Feature, FeatureCollection, Point
import pandas as pd
import geopandas as gpd

models.Base.metadata.create_all(bind=engine)

rd = redis.Redis(host="localhost", port=6379, db=0)

app = FastAPI()

origins = [
    "http://localhost:5001",
    # "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/hotspots/", response_model=list[schemas.Hotspot])
# def read_hotspots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     hotspots = crud.get_hotspots(db, skip=skip, limit=limit)
#     return hotspots

# Different function for translate db response to Pydantic response according to your different schema
def make_response_hotspot_properties(hotspot):
    return schemas.HotspotProperties(hotspot_id=hotspot.hotspot_id, radius=hotspot.radius, tz=hotspot.tz, satellite=hotspot.satellite) 

def make_response_hotspot_feature(hotspot, db):
    feature = json.loads(db.scalar(hotspot.geometry.ST_AsGeoJSON()))
    props = make_response_hotspot_properties(hotspot)
    return schemas.HotspotFeature(type="Feature", geometry=feature, properties=props) 

def make_response_hotspot_collection(hotspots, db):
    response = []
    for i in hotspots:
        response.append(make_response_hotspot_feature(i, db))
    feature_collection = FeatureCollection(type='FeatureCollection', features=response)
    return feature_collection

# @app.get("/hotspots/redis", response_model=schemas.HotspotCollection)
@app.get("/hotspots/redis") 
# def read_hotspots_redis():
async def read_hotspots_redis():
        # rd.geosearch(name='hotspots', member='Features', longitude=-72.75, latitude=-36.65, unit='km', height=400, width=400,) 
    return JSONResponse(json.loads(rd.get('hotspots')))
    # cache =  rd.get('hotspots')
    # if cache:
    #     print('cache hit')
    #     json_cache = json.loads(cache)
    #     # json_cache = [json.loads(cache)]
    #     # feat_col = FeatureCollection(type='FeatureCollection', features=json_cache[0]['features'])
    #     # return FeatureCollection(type='FeatureCollection', features=json_cache)

    #     return json_cache
    #     # return feat_col
    # else:
    #     print('cache miss')
    #     return "lero"

# bounding = {
#     "northeast": {
#         "lat": -36.52,
#         "lng": -72.75
#     },
#     "southwest": {
#         "lat": -36.70,
#         "lng": -73.12
#     }
# }
    
@app.get("/hotspots/", response_model=schemas.HotspotCollection)
# async def read_hotspots_bbox_time(bounding_box, time, db: Session = Depends(get_db)):
# async def read_hotspots_bbox_time(start_date: datetime= '2023-02-19T00:00:00', end_date: datetime = '2023-02-23T00:00:00', bounding_box: str = 'POLYGON((-73.24214851996301 -36.50752705827534,-72.86037361761926 -36.50752705827534,-72.86037361761926 -36.782990226719456,-73.24214851996301 -36.782990226719456,-73.24214851996301 -36.50752705827534))', db: Session = Depends(get_db)):
# async def read_hotspots_bbox_time(start_date: datetime, end_date: datetime, bounding_box: str, db: Session = Depends(get_db)):
async def read_hotspots_bbox_time(start_date: str, end_date: str, bounding_box: str, db: Session = Depends(get_db)):
# async def read_hotspots_bbox_time(start_date: str = '2023-02-19T00:00:00', end_date: str = '2023-02-23T00:00:00', bounding_box: str = '-36.52,-72.75,-36.70,-73.12', db: Session = Depends(get_db)):
# async def read_hotspots_bbox_time(start_date: datetime= '2023-02-19T00:00:00', end_date: datetime = '2023-02-23T00:00:00', bounding_box: dict = bounding, db: Session = Depends(get_db)):
# async def read_hotspots_bbox_time(search_options: schemas.SearchOptions, db: Session = Depends(get_db)):
    # db_hotspots = crud.get_hotspots_datetime_bbox(db, search_options) 
    db_hotspots = crud.get_hotspots_datetime_bbox(db, start_date=start_date, end_date=end_date, bbox=bounding_box)
    hotspots_feature_collection = make_response_hotspot_collection(db_hotspots, db)
    return hotspots_feature_collection


@app.get("/hotspots/postgis", response_model=schemas.HotspotCollection)
async def read_hotspots_postgis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_hotspots = crud.get_hotspots(db, skip=skip, limit=limit)
    hotspots_feature_collection = make_response_hotspot_collection(db_hotspots, db)
    return hotspots_feature_collection

# @app.get("/hotspots/{hotspot_id}", response_model=schemas.Hotspot)
# def read_hotspot(hotspot_id: int, db: Session = Depends(get_db)):
#     db_hotspot = crud.get_hotspot(db, hotspot_id=hotspot_id)
#     if db_hotspot is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_hotspot


@app.post("/hotspots/batch-upload/")
# def create_batch_hotspots(file: Annotated[bytes, File()] ):
async def create_batch_hotspots(file: UploadFile = File(...), db: Session = Depends(get_db)):
    features = []
    tmp_file = os.path.join("./", file.filename)

    with open(tmp_file, mode="wb+") as f:
        f.write(file.file.read())

    df = pd.read_csv(tmp_file)

    df['tz'] = pd.to_datetime(df['tz'])

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")

    del gdf['lon']
    del gdf['lat']

    gdf.to_postgis('hotspots', engine, if_exists='append')
    
    db_hotspots = crud.get_all_hotspots(db) 
    hotspots_feature_collection = make_response_hotspot_collection(db_hotspots, db)
    rd.delete('hotspots')
    rd.set('hotspots', hotspots_feature_collection.json())
    
    os.remove(tmp_file)

    return {"success": "data from csv was uploaded succesfully"}
    # return {"hotspots": hotspots_geojson}