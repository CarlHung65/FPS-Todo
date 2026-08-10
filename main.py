from fastapi import FastAPI, Depends # type: ignore
from sqlalchemy.orm import Session, sessionmaker
from typing import List

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

if __name__ == "__main__":
    init_and_load_db()