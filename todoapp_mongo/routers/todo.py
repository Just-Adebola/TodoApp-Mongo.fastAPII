from fastapi import APIRouter
from todoapp_mongo.crud.todo import todo_crud
from ..schemas import todo as todo_schema

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("/", response_model=todo_schema.Todo)
def create_todo_endpoint(todo: todo_schema.TodoCreate):
    return todo_crud.create_todo(todo)


@router.get("/{todo_id}")
def get_user_endpoint(todo_id: str):
    return todo_crud.get_single_todo(todo_id)

@router.get("/")
def get_all_todo_endpoint():
    return todo_crud.get_all_todo()

@router.put("/{todo_id}")
def update_todo(todo_id: str, update: todo_schema.TodoCreate):
    upadated_todo = todo_crud.update_todo_endpoint(todo_id, update)
    return upadated_todo

@router.delete("/{todo_id}")
def delete_user(todo_id: str):
    return todo_crud.delete_todo(todo_id)