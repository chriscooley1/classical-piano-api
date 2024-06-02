from fastapi import FastAPI, HTTPException
from typing import Optional
from models import Composer, Piece
import json

app = FastAPI()

with open("composers.json", "r") as f:
    composers_list: list[dict] = json.load(f)

with open("pieces.json", "r") as f:
    pieces_list: list[dict] = json.load(f)

composers: list[Composer] = []
pieces: list[Piece] = []

for composer_data in composers_list:
    composers.append(Composer(**composer_data))

for piece_data in pieces_list:
    pieces.append(Piece(**piece_data))

@app.get("/composers")
async def get_composers() -> list[Composer]:
    return composers

@app.get("/pieces")
async def get_pieces(composer_id: Optional[int] = None) -> list[Piece]:
    if composer_id is not None:
        return [piece for piece in pieces if piece.composer_id == composer_id]
    return pieces

@app.post("/composers")
async def create_composer(composer: Composer) -> None:
    if any(c.composer_id == composer.composer_id for c in composers):
        raise HTTPException(status_code=400, detail="Duplicate ID passed in")
    composers.append(composer)

@app.post("/pieces")
async def create_piece(piece: Piece) -> None:
    if piece.composer_id is not None and not any(c.composer_id == piece.composer_id for c in composers):
        raise HTTPException(status_code=400, detail="Composer ID doesn't exist")
    pieces.append(piece)

@app.put("/composers/{composer_id}")
async def update_composer(composer_id: int, updated_composer: Composer) -> Composer:
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            if any(c.composer_id == updated_composer.composer_id and c != composer for c in composers):
                raise HTTPException(status_code=400, detail="Duplicate ID passed in")
            composers[i] = updated_composer
            return updated_composer
    raise HTTPException(status_code=404, detail="Composer not found")

@app.put("/pieces/{piece_name}")
async def update_piece(piece_name: str, updated_piece: Piece) -> Piece:
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            if updated_piece.composer_id is not None and not any(c.composer_id == updated_piece.composer_id for c in composers):
                raise HTTPException(status_code=400, detail="Composer ID doesn't exist")
            pieces[i] = updated_piece
            return updated_piece
    raise HTTPException(status_code=404, detail="Piece not found")

@app.delete("/composers/{composer_id}")
async def delete_composer(composer_id: int) -> None:
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            composers.pop(i)
            return
    raise HTTPException(status_code=404, detail="Composer not found")

@app.delete("/pieces/{piece_name}")
async def delete_piece(piece_name: str) -> None:
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces.pop(i)
            return
    raise HTTPException(status_code=404, detail="Piece not found")
