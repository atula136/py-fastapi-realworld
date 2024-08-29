from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    image: Optional[HttpUrl] = None
    bio: Optional[str] = None

class UserResponse(UserBase):
    id: int
    token: str

    class Config(ConfigDict):
        from_attributes = True

class UserCreateWrapper(BaseModel):
    user: UserCreate

class UserUpdateWrapper(BaseModel):
    user: UserUpdate

class UserResponseWrapper(BaseModel):
    user: UserResponse

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserLoginWrapper(BaseModel):
    user: UserLogin