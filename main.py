from fastapi import FastAPI, Depends, HTTPException, status # type: ignore
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from schema import EmployeeSchema, EmpolyeeCreate

from database import engine, Base
from model import Employee
from cleaner import cleanerCSV

def init_and_load_db():
    # 建立 table
    Base.metadata.create_all(bind=engine)

    # 資料清洗
    df = cleanerCSV("customers.csv")

    # 匯入 PostgreSQL
    df.to_sql(
        name = 'employees',
        con = engine,
        if_exists = 'append',
        index = False
    )

# ------------------- API -------------------
app = FastAPI(title="EMS API")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------- API 路由定義 -------------------
@app.get("/")
def read_root():
    return {"message" : "Employee Management API is running"}

@app.get("/employees")
def get_all_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return employees

# 新增員工
@app.post("/employees", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmpolyeeCreate, db: Session = Depends(get_db)):
    # 檢查 emp_id 是否已存在 (因為 models.py 設定 unique=True)
    db_employee = db.query(Employee).filter(Employee.emp_id == employee.emp_id).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="emp_id is exist")
    
    # 將 Pydantic 模型轉為 SQLAlchemy 模型物件
    new_employee = Employee(**employee.model_dump())

    # 寫入資料庫
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee

# ------------------- API 路由定義 -------------------

if __name__ == "__main__":
    init_and_load_db()