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
def get_product(product_id: int, db:Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.id==product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.post("/products")
def create_product(product:Product, db: Session = Depends(get_db)):
    new_product = ProductDB(name=product.name, price=product.price, in_stock=product.in_stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.put("/products/{product_id}")
def update_product(product_id:int, product:Product, db:Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.id==product_id).first()
    if product_id is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name=product.name
    db_product.price=product.price
    db_product.in_stock=product.in_stock
    db.commit()
    return {"updated":db_product.id, "product":product}

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db:Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.id==product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"deleted": db_product}

@app.get("/users/{user_id}")
def get_user(user_id:int, db:Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(ProductDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return db_user

@app.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = UserDB(name=user.name, surname = user.surname, phone_number = user.phone_number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.put("/users/{user_id}")
def change_user(user_id:int, user:User, db:Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id==user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.surname = user.surname
    db_user.phone_number = user.phone_number
    db.commit()
    return {"updated":db_user.id, "user": user}

@app.delete("/users/{user_id}")
def delete_user(user_id:int, db:Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id==user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"deleted":db_user}

@app.get("/workers/{worker_id}")
def get_worker(worker_id:int, db:Session = Depends(get_db)):
    db_worker = db.query(WorkerDB).filter(WorkerDB.id == worker_id).first()
    if db_worker is None:
        raise HTTPException(status_code=404, detail="worker not found")
    return db_worker

@app.post("/workers")
def create_worker(worker:Workers, db:Session = Depends(get_db)):
    new_worker = WorkerDB(name=worker.name, surname=worker.surname, role=worker.role)
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)
    return new_worker

@app.put("/workers/{worker_id}")
def change_worker(worker_id:int, worker:Workers, db:Session = Depends(get_db)):
    db_worker = db.query(WorkerDB).filter(WorkerDB.id==worker_id).first()
    if db_worker is None:
        raise HTTPException(status_code=404, detail="worker not found")
    db_worker.name = worker.name
    db_worker.surname = worker.surname
    db_worker.role = worker.role
    db.commit()
    return{"updated":db_worker.id, "worker":worker}

@app.delete("/workers/{worker_id}")
def delete_worker(worker_id:int, db:Session = Depends(get_db)):
    db_worker = db.query(WorkerDB).filter(WorkerDB.id==worker_id).first()
    if db_worker is None:
        raise HTTPException(status_code=404, detail="worker not found")
    db.delete(db_worker)
    db.commit()
    return{"deleted":db_worker}



    