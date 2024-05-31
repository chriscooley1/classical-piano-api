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
def get_composers() -> list[Composer]:
    return composers

@app.get("/pieces")
def get_pieces(composer_id: Optional[int] = None) -> list[Piece]:
    if composer_id is not None:
        return [piece for piece in pieces if piece.composer_id == composer_id]
    return pieces

@app.post("/composers")
def create_composer(composer: Composer):
    pass

@app.post("/pieces")
def create_piece(piece: Piece):
    pass

@app.put("/composers/{composer_id}")
def update_composer(composer_id: int, composer: Composer):
    pass

@app.put("/pieces/{piece_name}")
def update_piece(piece_name: str, piece: Piece):
    pass

@app.delete("/composers/{composer_id}")
def delete_composer(composer_id: int):
    pass

@app.delete("/pieces/{piece_name}")
def delete_piece(piece_name: str):
    pass