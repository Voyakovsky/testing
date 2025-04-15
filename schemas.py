from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    password: str

class User(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
