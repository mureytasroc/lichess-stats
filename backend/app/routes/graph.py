from typing import Optional

from fastapi import APIRouter, Path, Query

from app.database.util import GameType
from app.models.games import *


router = APIRouter()

# TODO: routes for win graph (requires Neo4J)
