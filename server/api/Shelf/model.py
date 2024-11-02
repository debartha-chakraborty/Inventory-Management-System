from database import Base
from sqlalchemy import Column, Integer, Text


class Shelf(Base):
    __tablename__ = 'shelf'
    
    id = Column(Integer, primary_key=True, index=True)
    levels = Column(Integer, nullable=False)
    position = Column(Text)
    
    def __repr__(self):
        return f"<Shelf(id={self.id}, levels={self.levels}, position='{self.position}')>"
