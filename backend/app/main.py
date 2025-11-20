from fastapi import FastAPI

from .api.routes import router

app = FastAPI(title="PhotoBrain API")
app.include_router(router)


@app.get("/", response_model=dict)
def root() -> dict:
    return {"message": "PhotoBrain backend is running"}
