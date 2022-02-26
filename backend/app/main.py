from fastapi import FastAPI
import uvicorn


app = FastAPI(title="ChessWins.net", docs_url="/api/docs", openapi_url="/api")


@app.get("/api/")
async def root():
    return {"message": "Hello World"}


# TODO: setup routers

if __name__ == "__main__":
    # For local development
    uvicorn.run("main:app", host="localhost", reload=True, port=8000)
