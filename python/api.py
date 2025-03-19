from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from db import DataBase

##########################
#      Initialization    #
##########################

app: FastAPI = FastAPI()
db: DataBase = DataBase()

##########################
#      CORS Config       #
##########################

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Permite requisições de qualquer origem (pode ser restringido)
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
    ],  # Permite todos os métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

##########################
#      Pydantic Classes  #
##########################


class User(BaseModel):
    username: str
    password: str


class new_URL(BaseModel):
    text: str


##########################
#      GET Endpoints     #
##########################


@app.get("/{short_url}")
async def redirect(short_url: str):
    url = db.get_long_url(short_url)

    return RedirectResponse(url=url)


##########################
#     POST Endpoints     #
##########################


@app.post("/user/{user_id}/add_url/")
async def add_url(user_id: int, new_url: new_URL):
    shortened_url: str = db.add_url(user_id=user_id, url=new_url.text)
    return JSONResponse(
        content={"status": "URL added", "short_url": shortened_url}, status_code=200
    )


@app.get("/user/{user_id}/get_data/")
async def get_urls(user_id: str):
    urls = db.get_urls_from_user(int(user_id))
    return JSONResponse(content=urls, status_code=200)


@app.post("/login/")
async def login(user: User):
    user_data = db.login(user.username, user.password)

    if user_data is None:
        return JSONResponse(content={"status": "error"}, status_code=404)
    else:
        return JSONResponse(content=user_data, status_code=200)


################
# ADD INTO DB
################


@app.post("/register")
async def add_user(user: User):
    db.add_user(user.username, user.password)
    return JSONResponse(content={"status": "User created"}, status_code=200)


################
# DELETE FROM DB
################
