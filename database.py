import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

db_host = os.getenv("POSTGRES_HOSTNAME")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_port = os.getenv("POSTGRES_PORT")

password = quote_plus(db_password) if db_password else ""

database_url = f"postgresql+psycopg2://{db_user}:{password}@{db_host}:{db_port}/{db_name}"

engine = (create_engine(database_url, echo=True))

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("Successfully to connected database")
    except:
        print("Fail to connect")