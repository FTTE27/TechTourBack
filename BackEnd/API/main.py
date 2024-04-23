from fastapi import FastAPI
from routers import products
from routers import users
from routers import services
from routers import orders
from routers import list_orders

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(services.router)
app.include_router(orders.router)
app.include_router(list_orders.router)

@app.get("/")
async def root():
    return ""

@app.get("/url")
async def root():
    return {"url": "https://www.youtube.com"}