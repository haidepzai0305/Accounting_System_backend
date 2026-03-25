from datetime import datetime
import uuid

from backend.models import AuditLog , db


def create_audit_log(user_id, action, table_name, record_id=None, old_value=None, new_value=None):
    log = AuditLog(
        log_id=f"LOG{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:4]}",
        user_id=user_id,
        action=action,
        table_name=table_name,
        record_id=record_id,
        old_value=old_value,
        new_value=new_value,
        timestamp=datetime.utcnow()
    )

    db.session.add(log)