from fastapi import FastAPI
from app.routers import products
from app.routers import users
from fastapi.staticfiles import StaticFiles


app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def read_root():
    return {"Hello": "World"}

