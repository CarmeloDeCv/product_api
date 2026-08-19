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

class Workers(BaseModel):
    name:str
    surname:str
    company_id:int


products={}
users={}
workers={}
workers_next_id=1
users_next_id=1
products_next_id=1

@app.get("/")
def home():
    return {"message": "It works"}

@app.get("/products")
def list_products():
    return products

@app.get("/users")
def list_users():
    return users

@app.get("/workers")
def list_workers():
    return workers

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]

@app.post("/products")
def create_product(product:Product):
    global products_next_id
    products[products_next_id] = product
    created_id = products_next_id
    products_next_id += 1
    return {"id":created_id, "product":product}

@app.put("/products/{product_id}")
def update_product(product_id:int, product:Product):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
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
        raise HTTPException(status_code=404, detail = "User not found")
    return users[user_id]

@app.post("/users")
def create_user(user: User):
    global users_next_id
    users[users_next_id]=user
    created_user_id=users_next_id
    users_next_id+=1
    return {"id":created_user_id, "user":user}

@app.put("/users/{user_id}")
def change_user(user_id:int, user:User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id]=user
    return {"updated":user_id, "user": user}

@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return {"deleted":user_id}

@app.get("/workers/{worker_id}")
def get_worker(worker_id:int):
    if worker_id not in workers:
        raise HTTPException(status_code=404, detail="worker not found")
    return workers[worker_id]

@app.post("/workers")
def create_worker(worker:Workers):
    global workers_next_id
    workers[workers_next_id]=worker
    created_worker_id=workers_next_id
    workers_next_id+=1
    return{"id":created_worker_id, "worker":worker}

@app.put("/workers/{worker_id}")
def change_worker(worker_id:int, worker:Workers):
    if worker_id not in workers:
        raise HTTPException(status_code=404, detail="worker not found")
    workers[worker_id]= worker
    return{"updated":worker_id, "worker":worker}

@app.delete("/workers/{worker_id}")
def delete_worker(worker_id:int):
    if worker_id not in workers:
        raise HTTPException(status_code=404, detail="worker not found")
    del workers[worker_id]
    return{"deleted":worker_id}



    