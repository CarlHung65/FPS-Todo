from pydantic import BaseModel
from datetime import date
from typing import Optional

# 定義單一員工回傳格式
class EmployeeSchema(BaseModel):
    id: int
    emp_id: str
    name: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    hire_date: Optional[date] = None

    class Config:
        # 讓 Pydantic 能夠自動轉譯 SQLAlchemy 的 ORM 物件
        from_attributes = True