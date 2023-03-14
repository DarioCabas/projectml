from fastapi import FastAPI
from projectml.app.routers import products
from projectml.app.routers import users


app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}



