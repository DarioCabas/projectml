from typing import Union

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    id: int
    name: str
    lastname: str
    age: int
    country: str

users_list = [Item(id=1,name="Dario", lastname="Cabascango", age=29, country="Ecuador"),
              Item(id=2,name="Juan", lastname="Hernandez", age=21, country="Cuenca"),
              Item(id=3,name="Kitty", lastname="Juliana", age=29, country="Ecuador")
              ]

@router.get("/usersjson")
async def usersjson():
    return [{"name": "Dario", "lastname":"Cabascango", "age": 24, "country": "Ecuador"},
            {"name": "Dario", "lastname":"Cabascango", "age": 24, "country": "Ecuador"},
            {"name": "Dario", "lastname":"Cabascango", "age": 24, "country": "Ecuador"}]

@router.get("/users")
async def users():
    return users_list


#Path es como obligatorio

@router.get("/users/{id}")
async def user(id: int):
    return search_user(id)


#Query es como que no podria ser que sea necesario

@router.get("/usersquery/")
async def user(id: int):
    return search_user(id)


@router.post("/user/", response_model=Item, status_code=201)
async def user(user: Item):
    if type(search_user(user.id)) == Item:
       raise HTTPException(status_code=404, detail="El usuario ya existe")
    users_list.routerend(user)
    return user 



@router.put("/user/")
async def user(user:Item):

    found = False

    for index, saved_user in enumerate(users_list): 
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha encontrado el usuario"}
    return user

@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list): 
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "No se ha eliminado el usuario"}
    return {"Usuario borrado exitosamente"}

    
def search_user(id: int): 
    users = filter(lambda x: x.id == id, users_list)
    try: 
        return list(users)[0]
    except: 
        return {"error": "Usuario no encontrado" }
    
