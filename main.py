from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from presentations.router import router as presentation_router
from users.router import router as user_router
from pages.router import router as pages_router
from fastapi.staticfiles import StaticFiles
from init_superuser import init_superuser


app = FastAPI(
    title="Presentation"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(presentation_router)
app.include_router(user_router)
app.include_router(pages_router)


@app.on_event("startup")
async def startup_event():
    await init_superuser()


@app.get("/")
async def home():
    return RedirectResponse("/pages/search", status_code=status.HTTP_301_MOVED_PERMANENTLY)
