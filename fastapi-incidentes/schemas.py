from pydantic import BaseModel

# Lo que se necesita para crear una incidencia
class IncidenciaCreate(BaseModel):
    titulo: str
    descripcion: str
    prioridad: str
    estado: str

# Lo que la API devuelve (incluye el ID)
class Incidencia(IncidenciaCreate):
    id: int

    class Config:
        from_attributes = True