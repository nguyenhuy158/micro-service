from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    VENDOR = "vendor"


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


class StockStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    OUT_OF_STOCK = "out_of_stock"
