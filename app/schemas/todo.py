from pydantic import BaseModel, ConfigDict

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

    class Config(ConfigDict):
        from_attributes = True