from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List


router= APIRouter(prefix="/orders", 
                  tags= ["orders"],
                  responses = {404: {"message":"No encontrado"}})

class Product(BaseModel):
    id: int
    name: str
    description: str
    image: str
    price: float
    place: str
    id_provider: int
    availability: bool
    comments: List[str] = []

class Order(BaseModel):
    id: int
    id_usuario: int
    products: List[Product]
    
    
orders_group =  [Order(id= 1, id_usuario= 2, products= [Product(id= 1, name= "Tabla de surf", description= "Tabla de surf de 1,8 m", image= "link imagen", price= 15000, place= "Cartagena", id_provider= 2, availability= True, comments=["Buen producto", "Recomendado"])])]

@router.get("/")
async def orders():
    return orders_group

@router.get("/{id}") # Path
async def order(id: int):
    return search_order(id)
    
@router.get("/") # Query
async def order(id: int, ):
    return search_order(id)
    
@router.post("/", response_model=order, status_code=201) # Creación servicio
async def order(order: order):
    if type(search_order(order.id)) == order:
        raise HTTPException(status_code=204, detail="La orden ya existe")
    else:
        orders_group.append(order)
        return order

@router.put("/", response_model=order) # Actualizar orden
async def order(order: order):
    found = False
    for index, saved_order in enumerate(orders_group):
        if saved_order.id == order.id:
             orders_group[index] = order
             found = True
    if not found:
        raise HTTPException(status_code=404, detail="Orden no encontrado")
    else:
        return order
    
@router.delete("/{id}") # Borrar orden por Id
async def order(id: int):
    found = False
    for index, saved_order in enumerate(orders_group):
        if saved_order.id == id:
             del orders_group[index]
             found = True
    if not found:
        raise HTTPException(status_code=404, detail="Orden no encontrado")
    

def search_order(id: int):
    orders = filter(lambda order: order.id == id, orders_group )
    try:
        return list(orders)[0]
    except:
        return {"error":"Orden no encontrado"}