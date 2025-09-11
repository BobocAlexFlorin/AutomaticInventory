from sqlalchemy.orm import Session
from . import models


# Simple rule-based categorization
CATEGORY_RULES = {
'thinkvision': 'Monitor',
'iphone': 'Phone',
'latitude': 'Laptop',
'logitech': 'Peripheral',
}




def auto_categorize(vendor: str | None, model: str | None) -> str:
if model:
m = model.lower()
for k, v in CATEGORY_RULES.items():
if k in m:
return v
if vendor:
vnd = vendor.lower()
for k, v in CATEGORY_RULES.items():
if k in vnd:
return v
return 'Unknown'




def create_device(db: Session, serial_number: str, vendor: str | None, model: str | None, user_id: int):
# find or create category
category_name = auto_categorize(vendor, model)
cat = db.query(models.Category).filter(models.Category.Name == category_name).first()
if not cat:
cat = models.Category(Name=category_name, Description=f'Auto-created for {category_name}')
db.add(cat)
db.commit()
db.refresh(cat)


device = models.Device(
SerialNumber=serial_number,
Vendor=vendor,
Model=model,
CategoryId=cat.Id,
UserId=user_id
)
db.add(device)
db.commit()
db.refresh(device)
return device




def get_devices_for_user(db: Session, user_id: int):
return db.query(models.Device).filter(models.Device.UserId == user_id).all()




def search_devices(db: Session, q: str):
q_like = f"%{q}%"
return db.query(models.Device).filter(
(models.Device.SerialNumber.ilike(q_like)) |
(models.Device.Vendor.ilike(q_like)) |
(models.Device.Model.ilike(q_like))
).all()