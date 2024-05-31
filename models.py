from pydantic import BaseModel
from typing import Optional


class Composer(BaseModel):
    name: str
    composer_id: int
    home_country: str

class Piece(BaseModel):
    name: str
    alt_name: Optional[str] = None
    difficulty: int
    composer_id: Optional[int] = None