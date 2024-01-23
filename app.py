from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb+srv://santimn08:tarzan12@cluster0.60ipbly.mongodb.net/")  # Aquí debes especificar tu conexión a MongoDB
db = client["videojuegos"]
collection = db["videojuego"]


class VideojuegoCreate(BaseModel):
    nombre: str
    categoria: str
    multijugador: int
    precio: float
    desarrolladora: str
    # Otros campos según tu modelo
    
# Modelo para la actualización de un videojuego
class VideojuegoUpdate(BaseModel):
    nombre: str = None
    categoria: str = None
    multijugador: int = None
    precio: float = None
    desarrolladora: str = None

# Ruta para crear un videojuego en MongoDB
@app.post("/videojuego/")
async def create_videojuego(videojuego: VideojuegoCreate):
    videojuego_data = videojuego.dict()
    inserted_data = collection.insert_one(videojuego_data)
    inserted_id = str(inserted_data.inserted_id)  # Convertimos el ObjectId a string

    # Actualizamos el objeto antes de devolverlo
    videojuego_data['_id'] = inserted_id
    return videojuego_data


# Ruta para obtener un videojuego específico de MongoDB
@app.get("/videojuego/{videojuego_id}")
async def read_videojuego(videojuego_id: str):
    videojuego = collection.find_one({"_id": ObjectId(videojuego_id)})  # Convertimos el videojuego_id a ObjectId
    if videojuego:
        videojuego['_id'] = str(videojuego['_id'])  # Convertimos el _id a string
        return videojuego
    raise HTTPException(status_code=404, detail="Videojuego no encontrado")


# Ruta para obtener todos los videojuegos
@app.get("/videojuegos/")
async def get_all_videojuegos():
    videojuegos = list(collection.find())
    for videojuego in videojuegos:
        videojuego['_id'] = str(videojuego['_id'])  # Convertimos el _id a string
    return videojuegos


@app.put("/videojuegos/{videojuego_id}")
async def update_videojuego(videojuego_id: str, updated_data: VideojuegoUpdate):
    # Convertimos el videojuego_id a ObjectId
    videojuego_id_obj = ObjectId(videojuego_id)

    # Actualizamos el videojuego en la base de datos
    result = collection.update_one(
        {"_id": videojuego_id_obj},
        {"$set": updated_data.dict(exclude_unset=True)}
    )

    if result.modified_count == 1:
        return {"status": f"El videojuego con ID {videojuego_id} ha sido actualizado"}
    
    raise HTTPException(status_code=404, detail="Videojuego no encontrado")

# Ruta para eliminar un videojuego de MongoDB
@app.delete("/videojuego/{videojuego_id}")
async def delete_videojuego(videojuego_id: str):
    deleted_game = collection.delete_one({"_id": ObjectId(videojuego_id)})
    if deleted_game.deleted_count == 1:
        return {"status": f"El videojuego con ID {videojuego_id} ha sido eliminado"}
    raise HTTPException(status_code=404, detail="Videojuego no encontrado")

