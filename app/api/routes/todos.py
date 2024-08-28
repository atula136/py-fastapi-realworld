from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.todo import create_todo_item, get_todo_items
from app.schemas.todo import TodoCreate,TodoResponse
from app.api.deps import get_db

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_todo_item(db=db, todo=todo)

@router.get("/", response_model=List[TodoResponse])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_todo_items(db=db, skip=skip, limit=limit)
