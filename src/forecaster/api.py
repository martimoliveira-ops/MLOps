from fastapi import FastAPI

from forecaster import __version__

app = FastAPI(title="forecaster", version=__version__)


@app.get("/health")
def health():
    return {"status": "ok"}
