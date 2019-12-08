from typing import List, Dict
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Schema
from databases import Database
from asyncpg.exceptions import ForeignKeyViolationError

from users_request import get_current_user
import models
import data_analys as da
from settings import DATABASES
from schemas import User

app = FastAPI()
db = Database(DATABASES['development']['url'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

#########
# SETUP #
#########


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()


###########
# SCHEMAS #
###########

class DeviceBase(BaseModel):
    name: str


class DeviceCreate(DeviceBase):
    pass


class Device(DeviceBase):
    id: int
    name:str
    active: bool  #If turned on by user
    connected: bool #If a connection can be etablished


class Reading(BaseModel):
    reading: float
    timedelta: int = Schema(..., description=(
        'Milliseconds from reading the value to sending the request'
    ))


class MeasurementCreate(BaseModel):
    readings: List[Reading]


class Message(BaseModel):
    message: str


class Event(BaseModel):
    id: int
    datetime: str
    count: int

##########
# ROUTES #
##########

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return user

@app.get('/events/{device_id}', response_model=List[Event])
async def read_events(device_id: int):
    query = "SELECT * FROM measurements WHERE device_id = :device_id"
    data = await db.fetch_all(query = query, values = {"device_id": device_id})
    if data is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return da.get_events(data)


@app.get('/devices', response_model=List[Device])
async def read_devices():
    return await db.fetch_all(models.devices.select())

@app.get('/device/{device_id}', response_model=Device)
async def read_device(device_id: int):
    query = "SELECT id, name, active, connected FROM devices WHERE id = :device_id"
    return await db.fetch_one(query = query, values = {"device_id": device_id})


@app.post('/devices', response_model=Device)
async def create_device(device: DeviceCreate):
    id = await db.execute(models.devices.insert(device.dict()))
    return {**device.dict(), 'id': id}


@app.post('/device/{device_id}', response_model=Message)
async def create_measurements(device_id: int, measurements: MeasurementCreate):
    
    query = "SELECT active FROM devices WHERE id = :device_id"
    active = await db.fetch_one(query = query, values = {"device_id": device_id})
    if( active['active'] == True ):
        current_time = datetime.now()
        to_insert = [{
            'reading': measurement.reading,
            'device_id': device_id,
            'created_at': (
                current_time + timedelta(milliseconds=measurement.timedelta)
            ),
        } for measurement in measurements.readings]
        try:
            await db.execute(models.measurements.insert(to_insert))
            return {'message': 'Measurements successfully inserted'}
        except ForeignKeyViolationError:
            msg = 'No device with this id'
            raise HTTPException(status_code=404, detail=msg)
    else:
        print(device_id, "Insert not executed)")


@app.post('/device/{device_id}/activate', response_model=Message)
async def update_settings(device_id: int):
    query = "UPDATE devices SET active= True WHERE id= :device_id"
    try:
        await db.execute(query = query, values = {"device_id": device_id})
        return {'message': 'Device setting updated'}
    except ForeignKeyViolationError:
        msg = 'No device with this id'
        raise HTTPException(status_code=404, detail=msg)

@app.post('/device/{device_id}/deactivate', response_model=Message)
async def update_settings(device_id: int):
    query = "UPDATE devices SET active= FALSE WHERE id= :device_id" 
    try:
        await db.fetch_one(query = query, values = {"device_id": device_id})
        return {'message': 'Device updated'}
    except ForeignKeyViolationError:
        msg = 'No device with this id'
        raise HTTPException(status_code=404, detail=msg)