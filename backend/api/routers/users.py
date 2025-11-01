from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database import functions, schemas, models
from ...database.connection import get_db
from ..auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registra um novo usuário.
    (Antigo POST /register)
    """
    db_user = functions.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=409, detail="Username already registered")
    return functions.create_user(db=db, user=user)

@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_current_user(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleta a conta do usuário autenticado.
    (Substitui o inseguro DELETE /users/{user_id})
    """
    return functions.remove_user_account(db=db, user_id=current_user.id)


@router.get("/me/urls", response_model=List[schemas.Url])
def get_my_urls(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Lista todas as URLs encurtadas pelo usuário autenticado.
    (Antigo GET /users/me/urls)
    """
    return functions.get_user_urls(db=db, user_id=current_user.id)
