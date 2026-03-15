from jwt import encode, decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
from modules.auth.dto.authDTO import userTokenDTO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(data: userTokenDTO, expires_delta: timedelta | None = None) -> str:
    to_encode = data.model_dump()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=720)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = encode(
        to_encode,
        os.environ["JWT_SECRET"],
        algorithm=os.environ["JWT_ALGORITHM"]
    )
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> userTokenDTO:
    try:
        payload = decode(token, os.environ["JWT_SECRET"], algorithms=[os.environ["JWT_ALGORITHM"]])
        username: str | None = payload.get("username")
        email: str | None = payload.get("email")

        if username is None or email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        return userTokenDTO(username=username, email=email )

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")