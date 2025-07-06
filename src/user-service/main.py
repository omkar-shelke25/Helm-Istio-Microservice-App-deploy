from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import os

app = FastAPI()

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()
users_collection = db.users

# Pydantic models
class User(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

def to_object_id(id: str):
    try:
        return ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

# Routes
@app.post("/users/", response_model=dict)
async def create_user(user: User):
    try:
        user_dict = user.dict()
        result = users_collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        return user_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=dict)
async def get_user(user_id: str):
    try:
        oid = to_object_id(user_id)
        user = users_collection.find_one({"_id": oid})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user["_id"] = str(user["_id"])
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/", response_model=list[dict])
async def list_users():
    try:
        users = list(users_collection.find())
        for user in users:
            user["_id"] = str(user["_id"])
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/users/{user_id}", response_model=dict)
async def update_user(user_id: str, user_update: UserUpdate):
    try:
        oid = to_object_id(user_id)
        update_dict = {k: v for k, v in user_update.dict().items() if v is not None}
        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")
        result = users_collection.update_one({"_id": oid}, {"$set": update_dict})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        user = users_collection.find_one({"_id": oid})
        user["_id"] = str(user["_id"])
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    try:
        oid = to_object_id(user_id)
        result = users_collection.delete_one({"_id": oid})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=dict)
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
