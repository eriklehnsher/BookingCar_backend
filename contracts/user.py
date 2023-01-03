from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from contracts.pyObjectId import *


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    role: str = Field(...)
    vendor_state:  str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "ADMIN",
                "email": "admin@gmail.com",
                "password": "admin",
              
                "role": "",
                "vendor_state": ""
            }
        }


class UpdateUserModel(BaseModel):
    username: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    role: str = Field(...)
    vendor_state:  str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "ADMIN",
                "email": "admin@gmail.com",
                "password": "admin",
                "role": "",
                "vendor_state": ""
            }
        }
# Update_UserName-Model

class ChangeUserName(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "ADMIN",
            }
        }


class UpdateChangeUserName(BaseModel):
    username: str = Field(...)
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "ADMIN27",
            }
        }



# 

class UserLogin(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "admin@gmail.com",
                "password": "admin",
            }
        }


# vendor

class VendorModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    address: str = Field(...)
    phone: int = Field(...)
    carName: str = Field(...)
    role: str = Field(...)
    vendor_state:  str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "ADMIN",
                "address": "Hai Ba Trung",
                "phone": "19001781",
                "carName": "admin",
                "role": "",
                "vendor_state": ""
            }
        }


class UpdateVendorModel(BaseModel):
    username: str = Field(...)
    address: str = Field(...)
    phone: int = Field(...)
    carName: str = Field(...)
    role: str = Field(...)
    vendor_state:  str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "ADMIN",
                "address": "Hai Ba Trung",
                "phone": "19001781",
                "carName": "admin",
                "role": "",
                "vendor_state": ""
            }
        }
