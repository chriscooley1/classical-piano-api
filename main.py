import json


from fastapi import FastAPI

from models import Piece, Composer

app = FastAPI()


with open("composers.json", "r") as f:
    composers_list: list[dict] = json.load(f)

with open("pieces.json", "r") as f:
    piece_list: list[dict] = json.load(f)

pieces: list[Piece] = []
composers: list[Composer] = []

for piece in piece_list:
    pieces.append(Piece(**piece))

for composer in composers_list:
    composers.append(Composer(**composer))


@app.get("/composers")
async def get_composers() -> list[Composer]:
    return composers

@app.post("/composers")
async def create_composers(composer: Composer) -> None:
    composers.append(composer)

@app.put("/composers{composer_id}")
async def update_composers(composer_id: int, updated_composer: Composer) -> None:
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            composers[i] = updated_composer
            return

@app.delete("/composers{composer_id}")
async def delete_composers(composer_id: int) -> None:
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            composers.pop(i)
            return

@app.get("/pieces")
async def get_piece(composer_id: int = None) -> list[Piece]:
    if composer_id is not None:
        filtered_pieces = [piece for piece in pieces if piece.composer_id == composer_id]
        return filtered_pieces
    else:
        return pieces

@app.post("/pieces")
async def create_piece(piece: Piece) -> None:
    pieces.append(piece)

@app.put("/pieces{piece_name}")
async def update_pieces(piece_name: str, updated_piece: Piece) -> None:
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces[i] = updated_piece
            return

@app.delete("/pieces{piece_name}")
async def delete_pieces(piece_name: str) -> None:
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces.pop(i)
            return