from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class UrlBase(BaseModel):
    url: str

class UrlCreate(UrlBase):
    pass

class Url(UrlBase):
    id: int
    owner_id: int
    short_url: str
    
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    urls: List[Url] = []

    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str