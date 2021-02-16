from pydantic import BaseModel


class Person(BaseModel):
    first_name: str
    last_name: str
    age: str
    favourite_color: str


class Name(BaseModel):
    first_name: str
    last_name: str


class User(BaseModel):
    username: str
    password: str
