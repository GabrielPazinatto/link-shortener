from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from ..utils import generate_random_url, hash_password, verify_password 

def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()

def login_user(db: Session, user_login: schemas.UserLogin) -> models.User:
    db_user = get_user_by_username(db, username=user_login.username)
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if not verify_password(user_login.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong Password")
    
    return db_user

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=409, detail="User already exists")

    # encryption method has a limit of 72 bytes input
    hashed_password = hash_password(user.password[:72])
    db_user = models.User(username=user.username, password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def remove_user_account(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}

def get_original_url(db: Session, short_url: str) -> str | None:
    db_url = db.query(models.Url).filter(models.Url.short_url == short_url).first()
    return db_url.url if db_url else None

def get_user_urls(db: Session, user_id: int) -> list[models.Url]:
    return db.query(models.Url).filter(models.Url.owner_id == user_id).all()

def add_new_url(db: Session, url: str, user_id: int) -> models.Url:
    short_url = generate_random_url()
    
    while get_original_url(db, short_url):
        short_url = generate_random_url()
        
    db_url = models.Url(owner_id=user_id, url=url, short_url=short_url)
    
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return db_url

def delete_url(db: Session, short_url: str, user_id: int):
    db_url = db.query(models.Url).filter(
        models.Url.short_url == short_url,
        models.Url.owner_id == user_id
    ).first()

    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found or not owned by user")
    
    db.delete(db_url)
    db.commit()
    return {"detail": "URL deleted successfully"}

def delete_urls(db: Session, short_urls: list[str], user_id: int):
    db_urls = db.query(models.Url).filter(
        models.Url.short_url.in_(short_urls),
        models.Url.owner_id == user_id
    ).all()

    if not db_urls:
        raise HTTPException(status_code=404, detail="No URLs found or not owned by user")
    
    for url in db_urls:
        db.delete(url)
        
    db.commit()
    return {"detail": f"{len(db_urls)} URLs deleted successfully"}