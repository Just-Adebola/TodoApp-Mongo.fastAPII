from ..serializers import todo as serializer
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from bson.objectid import ObjectId
from ..schemas.todo import TodoCreate
from ..database import todo_collection


class TodoCrud:

    @staticmethod
    def create_todo(todo_data: TodoCreate):
        todo_data = jsonable_encoder(todo_data)
        todo_document_data = todo_collection.insert_one(todo_data)
        todo_id = todo_document_data.inserted_id
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        return serializer.todo_serializer(todo)
    

    @staticmethod
    def get_single_todo(todo_id):
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")
        return serializer.todo_serializer(todo)
    

    @staticmethod
    def get_all_todo():
        documents = list(todo_collection.find())
        for doc in documents:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        return jsonable_encoder(documents)
    
    @staticmethod
    def update_todo_endpoint(todo_id: str, update: TodoCreate):
        todo = {"_id": ObjectId(todo_id)}
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")
        update_data = {"$set": update.model_dump(exclude_unset=True)}
        updated_user = todo_collection.update_one(todo, update_data)
        updated_user = todo_collection.find_one({"_id": ObjectId(todo_id)})
        return serializer.todo_serializer(updated_user)
    
    @staticmethod
    def delete_todo(todo_id: str):
        todo = {"_id": ObjectId(todo_id)}
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="todo not found.")
        deleted = todo_collection.delete_one(todo)
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Succesfully deleted!")

    



todo_crud = TodoCrud()