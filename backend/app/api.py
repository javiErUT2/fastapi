from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

todos = [
    {
        "id": 1,
        "item": "Read Stephen King's Cujo"
    },
    {
        "id": 2,
        "item": "Go for shopping"
    },
    {
        "id": 3,
        "item": "Cook dinner"
    }
]

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Hello, World!"}

@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return { "data": todos }

@app.post("/todo", tags=["todos"])
async def add_todo(todo: dict) -> dict:
    todos.append(todo)
    return {
        "data": { "Todo added." }
    }

@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todo["item"] = body["item"]
            return {
                "data": f"Todo with id {id} has been updated."
            }

    return {
        "data": f"Todo with id {id} not found."
    }
    
@app.delete("/todo/{id}", tags=["todos"])
async def delete_todo(id: int) -> dict:
    global todos
    initial_length = len(todos)

    todos = [todo for todo in todos if int(todo["id"]) != id]

    if len(todos) < initial_length:
        return {
            "data": f"Todo with id {id} has been removed."
        }
    else:
        return {
            "data": f"Todo with id {id} not found."
        }
