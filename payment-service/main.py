from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os
import httpx

app = FastAPI()

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database()
payments_collection = db.payments

# Pydantic models
class Payment(BaseModel):
    order_id: str
    amount: float
    status: str  # e.g., "pending", "completed", "failed"

class PaymentUpdate(BaseModel):
    status: str | None = None
    amount: float | None = None

# Routes
@app.post("/payments/", response_model=dict)
async def create_payment(payment: Payment):
    try:
        # Verify order exists by calling Order Service
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{os.getenv('ORDER_SERVICE_URL')}/orders/{payment.order_id}")
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="Order not found")
        
        payment_dict = payment.dict()
        result = payments_collection.insert_one(payment_dict)
        payment_dict["_id"] = str(result.inserted_id)  # Convert ObjectId to string
        return payment_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/payments/{payment_id}", response_model=dict)
async def get_payment(payment_id: str):
    try:
        payment = payments_collection.find_one({"_id": payment_id})
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        # Fetch order details from Order Service
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{os.getenv('ORDER_SERVICE_URL')}/orders/{payment.order_id}")
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="Order not found")
            order = response.json()
        
        payment["_id"] = str(payment["_id"])  # Convert ObjectId to string
        return {"payment": payment, "order": order}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/payments/", response_model=list[dict])
async def list_payments():
    try:
        payments = list(payments_collection.find())
        for payment in payments:
            payment["_id"] = str(payment["_id"])  # Convert ObjectId to string
        return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/payments/{payment_id}", response_model=dict)
async def update_payment(payment_id: str, payment_update: PaymentUpdate):
    try:
        update_dict = {k: v for k, v in payment_update.dict().items() if v is not None}
        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")
        result = payments_collection.update_one({"_id": payment_id}, {"$set": update_dict})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Payment not found")
        payment = payments_collection.find_one({"_id": payment_id})
        payment["_id"] = str(payment["_id"])  # Convert ObjectId to string
        return payment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/payments/{payment_id}", response_model=dict)
async def delete_payment(payment_id: str):
    try:
        result = payments_collection.delete_one({"_id": payment_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Payment not found")
        return {"message": "Payment deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=dict)
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)
