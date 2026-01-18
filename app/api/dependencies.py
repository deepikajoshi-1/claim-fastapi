from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(token_url="/auth/login")
def get_current_user(token : str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode( token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return {
            "user_id": payload.get("sub"),
            "role": payload.get("role")
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
            
        )
    
def require_role(allowed_roles: list):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker
