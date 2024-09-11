from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
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

    # SQLAlchemy provides a convenient way to use raw SQL but still return ORM-mapped objects via the .from_statement() method.
    result = db.query(User).from_statement(sql).params(username=username).first()
    return result

    # dialect = db.bind.dialect.name
    # if dialect == 'mysql':
    #     return db.query(User).filter(func.binary(User.username) == username).first()
    # elif dialect == 'sqlite':
    #     return db.query(User).filter(User.username.collate("binary") == username).first()
    # else:
    #     raise NotImplementedError(f"Database dialect '{dialect}' is not supported.")

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
    """
    Follow a user, ensuring that the current user isn't already following the target user.
    """
    # Load the current user with the 'following' relationship
    current_user = db.query(User).options(joinedload(User.following)).filter_by(id=current_user.id).first()

    if not current_user:
        raise ValueError("Current user not found")

    # Ensure user_to_follow is a valid User instance and exists
    if not db.query(User).filter_by(id=user_to_follow.id).first():
        raise ValueError("User to follow does not exist")

    # Check if the user_to_follow is already in the current_user's following list
    if user_to_follow in current_user.following:
        return user_to_follow

    # Add the existing user_to_follow to the current_user's following list
    current_user.following.append(user_to_follow)

    # Commit transaction
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Log the error if needed
        raise ValueError("An error occurred while trying to follow the user. This may be due to a primary key violation or other database constraints.") from e

    return user_to_follow

def unfollow_user(db: Session, current_user: User, user_to_unfollow: User) -> User:
    if user_to_unfollow in current_user.following:
        current_user.following.remove(user_to_unfollow)
        db.commit()
    return user_to_unfollow

def is_following(db: Session, current_user: User, user_to_check: User) -> bool:
    return user_to_check in current_user.following