from fastapi import FastAPI # type: ignore

app = FastAPI()

@app.get("/")
def hello():
    return {"message" : "Hello world!"}