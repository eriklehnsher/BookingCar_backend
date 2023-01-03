from dataclasses import field
from datetime import date, datetime
from telnetlib import STATUS
from this import s
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from contracts.pyObjectId import *


class CarModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    type: str = Field(...) 
    seat: str = Field(...)
    battCapa: str = Field(...)
    fuel: str = Field(...)
    desc: str = Field(...)
    features: List[str] = Field(...)
    requiredDocuments: List[str] = Field(...)
    collateral: int = Field(...)
    price: int = Field(...)
    address: object = Field(...)
    images: List[object] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "MITSUBISHI 2019",
                "type": "xe-tu-lai",
                "seat": "2",
                "battCapa": "32,26 kwh",
                "fuel": "diesel",
                "desc": "short description",
                "features": ["map", "gps", "tire"],
                "requiredDocuments": ["cmnd", "gplx"],
                "collateral": 500,
                "price": 1000,
                "address":{"district":"","ward":"","addressDetail":""},
                "images": []
            }
        }


# car: Type, version, price,
class UpdateCarModel(BaseModel):
    name: Optional[str]
    type: Optional[str]
    seat: Optional[str]
    battCapa: Optional[str]
    fuel: Optional[str]
    desc: Optional[str]
    features: List[str]
    requiredDocuments:  List[str]
    collateral: Optional[int]
    price: Optional[int]
    address: object = Field(...)
    images: List[str] = Field(...)

    


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "MITSUBISHI 2019",
                "type": "xe-tu-lai",
                "seat": "2",
                "battCapa": "32,26 kwh",
                "fuel": "diesel",
                "desc": "short description",
                "features": ["map", "gps", "tire"],
                "requiredDocuments": ["cmnd", "gplx"],
                "collateral": 500,
                "price": 1000,
                "address":{"district":"","ward":"","addressDetail":""},
                "images": []
            }
        }


