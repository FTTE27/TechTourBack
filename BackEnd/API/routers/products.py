from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router= APIRouter(prefix="/products", 
                  tags= ["products"],
                  responses = {404: {"message":"No encontrado"}})

# Entidad product
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
    
products_list = [Product(id= 1, name= "Tabla de surf", description= "Tabla de surf de 1,8 m", image= "link imagen", price= 15000, place= "Cartagena", id_provider= 2, availability= True, comments=["Buen producto", "Recomendado"]),
                 Product(id= 2, name= "Balon de volleyball", description= "Balon de cuero para jugar volleyball", image= "link imagen", price= 10000, place= "Santa Marta", id_provider= 2, availability= True, comments=[""])]
        
# Obtener productos
    
@router.get("/")
async def products():
    return products_list

@router.get("/{id}") # Path
async def product(id: int):
    return search_product(id)
    
@router.get("/") # Query
async def product(id: int, ):
    return search_product(id)
    
@router.post("/", response_model=product, status_code=201) # Creación producto
async def product(product: product):
    if type(search_product(product.id)) == product:
        raise HTTPException(status_code=204, detail="El producto ya existe")
    else:
        products_list.append(product)
        return product

@router.put("/", response_model=product) # Actualizar producto
async def product(product: product):
    found = False
    for index, saved_product in enumerate(products_list):
        if saved_product.id == product.id:
             products_list[index] = product
             found = True
    if not found:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    else:
        return product
    
@router.delete("/{id}") # Borrar producto por Id
async def product(id: int):
    found = False
    for index, saved_product in enumerate(products_list):
        if saved_product.id == id:
             del products_list[index]
             found = True
    if not found:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    

def search_product(id: int):
    products = filter(lambda product: product.id == id, products_list )
    try:
        return list(products)[0]
    except:
        return {"error":"Producto no encontrado"}