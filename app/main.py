import uvicorn
from urllib.request import Request
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from starlette.responses import JSONResponse

from app.api.routes.index import router as api_router
from app.helper import connect, close
from fastapi_jwt_auth.exceptions import AuthJWTException, AccessTokenRequired
from pydantic import BaseModel
from config.app_config import HOST, PORT, INDEX


def get_application() -> FastAPI:
    application = FastAPI(title="EMBL-app")
    return application


app = FastAPI(title="EMBL-app")
app.include_router(api_router, prefix='/api')


@app.on_event('startup')
async def on_startup() -> None:
    await connect(HOST, PORT, INDEX)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close()


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AccessTokenRequired):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
