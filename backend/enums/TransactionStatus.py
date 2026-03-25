from enum import Enum


class TransactionStatusEnum(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"