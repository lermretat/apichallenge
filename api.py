from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root_route():
    return {"message": "háblate carita de pie"}
