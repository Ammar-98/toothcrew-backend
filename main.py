from typing import Union
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models, database


# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# ---------------- Pydantic Schemas ----------------
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class PostModal(BaseModel):
    title: str
    content: str
    user_id: int


class UserModal(BaseModel):
    name: str
    role: str


# ---------------- Routes ----------------
@app.get("/")
def read_root():
    return {"Hello": "World"}


# ✅ Create User
@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(payLoad: UserModal, db: Session = Depends(get_db)):
    new_user = models.User(**payLoad.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "user": new_user}


# ✅ Get User by ID
@app.get("/user/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}


# ✅ Create Post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payLoad: PostModal, db: Session = Depends(get_db)):
    new_post = models.Post(**payLoad.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "Post created", "post": new_post}


# ✅ Get Post by ID
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": post}
