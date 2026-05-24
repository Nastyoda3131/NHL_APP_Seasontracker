from fastapi import FastAPI

from app.routers import dev, team, users


app = FastAPI(title="NHL Topscorer API")


@app.get("/api/health")
def health():
    return {"status": "ok"}


app.include_router(dev.router)
app.include_router(team.router)
app.include_router(users.router)