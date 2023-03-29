from fastapi import FastAPI
from app.routers import products, users, basic_auth_users, jwt_auth_users
from fastapi.staticfiles import StaticFiles


app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def read_root():
    return {"Hello": "World"}

