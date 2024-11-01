from pydantic import BaseModel

import models
from database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

class ProductBase(BaseModel):
    product_id : int
    name : str
    description : str

class ShelfBase(BaseModel):
    shelf_id : int
    zone : str
    stack : str
    level : int
    position : str
    
class TrackerBase(BaseModel):
    product_id : int
    shelf_id : int
    item_id : str
    timestamp : str
    
class LogBase(BaseModel):
    product_id : int
    shelf_id : int
    item_id : str
    type : str
    action : str
    description : str
    timestamp : str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        