from fastapi import FastAPI
from presentations.router import router as presentation_router

app = FastAPI(
    title="Presentation"
)

app.include_router(presentation_router)


@app.get("/")
async def home():
    return {"message": "OK"}
