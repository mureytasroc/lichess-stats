from fastapi import APIRouter

from app.routes import games, graph, profile, rating


router = APIRouter()

router.include_router(rating.router, tags=["rating"], prefix="/rating")
router.include_router(games.router, tags=["games"], prefix="/games")
router.include_router(graph.router, tags=["graph"], prefix="/graph")
router.include_router(profile.router, tags=["profile"], prefix="/profile")
