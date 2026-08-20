from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Boolean 
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session 
from fastapi import Depends
app = FastAPI()

class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)


class WorkerDB(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key= True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    role = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

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
    role:str


products={}
users={}
workers={}
workers_next_id=1
users_next_id=1
products_next_id=1

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "It works"}

@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(ProductDB).all()

@app.get("/users")
def list_users(db:Session = Depends(get_db)):
    return db.query(UserDB).all()

@app.get("/workers")
def list_workers(db:Session = Depends(get_db)):
    return db.query(WorkerDB).all()

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]

@app.post("/products")
def create_product(product:Product, db: Session = Depends(get_db)):
    new_product = ProductDB(name=product.name, price=product.price, in_stock=product.in_stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

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
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = UserDB(name=user.name, surname = user.surname, phone_number = user.phone_number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

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
def create_worker(worker:Workers, db:Session = Depends(get_db)):
    new_worker = WorkerDB(name=worker.name, surname=worker.surname, role=worker.role)
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)
    return new_worker

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



    