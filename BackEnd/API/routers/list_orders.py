from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import datetime


router= APIRouter(prefix="/list_list_orders", 
                  tags= ["list_orders"],
                  responses = {404: {"message":"No encontrado"}})

class Service(BaseModel):
    id: int
    name: str
    description: str
    type: str
    image: str
    price: float
    place: str
    date: datetime.date # año,mes,dia
    hour: datetime.time # hora,minuto,segundo
    id_provider: int
    availability: bool
    comments: List[str] = []

class list_order(BaseModel):
    id: int
    id_usuario: int
    Services: List[Service]
    
list_orders_group =  [list_order(id= 1, id_usuario= 2, Services= [Service(id= 2, name= "Restaurante WOK", description= "Reserva para restaurante WOK", type= "Restaurante", image= "link imagen", price= 10000, place= "Santa Marta", date= datetime.date(2024, 4, 23), hour= datetime.time(19,30,0), id_provider= 2, availability= True, comments=[""])])]

@router.get("/")
async def list_orders():
    return list_orders_group

@router.get("/{id}") # Path
async def list_order(id: int):
    return search_list_order(id)
    
@router.get("/") # Query
async def list_order(id: int, ):
    return search_list_order(id)
    
@router.post("/", response_model=list_order, status_code=201) # Creación lista orden
async def list_order(list_order: list_order):
    if type(search_list_order(list_order.id)) == list_order:
        raise HTTPException(status_code=204, detail="La orden ya existe")
    else:
        list_orders_group.append(list_order)
        return list_order

@router.put("/", response_model=list_order) # Actualizar lista orden
async def list_order(list_order: list_order):
    found = False
    for index, saved_list_order in enumerate(list_orders_group):
        if saved_list_order.id == list_order.id:
             list_orders_group[index] = list_order
             found = True
    if not found:
        raise HTTPException(status_code=404, detail="Lista de orden no encontrado")
    else:
        return list_order
    
@router.delete("/{id}") # Borrar lista orden por Id
async def list_order(id: int):
    found = False
    for index, saved_list_order in enumerate(list_orders_group):
        if saved_list_order.id == id:
             del list_orders_group[index]
             found = True
    if not found:
        raise HTTPException(status_code=404, detail="Lista de orden no encontrado")
    

def search_list_order(id: int):
    list_orders = filter(lambda list_order: list_order.id == id, list_orders_group )
    try:
        return list(list_orders)[0]
    except:
        return {"error":"Lista de orden no encontrado"}