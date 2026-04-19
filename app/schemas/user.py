from pydantic import BaseModel

class UserOut(BaseModel):
    email: str
    rol: str