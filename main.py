from fastapi import FastAPI
from presentations.router import router as presentation_router
from users.router import router as user_router

app = FastAPI(
    title="Presentation"
)

app.include_router(presentation_router)
app.include_router(user_router)


@app.get("/")
async def home():
    return {"message": "OK"}
