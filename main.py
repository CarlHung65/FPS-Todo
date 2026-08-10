from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from schema import EmployeeSchema, EmpolyeeCreate, EmployeeUpdate

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

# --- 新增員工 ---
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

# --- 修改員工資料 ---
@app.put("/employees/{emp_id}", response_model=EmployeeSchema)
def update_employee(emp_id: int, employee_data: EmployeeUpdate, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="找不到該員工資料")
    
    # 只更新有傳入值的欄位 (exclude_unset=True)
    update_data = employee_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(emp, key, value)
        
    db.commit()
    db.refresh(emp)
    return emp

# --- 刪除員工資料 ---
@app.delete("/employees/{emp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="找不到該員工資料")
    
    db.delete(emp)
    db.commit()
    return None

# ------------------- API 路由定義 -------------------

if __name__ == "__main__":
    init_and_load_db()