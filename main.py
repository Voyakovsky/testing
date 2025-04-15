from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import schemas
from typing import List

from services import hash_password, verify_password

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add_user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hash = hash_password(user.password)
    new_user = User(name=user.name, hashed_password=hash)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при добавлении пользователя")
    return new_user


@app.get("/get_user", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {'id': user.id, 'name': user.name}


@app.post("/delete_user", response_model=schemas.User)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user:
        db.delete(user)
        db.commit()
        return user
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/get_all_users", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.put("/update_user", response_model=schemas.User)
def update_user(id: int, name: str, db: Session = Depends(get_db)):
    updated = db.query(User).filter(User.id == id).update({"name": name})
    db.commit()
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")

    user = db.query(User).filter(User.id == id).first()
    return user

@app.get("/login", response_model=schemas.User)
def login(name: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if verify_password(password, user.hashed_password):
        return user
    raise HTTPException(status_code=401, detail="Not authorized")

# добавить столбец хэш пассворд, изменить ручки
# добавить .env файл с данными бд и ключом хэша