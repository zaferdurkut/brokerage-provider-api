import uvicorn

from src.application import create_app
from prometheus_fastapi_instrumentator import Instrumentator

app = create_app()


@app.on_event("startup")
def startup_event():
    Instrumentator().instrument(app).expose(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
