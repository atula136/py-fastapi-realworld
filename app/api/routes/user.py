from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreateWrapper, UserLoginWrapper, UserUpdateWrapper, UserResponseWrapper
from app.db.models import User
from app.crud.user import get_user_by_email, get_user_by_username, create_user, update_user
from app.core.security.jwt import create_access_token, get_password_hash, verify_password
from ..deps import get_db, get_current_user

router = APIRouter()

# Helper functions
def create_access_token_for_user(user_id: int) -> str:
    return create_access_token(data={"sub": str(user_id)})

def get_user_or_404(db: Session, email: str):
    db_user = get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user

def build_user_response(user) -> dict:
    return {"user": user}

@router.post("/", response_model=UserResponseWrapper)
async def register_user(user: UserCreateWrapper, db: Session = Depends(get_db)):
    user_data = user.user
    if get_user_by_email(db, email=user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data.password = get_password_hash(user_data.password)
    created_user = create_user(db=db, user=user_data)
    created_user.token = create_access_token_for_user(created_user.id)

    return build_user_response(created_user)

@router.post("/login/", response_model=UserResponseWrapper)
async def login_user(user: UserLoginWrapper, db: Session = Depends(get_db)):
    print("NEIT - start login", user)
    user_data = user.user
    db_user = get_user_or_404(db, email=user_data.email)
    if not verify_password(user_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    db_user.token = create_access_token_for_user(db_user.id)

    print("NEIT - success login", db_user)
    return build_user_response(db_user)

@router.put("/", response_model=UserResponseWrapper)
async def update_user_profile(user: UserUpdateWrapper,
                              db: Session = Depends(get_db),
                              current_user: User = Depends(get_current_user)):
    user_data = user.user
    if user_data.username and user_data.username != current_user.username and get_user_by_username(db, username=user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already in use."
        )
    if user_data.email and user_data.email.lower() != current_user.email.lower() and get_user_by_email(db, email=user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use."
        )
    updated_user = update_user(db, db_user=current_user, user_update=user_data)
    updated_user.token = create_access_token_for_user(updated_user.id)

    return build_user_response(updated_user)