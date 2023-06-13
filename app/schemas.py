from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class UserData(UserBase):
    pass

class UserAuth(BaseModel):
    api_key: str