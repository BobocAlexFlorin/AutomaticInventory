import requests
from .config import settings




def push_to_snipeit(device: dict):
if not settings.snipeit_url or not settings.snipeit_token:
return {'status': 'skipped', 'reason': 'Snipe-IT not configured'}


url = f"{settings.snipeit_url.rstrip('/')}/api/v1/hardware"
headers = {
'Authorization': f'Bearer {settings.snipeit_token}',
'Accept': 'application/json'
}
payload = {
'asset_tag': device['SerialNumber'],
'name': device.get('Model') or 'Unknown model',
'notes': 'Imported from lightweight scanner',
}
r = requests.post(url, json=payload, headers=headers)
return {'status_code': r.status_code, 'body': r.json() if r.content else None}