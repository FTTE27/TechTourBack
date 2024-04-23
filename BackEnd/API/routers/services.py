from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import datetime

router= APIRouter(prefix="/services", 
                  tags= ["services"],
                  responses = {404: {"message":"No encontrado"}})

# Entidad service
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
    
services_list = [Service(id= 1, name= "Habitacion Hotel Paris Hillton", description= "Habitación con dos camas por 5 dias", type= "Hospedaje", image= "link imagen", price= 15000, place= "Cartagena", date= datetime.date(2024, 4, 23), hour= datetime.time(12,0,0), id_provider= 2, availability= True, comments=["Buen serviceo", "Recomendado"]),
                 Service(id= 2, name= "Restaurante WOK", description= "Reserva para restaurante WOK", type= "Restaurante", image= "link imagen", price= 10000, place= "Santa Marta", date= datetime.date(2024, 4, 23), hour= datetime.time(19,30,0), id_provider= 2, availability= True, comments=[""])]
        
# Obtener servicios
    
@router.get("/")
async def services():
    return services_list

@router.get("/{id}") # Path
async def service(id: int):
    return search_service(id)
    
@router.get("/") # Query
async def service(id: int, ):
    return search_service(id)
    
@router.post("/", response_model=service, status_code=201) # Creación servicio
async def service(service: service):
    if type(search_service(service.id)) == service:
        raise HTTPException(status_code=204, detail="El servicio ya existe")
    else:
        services_list.append(service)
        return service

@router.put("/", response_model=service) # Actualizar servicio
async def service(service: service):
    found = False
    for index, saved_service in enumerate(services_list):
        if saved_service.id == service.id:
             services_list[index] = service
             found = True
    if not found:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    else:
        return service
    
@router.delete("/{id}") # Borrar servicio por Id
async def service(id: int):
    found = False
    for index, saved_service in enumerate(services_list):
        if saved_service.id == id:
             del services_list[index]
             found = True
    if not found:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    

def search_service(id: int):
    services = filter(lambda service: service.id == id, services_list )
    try:
        return list(services)[0]
    except:
        return {"error":"Servicio no encontrado"}