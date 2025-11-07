import os
from fastapi import APIRouter, FastAPI, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from ..database import functions, schemas, models
from ..database.connection import get_db, engine

from .auth import (
    authenticate_user, 
    create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)

from .routers import users, urls

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

##########################
#      Config CORS       #
##########################

origin = os.getenv("API_ORIGIN")

print(origin, flush=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*", "GET", "POST", "PUT", "DELETE", "HEAD"],
    allow_headers=["*"],
)

##########################
#        Routers         #
##########################

app_router = APIRouter()
    
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(urls.router, prefix="/api/urls", tags=["URLs"])

##########################
#   Auth token         #
##########################

@app_router.post("/token", response_model=schemas.Token, tags=["Authentication"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    password_to_check = form_data.password[:72]
    
    user = authenticate_user(
        db, 
        username=form_data.username, 
        password=password_to_check
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app_router.head("/{short_url}", tags=["Redirect"])
def redirect_to_long_url(short_url: str, db: Session = Depends(get_db)):
    long_url = functions.get_original_url(db=db, short_url=short_url)
    if not long_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return RedirectResponse(url=long_url)


@app_router.get("/hello")
def say_hello():
    return {"message": "Hello, I am alive!"}

app.include_router(app_router, prefix="/api")
