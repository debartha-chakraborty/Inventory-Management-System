from sqlalchemy import Integer, String, Float, Column, Text, Boolean
from database import Base

class Product(Base):
    __tablename__ = "product"
    
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    is_continued = Column(Boolean)
    price = Column(Float, nullable=False)
    image = Column(Text)
    
    
    def __repr__(self):
        return f"<Product(product_id={self.product_id}, name='{self.name}')>"
            