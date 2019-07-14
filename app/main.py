from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from databases import Database

from models import devices, measurements
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


class DeviceCreate(BaseModel):
    name: str


class Device(DeviceCreate):
    id: int


class MeasurementCreate(BaseModel):
    device_id: int
    reading: float


##########
# ROUTES #
##########


@app.get('/devices', response_model=List[Device])
async def read_devices():
    return await db.fetch_all(devices.select())


@app.post('/devices', response_model=Device)
async def create_device(device: DeviceCreate) -> Device:
    id = await db.execute(devices.insert(device.dict()))
    return {**device.dict(), 'id': id}


@app.post('/measurements', response_model={})
async def create_measurement(measurement: MeasurementCreate):
    id = await db.execute(measurements.insert(measurement.dict()))
    return {}
