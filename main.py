from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas
import json
import re


app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.match(pattern, email):
        return True
    else:
        return False


def modify(db_user):
    return schemas.User(
        id=db_user.id,
        name=db_user.name,
        age=db_user.age,
        gender=db_user.gender,
        email=db_user.email,
        city=db_user.city,
        interests=json.loads(db_user.interests),
    )


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db_user.interests = json.dumps(user.interests)
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already used")
    if not validate_email(db_user.email):
        raise HTTPException(status_code=400, detail="Email validation failed")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return modify(db_user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return [modify(user) for user in users]


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return modify(user)


@app.get("/delete/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return modify(user)


@app.post("/update/", response_model=schemas.User)
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.name is not None:
        db_user.name = user.name
    if user.age is not None:
        db_user.age = user.age
    if user.gender is not None:
        db_user.gender = user.gender
    if user.email is not None:
        existing_user = (
            db.query(models.User).filter(models.User.email == user.email).first()
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already used")
        if not validate_email(user.email):
            raise HTTPException(status_code=400, detail="Email validation failed")
        db_user.email = user.email
    if user.city is not None:
        db_user.city = user.city
    if user.interests is not None:
        db_user.interests = json.dumps(user.interests)
    db.commit()
    return modify(db_user)


@app.get("/match/{user_id}", response_model=list[schemas.User])
def match_user(
    user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    users = (
        db.query(models.User)
        .filter(models.User.id != user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    users = [modify(user) for user in users]
    interests = set(db_user.interests)

    def score(user):
        sum = 0
        if user.gender != db_user.gender:
            print("matched")
            sum += 1 * 100
        if user.city == db_user.city:
            sum += 1 * 10
        sum += len(set(user.interests) & interests)
        return -sum

    users.sort(key=score)
    return users
