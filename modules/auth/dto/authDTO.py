from pydantic import BaseModel


class userDTO(BaseModel):
    username: str
    email: str
    password: str

class authDTO(BaseModel):
    email: str
    password: str

class userTokenDTO(BaseModel):
    username: str
    email: str
