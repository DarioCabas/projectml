from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,  OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "0f24af244196927b3ed412477ddb9269c07f21d98a6859a7a802bd600ed1ee42" 

router = APIRouter();

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel): 
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str



users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "$2a$12$hGsIHLjwigpEjUn5Ko/xKuIjWKx73SYzmVBzsQTlFiFKU9GS8D5Mm"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "$2a$12$Pc07gAeBKpn3SkCrEl6vKuiSv2tuadPs.iKOzdFmJPkCliocXERDO"
    }
    
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    execption = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Credendiales de authenticacion invalidas", headers={"WWW-Authenticate": "Bearer"})

    try: 
        username = jwt.decode(token, SECRET, ALGORITHM).get("sub")
        if username is None: 
            raise execption

    except JWTError:
        raise execption
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):   
    if user.disabled:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db =  users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)


    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contrasenia no es correcta")
    
    expire = datetime.utcnow() +  timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = { "sub": user.username, "exp": expire,  }
    
    return {"access_token": jwt.encode(access_token, SECRET,algorithm=ALGORITHM) , "token_type": "bearer"}

@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user
