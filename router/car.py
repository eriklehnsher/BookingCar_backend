from fastapi import APIRouter,Body,status, HTTPException
from contracts.car import CarModel, UpdateCarModel
from fastapi.encoders import jsonable_encoder
from db import db
from fastapi.responses import JSONResponse
from typing import Optional, List

router = APIRouter()

#Create a car
@router.post("/car/create", response_model=CarModel)
async def create_car(car: CarModel=Body(...)):
    car = jsonable_encoder(car)
    new_car = await db['Cars'].insert_one(car)
    created_car = await db["Cars"].find_one({"_id": new_car.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)

#Get all car
@router.get(
    "/car/all", response_model=List[CarModel]
)
async def list_cars():
    cars = await db["Cars"].find().to_list(1000)
    return cars

#Get a car by id
@router.get(
    "/car/{id}", response_model=CarModel
)
async def get_id(id: str):
    if (car := await db["Cars"].find_one({"_id": id})) is not None:
        return car

    raise HTTPException(status_code=404, detail="Car {id} not found")


#Update a car
@router.put("/car/{id}", response_model=CarModel)
async def update_id(id: str, car: UpdateCarModel = Body(...)):
    car = {k: v for k, v in car.dict().items() if v is not None}

    if len(car) >= 1:
        update_result = await db["Cars"].update_one({"_id": id}, {"$set": car})

        if update_result.modified_count == 1:
            if (
                updated_car := await db["car"].find_one({"_id": id})
            ) is not None:
                return updated_car

    if (existing_car := await db["Cars"].find_one({"_id": id})) is not None:
        return existing_car

    raise HTTPException(status_code=404, detail="Car {id} not found")

#Delete a car

@router.delete("/car/{id}")
async def delete_car(id: str):
    delete_result = await db["Cars"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Deleted successfully"})

    raise HTTPException(status_code=404, detail=f"Car {id} not found")


#booking a car 

