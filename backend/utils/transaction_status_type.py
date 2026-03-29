"""
Kiểu cột status cho cash_in / cash_out: tránh lỗi khi MySQL ENUM hoặc dữ liệu cũ
dùng chữ thường (approved) trong khi SQLAlchemy.Enum chỉ chấp nhận một tập giá trị cố định.
"""
from sqlalchemy import TypeDecorator, String

from backend.enums.TransactionStatus import TransactionStatusEnum


class TransactionStatusType(TypeDecorator):
    """Lưu VARCHAR/ENUM dưới dạng PENDING|APPROVED|REJECTED; đọc mọi biến thể chữ hoa/thường."""

    impl = String(20)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, TransactionStatusEnum):
            return value.value
        s = str(value).strip().upper()
        if s in ("PENDING", "APPROVED", "REJECTED"):
            return s
        low = str(value).strip().lower()
        legacy = {"pending": "PENDING", "approved": "APPROVED", "rejected": "REJECTED"}
        return legacy.get(low, "PENDING")

    def process_result_value(self, value, dialect):
        if value is None:
            return TransactionStatusEnum.PENDING
        s = str(value).strip().upper()
        if s in ("PENDING", "APPROVED", "REJECTED"):
            return TransactionStatusEnum[s]
        low = str(value).strip().lower()
        mapping = {
            "pending": TransactionStatusEnum.PENDING,
            "approved": TransactionStatusEnum.APPROVED,
            "rejected": TransactionStatusEnum.REJECTED,
        }
        return mapping.get(low, TransactionStatusEnum.PENDING)
