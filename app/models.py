from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    total_amount = Column(Float)
    status = Column(String, default="pending")
    # Vous pouvez ajouter d'autres champs selon vos besoins
