import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_redis_cache import FastApiRedisCache, cache

from app.documentation import tags_metadata
from app.routes import api
from app.util import in_prod, setup_sentry


app = FastAPI(
    title="lichess-stats.org",
    docs_url="/api/docs",
    openapi_url="/api.json",
    openapi_tags=tags_metadata,
    debug=not in_prod(),
)

# Middlewares
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prod middlewares
if in_prod():
    setup_sentry(app)

    @app.on_event("startup")
    def startup():
        redis_cache = FastApiRedisCache()
        redis_cache.init(
            host_url=os.environ["REDIS_URL"],
        )


app.include_router(api.router, prefix="/api")

if __name__ == "__main__":
    # For local development
    uvicorn.run("app.main:app", host="localhost", reload=True, port=8000)
