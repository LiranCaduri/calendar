from typing import Optional

from pydantic import BaseModel


class CurrentUser(BaseModel):
    """
    Validating fields types
    Returns a user details as a class.
    """
    user_id: Optional[int]
    username: str
    features: Optional[dict]
    is_manager: Optional[bool]

    class Config:
        orm_mode = True


class LoginUser(CurrentUser):
    """
    Validating fields types
    Returns a User object for signing in.
    """
    password: str
