from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    title : str
    desc: str
    due : str
    status : str

class UpdateTodo(BaseModel):
    title : Optional[str]= None
    desc : Optional[str]= None
    due : Optional[str]= None
    status : Optional[str]= None

todoList = {
    1: Todo(title = "WebApp API", desc = "Build FAST API Todo List", due = "8 May 2023", status = "Completed"),
    2: Todo(title = "Games FP", desc = "Horror game", due = "15 May 2023", status = "On Going"),
    3: Todo(title = "CompNet Forum", desc = "Clients ping each other", due = "15 May 2023", status = "On Going"),
}

filteredList ={
    1: Todo(title = "Filtered", desc = "Filtered", due = "Filtered", status = "Filtered")
}

@app.get("/")
def index():
    return { "Test" : "It works!"}

#Return by ID
@app.get("/get-todo/{id}")
def get_todo(id : int = Path(description = "ToDo ID")):
    if id in todoList:
        return todoList[id]
    return {"Error" : "ToDo ID doesn't exist."}

#Return by title
@app.get("/get-todo-by-title/{title}")
def get_todo(title : str): 
    for todo_id in todoList:
        if todoList[todo_id].title == title:
            return todoList[todo_id]
    return {"Error" : "ToDo Title doesn't exist."}

#Filtered with due
@app.get("/get-todo-by-due/{due}")
def get_todo(due : str): 
    global filteredList
    filteredList.clear() #Otherwise the previous filtered is still there
    for todo_id in todoList:
        # Filteredlist added
        if todoList[todo_id].due == due:
            filteredList[todo_id] = todoList[todo_id]
    return filteredList

#Filtered with status
@app.get("/filter-by-status/{status}")
def get_todo(status: str):
    global filteredList
    filteredList.clear() #Otherwise the previous filtered is still there
    for todo_id in todoList:
        # Filteredlist added
        if todoList[todo_id].status == status:
            filteredList[todo_id] = todoList[todo_id]
    return filteredList

#POST method (Add)
@app.post("/create-todo/{todo_id}")
def add_todo(todo_id: int, todo : Todo):
    if todo_id in todoList:
        return {"Error" : "ToDo ID is already available."}
    todoList[todo_id] = todo
    return todoList[todo_id]

#PUT method (Update)
@app.put("/update-todo/{todo_id}")
def update_todo(todo_id: int, todo: UpdateTodo):
    if todo_id not in todoList:
        return {"Error" : "ToDo ID doesn't exist"}
    if todo.title != None:
        todoList[todo_id].title = todo.title
    if todo.desc != None:
        todoList[todo_id].desc = todo.desc
    if todo.due != None:
        todoList[todo_id].due = todo.due
    if todo.status != None:
        todoList[todo_id].status = todo.status    
    return todoList[todo_id]

#DELETE method
@app.delete("/delete-todo/{todo_id}")
def delete_todo(todo_id:int):
    if todo_id not in todoList:
        return {"Error" : "ToDO ID is not available"}
    del todoList[todo_id]
    return {"Status" : "ToDo Deleted"}