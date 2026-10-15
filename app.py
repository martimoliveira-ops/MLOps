from fastapi import FastAPI, Query

from chain_of_functions import format_text

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/format")
def format_endpoint(text: str = Query(min_length=1, max_length=200)):
    return {"result": format_text(text)}
