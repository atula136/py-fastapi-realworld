from fastapi import Request, HTTPException, status
from fastapi.security.base import SecurityBase
from fastapi.security import HTTPBearer as CustomHTTPBearer, HTTPAuthorizationCredentials as CustomHTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param
from typing import Optional

class CustomHTTPScheme(SecurityBase):
    def __init__(self, auto_error: bool = True):
        self.model = CustomHTTPBearer(bearerFormat="Bearer or Token")
        self.scheme_name = "CustomHTTPScheme"
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[CustomHTTPAuthorizationCredentials]:
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        
        if not authorization or not credentials or scheme.lower() not in ("bearer", "token"):
            if self.auto_error:
                print("NEIT1", scheme, credentials)
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authorization format",
                )
            else:
                print("NEIT2", scheme, credentials)
                return None
        
        return CustomHTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
