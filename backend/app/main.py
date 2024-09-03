from fastapi import FastAPI

app = FastAPI()


@app.post("/api/search")
def search_stats():
    pass