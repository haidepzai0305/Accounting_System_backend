from enum import Enum


# Giá trị phải khớp ENUM MySQL (thường là PENDING, APPROVED, REJECTED — chữ hoa)
class TransactionStatusEnum(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"