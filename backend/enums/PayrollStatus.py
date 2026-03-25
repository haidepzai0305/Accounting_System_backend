from enum import Enum


class PayrollStatusEnum(Enum):
    DRAFT = "draft"
    CALCULATED = "calculated"
    APPROVED = "approved"
    PAID = "paid"