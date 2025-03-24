from ..serializers import user as serializer
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from bson.objectid import ObjectId
from ..schemas.user import UserCreate, UserUpdate, User
from ..database import user_collection


class UserCrud:

    @staticmethod
    def create_user(user_data: UserCreate):
        user_data = jsonable_encoder(user_data)
        user_document_data = user_collection.insert_one(user_data)
        user_id = user_document_data.inserted_id
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        return serializer.user_serializer(user)
    
    @staticmethod
    def get_single_user(user_id):
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return serializer.user_serializer(user)
    
    @staticmethod
    def get_all_users():
        documents = list(user_collection.find())
        for doc in documents:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        return jsonable_encoder(documents)
    
    @staticmethod
    def update_user_endpoint(user_id: str, update: UserUpdate):
        user = {"_id": ObjectId(user_id)}
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        update_data = {"$set": update.model_dump(exclude_unset=True)}
        updated_user = user_collection.update_one(user, update_data)
        updated_user = user_collection.find_one({"_id": ObjectId(user_id)})
        return serializer.user_serializer(updated_user)
    
    @staticmethod
    def delete_user(user_id: str):
        user = {"_id": ObjectId(user_id)}
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        deleted = user_collection.delete_one(user)
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Succesfully deleted!")



user_crud = UserCrud()