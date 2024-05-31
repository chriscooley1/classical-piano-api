import json
from fastapi import FastAPI, HTTPException
from typing import Optional
from models import Composer, Piece

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
    composers.append(composer)

@app.post("/pieces")
async def create_piece(piece: Piece) -> None:
    pieces.append(piece)

@app.put("/composers/{composer_id}")
async def update_composer(composer_id: int, updated_composer: Composer) -> None:
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            composers[i] = updated_composer
            return updated_composer
    composers.append(updated_composer)
    return

@app.put("/pieces/{piece_name}")
async def update_piece(piece_name: str, updated_piece: Piece) -> None:
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces[i] = updated_piece
            return updated_piece
    pieces.append(updated_piece)
    return

@app.delete("/composers/{composer_id}")
async def delete_composer(composer_id: int) -> None:
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            composers.pop(i)
            return

@app.delete("/pieces/{piece_name}")
async def delete_piece(piece_name: str) -> None:
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces.pop(i)
            return