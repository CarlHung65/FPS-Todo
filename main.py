from fastapi import FastAPI # type: ignore
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

app = FastAPI()

@app.get("/")
def hello():
    return {"message" : "Hello world!"}


if __name__ == "__main__":
    init_and_load_db()