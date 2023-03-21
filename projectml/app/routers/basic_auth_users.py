from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI();

class User(BaseModel): 
    username: str
    full_name: str
    email: str
    disabled: bool

users_db = {
    "mouredev": {
        "mouredev": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "123456"
    },
    "mouredev2": {
        "mouredev": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "123456"
    }
    
}