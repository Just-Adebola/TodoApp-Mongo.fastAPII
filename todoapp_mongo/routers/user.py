from fastapi import APIRouter
from ..crud.user import user_crud
from ..schemas import user as user_schema

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user_endpoint(user: user_schema.UserCreate):
    return user_crud.create_user(user)

@router.get("/{user_id}")
def get_user_endpoint(user_id: str):
    return user_crud.get_single_user(user_id)

@router.get("/")
def get_all_users_endpoint():
    return user_crud.get_all_users()

@router.put("/{user_id}")
def update_user(user_id: str, update: user_schema.UserUpdate):
    upadated_user = user_crud.update_user_endpoint(user_id, update)
    return upadated_user 

@router.delete("/{user_id}")
def delete_user(user_id: str):
    return user_crud.delete_user(user_id)