from sqlalchemy import Column, Integer, String, Date, Float
from database import Base
from sqlalchemy.orm import declarative_base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String(10), unique=True, nullable=False)
    name = Column(String(20))
    gender = Column(String(20))
    email = Column(String(50))
    phone = Column(String(20))
    department = Column(String(20))
    salary = Column(Float)
    hire_date = Column(Date)