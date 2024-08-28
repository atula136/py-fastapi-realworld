from sqlalchemy.orm import Session
from app.db.models import TodoItem
from app.schemas.todo import TodoCreate

def create_todo_item(db: Session, todo: TodoCreate):
    db_todo = TodoItem(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TodoItem).offset(skip).limit(limit).all()