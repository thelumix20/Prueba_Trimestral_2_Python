from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, auth, database, schemas # Asegúrate de crear schemas.py
from typing import List

app = FastAPI(title="API de Incidentes - Prueba Trimestral")

# Crear tablas en XAMPP si no existen
models.Base.metadata.create_all(bind=database.engine)

# Dependencia para la BD
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Endpoint de Login corregido para Swagger
@app.post("/login")
# Cambia (form_data: dict) por esto:
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Ahora accedemos con .username y .password (como atributos, no como llaves de dict)
    if form_data.username == "admin" and form_data.password == "1234":
        token = auth.create_access_token(data={"sub": form_data.username})
        return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Usuario o password incorrectos")

# 2. Endpoint público: Listar incidencias
@app.get("/incidencias", response_model=List[schemas.Incidencia])
def listar_incidencias(db: Session = Depends(get_db)):
    return db.query(models.Incidencia).all()

# 3. Endpoint protegido: Crear incidencia
@app.post("/incidencias", response_model=schemas.Incidencia)
def crear_incidencia(
    incidencia: schemas.IncidenciaCreate, 
    db: Session = Depends(get_db), 
    user: str = Depends(auth.get_current_user) # Esto activa el candado
):
    nueva_incidencia = models.Incidencia(**incidencia.model_dump())
    db.add(nueva_incidencia)
    db.commit()
    db.refresh(nueva_incidencia)
    return nueva_incidencia

# 4. Endpoint protegido extra: Ver perfil (Punto 5 de la práctica)
@app.get("/perfil")
def obtener_perfil(user: str = Depends(auth.get_current_user)):
    return {"usuario_autenticado": user, "rol": "Administrador"}