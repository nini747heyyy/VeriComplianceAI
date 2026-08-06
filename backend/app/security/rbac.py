import time
import jwt
from fastapi import Request, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from typing import List, Optional

SECRET_KEY = "PRODUCTION_SUPER_SECRET_CHANGE_IN_ENV"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
security_bearer = HTTPBearer()

ROLE_HIERARCHY = {
    "Super Admin": ["*"],
    "Organization Admin": ["org:write", "org:read", "docs:write", "docs:read", "rules:write", "audit:run"],
    "Compliance Officer": ["docs:write", "docs:read", "rules:write", "audit:run"],
    "Manager": ["docs:write", "docs:read", "audit:run"],
    "Employee": ["docs:read"],
    "Viewer": ["docs:read_public"]
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: int = 3600) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": time.time() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_claims(credentials: HTTPAuthorizationCredentials = Security(security_bearer)) -> dict:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token.")

class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, claims: dict = Depends(get_current_user_claims)):
        user_role = claims.get("role")
        permissions = ROLE_HIERARCHY.get(user_role, [])
        if "*" not in permissions and self.required_permission not in permissions:
            raise HTTPException(
                status_code=403, 
                detail=f"Role '{user_role}' lacks required permission: {self.required_permission}"
            )
        return claims