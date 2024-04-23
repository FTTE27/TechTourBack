from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix= "/users", 
                   tags= ["users"],
                   responses = {404: {"message":"No encontrado"}})

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone: int
    password: str
    

users_list = [User(id= 1,name= "Juan Andres",surname= "Vasquez Velasco", email= "ja.vasquez@javeriana.edu.co", phone= 30283508, password= "ABC123"),
         User(id= 2,name= "Pedro",surname= "Perez",email= "pedrop@javeriana.edu.co", phone= 302833321, password= "DEF456", ),
         User(id= 3,name= "Felipe",surname= "Suarez Rodriguez",email= "felipes@javeriana.edu.co", phone= 242535354, password= "XYZ111")]

# Obtener usuarios
    
@router.get("/")
async def users():
    return users_list

@router.get("/{id}") # Path id
async def user(id: int):
    return search_user(id)

@router.get("/{email}") # Path email
async def user(email: str):
    return search_user_email(email)
    
@router.get("/") # Query id
async def user(id: int, ):
    return search_user(id)

@router.get("/") # Query email
async def user(email: str, ):
    return search_user_email(email)
    
@router.post("/", response_model=User, status_code=201) # Creación usuario
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user

@router.put("/", response_model=User) # Actualizar usuario
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
             users_list[index] = user
             found = True
    if not found:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        return user
    
@router.delete("/{id}") # Borrar usuario por Id
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
             del users_list[index]
             found = True
    if not found:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
@router.delete("/{email}") # Borrar usuario por email
async def user(email: str):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.email == email:
             del users_list[index]
             found = True
    if not found:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list )
    try:
        return list(users)[0]
    except:
        return {"error":"Usuario no encontrado"}
    
def search_user_email(email: str):
    users = filter(lambda user: user.email == email, users_list )
    try:
        return list(users)[0]
    except:
        return {"error":"Usuario no encontrado"}