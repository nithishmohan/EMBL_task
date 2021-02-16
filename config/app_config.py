from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Token"  # noqa: S105 在做用户校验时，需要把这个前缀加上，并加空格
VERSION = "1.0.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

HOST:str = config("HOST",cast=str,default="127.0.0.1")
PORT:int = config("PORT",cast=int,default=6379)
INDEX: int = config("PORT", cast=int, default=0)

TEST_HOST:str = config("HOST",cast=str,default="127.0.0.1")
TEST_PORT:int = config("PORT",cast=int,default=6379)
TEST_INDEX: int = config("PORT", cast=int, default=1)

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=""
)
