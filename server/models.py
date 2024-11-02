from sqlalchemy import Integer, String, Float, Column, Text, Boolean, ForeignKey, TIMESTAMP
from database import Base

class Product(Base):
    __tablename__ = "product"
    
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, default='{}')
    is_continued = Column(Boolean, default=True)
    price = Column(Float, nullable=False)
    image = Column(Text)
    
    
    def __repr__(self):
        return f"<Product(product_id={self.product_id}, name='{self.name}')>"
            

class Shelf(Base):
    __tablename__ = 'shelf'
    
    shelf_id = Column(Integer, primary_key=True, index=True)
    zone = Column(String(28), nullable=False)
    stack = Column(String(16), nullable=False)
    level = Column(Integer, nullable=False)
    position = Column(Text, default='{}')
    
    def __repr__(self):
        return f"<Shelf(id={self.shelf_id}, zone={self.zone}, stack={self.stack}, level={self.level})>"


class Tracker(Base):
    __tablename__ = 'tracker'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.product_id'))
    shelf_id = Column(Integer, ForeignKey('shelf.shelf_id'))
    item_id = Column(String(32))
    timestamp = Column(TIMESTAMP, server_default='now()')


class Log(Base):
    __tablename__ = 'log'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.product_id'))
    shelf_id = Column(Integer, ForeignKey('shelf.shelf_id'))
    item_id = Column(String(32))
    type = Column(String(16), nullable=False)
    action = Column(String(16), nullable=False)
    description = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, server_default='now()')
    
    def __repr__(self):
        return f"<Log(id={self.id}, product_id={self.product_id}, shelf_id={self.shelf_id}, type={self.type}, action={self.action})>"
