from fastapi import FastAPI
import uvicorn


def get_application() -> FastAPI:
    application = FastAPI(title="EMBL-app")
    return application


app = get_application()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

