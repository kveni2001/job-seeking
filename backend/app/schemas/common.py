from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T")


class ORMBaseModel(BaseModel):
    """Base model with ORM mode / from_attributes enabled for SQLAlchemy compatibility."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TimestampSchema(ORMBaseModel):
    """Timestamp mixin schema for models tracking creation and updates."""
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")


class IDSchema(ORMBaseModel):
    """UUID Primary Key schema."""
    id: UUID = Field(..., description="Unique UUID identifier")


class MessageResponse(BaseModel):
    """Standard message response for simple actions or confirmations."""
    message: str = Field(..., description="Human-readable response message")
    success: bool = Field(default=True, description="Indicates whether the operation succeeded")


class ErrorDetail(BaseModel):
    """Detailed error object."""
    field: Optional[str] = Field(None, description="Field name where error occurred")
    message: str = Field(..., description="Error description message")


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str = Field(..., description="Primary error message")
    code: Optional[str] = Field(None, description="Machine-readable error code")
    errors: Optional[List[ErrorDetail]] = Field(None, description="List of granular errors")


class PaginationParams(BaseModel):
    """Query parameters for pagination."""
    page: int = Field(default=1, ge=1, description="Page number starting at 1")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page (max 100)")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated wrapper response."""
    items: List[T] = Field(..., description="List of items for current page")
    total: int = Field(..., ge=0, description="Total count of items matching filter")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, description="Number of items per page")
    total_pages: int = Field(..., ge=0, description="Total number of pages")

    model_config = ConfigDict(from_attributes=True)
