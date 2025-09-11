from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db, Base
from .config import settings


# Create tables at startup (for prototype)
Base.metadata.create_all(bind=engine)


app = FastAPI(title='Inventory Scanner API')


@app.post('/scan', response_model=schemas.DeviceOut)
def scan_device(payload: schemas.ScanInput, db: Session = Depends(get_db)):
# Basic validation: ensure user exists (create quick user if missing for prototype)
user = db.query(models.User).filter(models.User.Id == payload.user_id).first()
if not user:
# Create a stub user so devices can be assigned (prototype behavior)
user = models.User(Id=payload.user_id, Name=f'User {payload.user_id}', Email=None)
db.add(user)
db.commit()
db.refresh(user)


# Prevent duplicate serials
existing = db.query(models.Device).filter(models.Device.SerialNumber == payload.serial_number).first()
if existing:
raise HTTPException(status_code=400, detail='Serial number already exists')


device = crud.create_device(db, payload.serial_number, payload.vendor, payload.model, payload.user_id)


# optional: push to Snipe-IT
try:
from .snipeit import push_to_snipeit
push_to_snipeit({
'SerialNumber': device.SerialNumber,
'Model': device.Model,
'Vendor': device.Vendor,
'UserId': device.UserId
})
except Exception:
pass


# Build response
category = db.query(models.Category).filter(models.Category.Id == device.CategoryId).first()
return schemas.DeviceOut(
id=device.Id,
serial_number=device.SerialNumber,
vendor=device.Vendor,
model=device.Model,
category=category.Name if category else None,
user_id=device.UserId,
date_added=device.DateAdded
)


@app.get('/users/{user_id}/devices')
def list_user_devices(user_id: int, db: Session = Depends(get_db)):
devices = crud.get_devices_for_user(db, user_id)
results = []
for d in devices:
cat = db.query(models.Category).filter(models.Category.Id == d.CategoryId).first()
results.append({
'id': d.Id,
'serial_number': d.SerialNumber,
'vendor': d.Vendor,
'model': d.Model,
'category': cat.Name if cat else None,
'user_id': d.UserId,
'date_added': d.DateAdded
})
return results


@app.get('/devices')
def search(q: str | None = None, db: Session = Depends(get_db)):
if not q:
# return first 100
devices = db.query(models.Device).limit(100).all()
else:
devices = crud.search_devices(db, q)
out = []
for d in devices:
cat = db.query(models.Category).filter(models.Category.Id == d.CategoryId).first()
out.append({