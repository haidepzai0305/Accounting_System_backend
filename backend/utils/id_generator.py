import uuid
from datetime import datetime

def generate_id(prefix):
    return f"{prefix}{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:4]}"