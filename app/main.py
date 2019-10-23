from typing import List
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Schema
from databases import Database
from asyncpg.exceptions import ForeignKeyViolationError

import models
import data_analys as da
from settings import DATABASES


app = FastAPI()
db = Database(DATABASES['development']['url'])


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

@app.get('/events/{device_id}', response_model=List[Event])
async def read_events(device_id: int):
    data = await db.fetch_all(models.measurements.select().where(models.measurements.device_id == device_id))
    if data is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return da.get_events(data)


@app.get('/devices', response_model=List[Device])
async def read_devices():
    return await db.fetch_all(models.devices.select())


@app.post('/devices', response_model=Device)
async def create_device(device: DeviceCreate):
    id = await db.execute(models.devices.insert(device.dict()))
    return {**device.dict(), 'id': id}


@app.post('/device/{device_id}', response_model=Message)
async def create_measurements(device_id: int, measurements: MeasurementCreate):
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
