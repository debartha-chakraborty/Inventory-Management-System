from pydantic import BaseModel

class Product(BaseModel):
    product_id: int
    name: str
    description: str | None = None
    price: float
    image: str | None = None
    
    class Config:
        orm_mode = True
        
        