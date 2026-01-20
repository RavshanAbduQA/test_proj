"""Pydantic models for API schema validation."""
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class Geo(BaseModel):
    """Geographic coordinates model."""
    lat: str
    lng: str


class Address(BaseModel):
    """User address model."""
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(BaseModel):
    """Company model."""
    name: str
    catchPhrase: str
    bs: str


class User(BaseModel):
    """User model."""
    id: int
    name: str
    username: str
    email: EmailStr
    address: Address
    phone: str
    website: str
    company: Company


class Post(BaseModel):
    """Post model."""
    userId: int = Field(..., gt=0, description="User ID must be positive")
    id: int = Field(..., gt=0, description="Post ID must be positive")
    title: str = Field(..., min_length=1, description="Title cannot be empty")
    body: str = Field(..., min_length=1, description="Body cannot be empty")


class PostCreate(BaseModel):
    """Model for creating a new post."""
    userId: int = Field(..., gt=0)
    title: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)


class PostUpdate(BaseModel):
    """Model for updating a post."""
    userId: Optional[int] = Field(None, gt=0)
    id: Optional[int] = Field(None, gt=0)
    title: Optional[str] = Field(None, min_length=1)
    body: Optional[str] = Field(None, min_length=1)


class Comment(BaseModel):
    """Comment model."""
    postId: int = Field(..., gt=0, description="Post ID must be positive")
    id: int = Field(..., gt=0, description="Comment ID must be positive")
    name: str = Field(..., min_length=1, description="Name cannot be empty")
    email: EmailStr
    body: str = Field(..., min_length=1, description="Body cannot be empty")

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """Validate email format."""
        if '@' not in v or '.' not in v.split('@')[1]:
            raise ValueError('Invalid email format')
        return v
