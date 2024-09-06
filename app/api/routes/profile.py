# app/api/routes/profile.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.crud.user import get_user_by_username, follow_user, unfollow_user, is_following
from app.schemas.user import Profile, ProfileResponseWrapper
from app.db.models import User

router = APIRouter()

def build_profile_response(profile) -> dict:
    return {"profile": profile}

@router.post("/profiles/{username}/follow/", response_model=ProfileResponseWrapper)
async def follow_user_endpoint(
    username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_to_follow = get_user_by_username(db, username)
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="User not found")
    
    followed_user = follow_user(db, current_user, user_to_follow)
    profile = Profile(
        username=followed_user.username,
        bio=followed_user.bio,
        image=followed_user.image,
        following=True
    )
    return build_profile_response(profile)

@router.delete("/profiles/{username}/follow/", response_model=ProfileResponseWrapper)
async def unfollow_user_endpoint(
    username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_to_unfollow = get_user_by_username(db, username)
    if not user_to_unfollow:
        raise HTTPException(status_code=404, detail="User not found")
    
    unfollowed_user = unfollow_user(db, current_user, user_to_unfollow)
    profile = Profile(
        username=unfollowed_user.username,
        bio=unfollowed_user.bio,
        image=unfollowed_user.image,
        following=False
    )
    return build_profile_response(profile)
