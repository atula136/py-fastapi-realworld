from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoUpdate(BaseModel):
    title: str
    description: str
    completed: bool

class TodoResponse(TodoCreate):
    id: int
    completed: bool

    class Config:
        from_attributes = True