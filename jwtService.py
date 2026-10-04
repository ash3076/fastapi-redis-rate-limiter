from datetime import timedelta , datetime , timezone 
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
import os 

load_dotenv()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def generate_token(data):
    to_encode=data.copy()
    expiry_date = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp" : expiry_date
    }) 

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def current_user(token:str=Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code =401 , detail={"Invalid Token"})
        return username
    except JWTError:
        raise HTTPException(status_code=402 , detail="user notfound")
    