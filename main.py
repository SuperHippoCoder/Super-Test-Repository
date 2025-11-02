from typing import Annotated, Optional
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from contextlib import asynccontextmanager

from database import create_tables, delete_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("Очищено")
    await create_tables()
    print("Создано")
    yield
    print("Выключение")
    

app = FastAPI(lifespan=lifespan)

class STaskAdd(BaseModel):
    name : str
    description : Optional[str] = None

class STask(STaskAdd):
    id : int

tasks = []

@app.get("/tasks")
async def add_task(
    task : Annotated[STaskAdd, Depends()]
):
    tasks.append(task)
    return {"OK": True}

#@app.get("/tasks")
#def get_tasks():
    #task = STask(name="Какашка", description="Куа")
    #return {"data": task}