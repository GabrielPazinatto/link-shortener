from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...database import functions, schemas, models
from ...database.connection import get_db
from ..auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Url, status_code=status.HTTP_201_CREATED)
def create_url(
    url: schemas.UrlCreate, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return functions.add_new_url(db=db, url=url.url, user_id=current_user.id)

@router.delete("/", status_code=status.HTTP_200_OK)
def delete_url(
    short_urls: list[str],
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted_urls = functions.delete_urls(db=db, short_urls=short_urls, user_id=current_user.id)
    if not deleted_urls:
        raise HTTPException(status_code=404, detail="URL not found or not owned by user")
    return {"detail": f"{deleted_urls} URLs deleted"}
