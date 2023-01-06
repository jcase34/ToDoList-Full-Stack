from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the username and password in order to get a token.
# In this way, we required that the path operation include 'login' 
# Sets oath2_scheme as "callable"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# 
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# Functions below detail validating the token & checking token expiry. Without these the token is created, but never validated on API end
def verify_access_token(token: str, credentials_exception):

    # Possible error out
    try:
        # Extract decoded jwt data & store within stdlib dictionary
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception

        # Check against TokenData schema
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


# Pass as dependency for any path related operations.
# 
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials.", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials.", headers={"WWW-Authenticate": "Bearer"})

#     return verify_access_token(token, credentials_exception)