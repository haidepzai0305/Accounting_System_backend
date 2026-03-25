from datetime import datetime

from backend.models import AuditLog,db
from backend.utils.id_generator import generate_id


def create_audit_log(user_id, action, table_name, record_id=None, old_value=None, new_value=None):

    log = AuditLog(
        log_id=generate_id("LOG"),
        user_id=user_id,
        action=action,
        table_name=table_name,
        record_id=record_id,
        old_value=old_value,
        new_value=new_value,
        timestamp=datetime.utcnow()
    )

    db.session.add(log)