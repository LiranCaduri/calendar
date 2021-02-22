from typing import Optional

from pydantic import BaseModel


class CurrentUser(BaseModel):
    """
    Validating fields types
    Returns a user details as a class.
    """
    user_id: Optional[int]
    features: Optional[dict]
    username: str
    
    class Config:
        orm_mode = True


class LoginUser(CurrentUser):
    """
    Validating fields types
    Returns a User object for signing in.
    """
    password: str
    is_manager: Optional[bool]


class UpdateFeatures(CurrentUser):
    """
    Validating fields types
    Returns a User object for signing in.
    """
    is_manager: Optional[bool] = False
