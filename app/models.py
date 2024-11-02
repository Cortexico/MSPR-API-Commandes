from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True)
    total_amount = Column(Float)
    status = Column(String, default="pending")
    items = relationship("OrderItem", back_populates="order")

    customer = relationship("Customer", back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(String, ForeignKey("products.id"), index=True)
    quantity = Column(Integer)
    price = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    
class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    address = Column(String)

    orders = relationship("Order", back_populates="customer")