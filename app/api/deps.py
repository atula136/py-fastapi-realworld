from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from app.core.security.jwt import decode_access_token
from app.core.security.models import CustomHTTPScheme, CustomHTTPAuthorizationCredentials
from app.crud.user import get_user_by_id
from app.db.models import User

security = CustomHTTPScheme()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: CustomHTTPAuthorizationCredentials = Depends(security)) -> User:
    # Define the credentials exception upfront
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": token.scheme.capitalize()},
    )

    # Extract the token from the credentials
    token_str = token.credentials
    
    # Decode the JWT token
    payload = decode_access_token(token_str)
    
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    
    # Retrieve the user by user_id
    user = get_user_by_id(db, user_id=int(user_id))
    
    if user is None:
        raise credentials_exception
    
    return user

# import logging
# from fastapi.security import OAuth2PasswordBearer
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     logging.info(f"Token: {token}")
#     payload = decode_access_token(token)
#     if payload is None:
#         raise credentials_exception
#     user_id: str = payload.get("sub")
#     user = get_user_by_id(db, user_id=int(user_id))
#     if user is None:
#         logging.error("User not found")
#         raise credentials_exception

#     return user