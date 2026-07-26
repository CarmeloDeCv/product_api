from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

class Product(BaseModel):
    name:str
    price:float
    in_stock:bool=True

class User(BaseModel):
    name:str
    surname:str
    phone_number:str

products={}
users={}
user_next_id=1
next_id=1

@app.get("/")
def home():
    return {"message": "It works"}

@app.get("/products")
def list_products():
    return products

@app.get("/users")
def list_users():
    return users

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="suck pipi")
    return products[product_id]

@app.post("/products")
def create_product(product:Product):
    global next_id
    products[next_id] = product
    created_id = next_id
    next_id += 1
    return {"id":created_id, "product":product}

@app.put("/products/{product_id}")
def update_product(product_id:int, product:Product):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="suck caca")
    products[product_id] = product
    return {"updated":product_id, "product":product}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]
    return {"deleted": product_id}

@app.get("/users/{user_id}")
def get_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail = "you pooped the wrong number")
    return users[user_id]

@app.post("/users")
def create_user(user: User):
    global user_next_id
    users[user_next_id]=user
    created_user_id=user_next_id
    user_next_id+=1
    return {"id":created_user_id, "user":user}

@app.put("/users/{user_id}")
def change_user(user_id:int, user:User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="you pooper in the wrong place")
    users[user_id]=user
    return {"updated":user_id, "user": user}

@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="poooped deletedn nit")
    del users[user_id]
    return {"deleted":user_id}


    