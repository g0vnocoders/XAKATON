from sqlalchemy.orm import Session

import models, schemas
import hashlib


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_password(db: Session, password: str):
    return db.query(models.User).filter(models.User.hashed_password == password).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    nothashed_password =user.password #hashlib.sha256
    db_user = models.User(email=user.email, hashed_password=nothashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def delete_item_by_id(db: Session, id:str):
    db.query(models.Item).filter(models.Item.id==int(id)).delete()
    db.commit()

def create_user_item(db: Session, item: schemas.ItemCreate, user_password: str):
    user_id=get_user_by_password(db,user_password)
    db_item = models.Item(**item.dict(), owner_name=user_id.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
