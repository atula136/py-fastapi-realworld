from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    # case-sensitive
    # only work for MySQL
    # return db.query(User).filter(func.binary(User.username) == username).first()
    # work for SQLite
    # return db.query(User).filter(User.username.collate("binary") == username).first()
    
    # Determine the dialect being used
    dialect = db.bind.dialect.name
    
    # Different queries for MySQL and SQLite
    if dialect == 'mysql':
        sql = text(
            """
            SELECT * FROM users
            WHERE BINARY username = :username
            LIMIT 1
            """
        )
    elif dialect == 'sqlite':
        sql = text(
            """
            SELECT * FROM users
            WHERE username COLLATE BINARY = :username
            LIMIT 1
            """
        )
    else:
        raise NotImplementedError(f"Database dialect '{dialect}' is not supported.")

    result = db.execute(sql, {'username': username}).fetchone()
    return result

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email.ilike(email)).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def update_user(db:Session, db_user: User, user_update: UserUpdate) -> User:
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def follow_user(db: Session, current_user: User, user_to_follow: User) -> User:
    if user_to_follow not in current_user.following:
        current_user.following.append(user_to_follow)
        db.commit()
    return user_to_follow

def unfollow_user(db: Session, current_user: User, user_to_unfollow: User) -> User:
    if user_to_unfollow in current_user.following:
        current_user.following.remove(user_to_unfollow)
        db.commit()
    return user_to_unfollow

def is_following(db: Session, current_user: User, user_to_check: User) -> bool:
    return user_to_check in current_user.following