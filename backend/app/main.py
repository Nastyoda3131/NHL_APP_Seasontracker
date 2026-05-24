from fastapi import FastAPI

app = FastAPI(title="NHL Topscorer API")

@app.get("/api/health")
def health():
    return {"status": "ok"}
