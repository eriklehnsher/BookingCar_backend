from socket import create_server
from fastapi import APIRouter, Body, status, HTTPException
from contracts.user import UserLogin, UserModel, UpdateUserModel, VendorModel, UpdateVendorModel
from fastapi.encoders import jsonable_encoder
from db import db
from bson import ObjectId
from fastapi.responses import JSONResponse
from typing import List, Optional
from passlib.context import CryptContext
from contracts.token import *
import datetime
from jose import jwt
from config import settings


router = APIRouter()


def get_hashed_password(password: str):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)

# Register


@router.post("/user/register", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    email = user.dict()["email"]
    find_user_in_db = await db["Users"].find_one({"email": email})
    if find_user_in_db is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="email_already_used")
    else:
        user = user.dict()
        new_user = await db['Users'].insert_one(user)
        await db["Users"].update_one({"_id": new_user.inserted_id}, {"$set": {"password": get_hashed_password(user["password"])}})
        await db["Users"].update_one({"_id": new_user.inserted_id}, {"$set": {"role": "customer", "vendor_state": ""}})
        created_user = await db["Users"].find_one({"_id": new_user.inserted_id})
        return created_user

# vendor


@router.post("/vendor/register", response_model=VendorModel)
async def create_vendor(user: VendorModel = Body(...)):
    user = user.dict()
    new_user = await db['Users'].insert_one(user)
    await db["Users"].update_one({"_id": new_user.inserted_id}, {"$set": {"role": "customer", "vendor_state": "pending"}})
    created_user = await db["Users"].find_one({"_id": new_user.inserted_id})
    return created_user


    # email = user.dict()["email"]
    # find_user_in_db = await db["Users"].find_one({"email": email})
    # if find_user_in_db is not None:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email_already_used")
    # else:
    #     user = user.dict()
    #     new_user = await db['Users'].insert_one(user)
    #     await db["Users"].update_one({"_id": new_user.inserted_id}, {"$set": {"password": get_hashed_password(user["password"])}})
    #     await db["Users"].update_one({"_id": new_user.inserted_id}, {"$set": {"role": "customer", "vendor_state":"pending"}})
    #     created_user = await db["Users"].find_one({"_id": new_user.inserted_id})
    #     return created_user


@router.post("/vendor/approve/{id}", response_model=VendorModel)
async def approve_vendor(id: str):
    vendor = await db["Users"].find_one({"_id": ObjectId(id)})
    if vendor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    else:
        await db["Users"].update_one({"_id": ObjectId(id)}, {"$set": {"role": "vendor", "vendor_state": "approved"}})
        updated_vendor = await db["Users"].find_one({"_id": ObjectId(id)})
        return updated_vendor


@router.post("/vendor/reject/{id}", response_model=VendorModel)
async def approve_vendor(id: str):
    vendor = await db["Users"].find_one({"_id": ObjectId(id)})
    if vendor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    else:
        await db["Users"].update_one({"_id": ObjectId(id)}, {"$set": {"vendor_state": "rejected"}})
        updated_vendor = await db["Users"].find_one({"_id": ObjectId(id)})
        return updated_vendor

# get vendor


@router.get("/vendor/list-pending", response_model=List[VendorModel])
async def list_vendors():
    vendors = await db["Users"].find({'vendor_state': "pending"}).to_list(1000)
    return vendors


@router.get("/vendor/list-approved", response_model=List[VendorModel])
async def list_vendors():
    vendors = await db["Users"].find({'vendor_state': "approved"}).to_list(1000)
    return vendors


@router.get("/vendor/list-rejected", response_model=List[VendorModel])
async def list_vendors():
    vendors = await db["Users"].find({'vendor_state': "rejected"}).to_list(1000)
    return vendors

# Login


def verify_password(password: str, hashed_password: str):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(password, hashed_password)


async def authenticate_user(email: str, password: str):
    user = await db["Users"].find_one({"email": email})
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


@router.post("/user/login", response_model=Token)
async def login(user_data: UserLogin = Body(...)):
    user_data = user_data.dict()
    user = await authenticate_user(user_data["email"], user_data["password"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=300)
    if (user["role"] == "admin"):
        access_token_expires = datetime.timedelta(minutes=600)
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"],
              "name": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ADMIN: get all users
@router.get("/user/all", response_model=List[UserModel])
async def list_users():
    users = await db["Users"].find({'vendor_state': ""}).to_list(1000)
    return users

# Get a user


@router.get("/user/{id}", response_model=UserModel)
async def show_user(id: str):
    if (user := await db["Users"].find_one({"_id": ObjectId(id)})) is not None:
        return user
    raise HTTPException(status_code=404, detail="user {id} not found")



@router.get("/user/email/{email}", response_model=UserModel)
async def get_user_by_email(email: str):
    if (user := await db["Users"].find_one({"email": email})) is not None:
        return user
    raise HTTPException(status_code=404, detail="user {id} not found")



# Update a user


@router.put("/user/{id}", response_model=UserModel)
async def update_user(id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await db["Users"].update_one({"_id": ObjectId(id)}, {"$set": user})

        if update_result.modified_count == 1:
            if (
                updated_user := await db["Users"].find_one({"_id": ObjectId(id)})
            ) is not None:
                return updated_user

    if (existing_user := await db["Users"].find_one({"_id": ObjectId(id)})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.delete("/user/{id}")
async def delete_user(id: str):
    delete_result = await db["Users"].delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Deleted successfully"})

    raise HTTPException(status_code=404, detail=f"User {id} not found")
