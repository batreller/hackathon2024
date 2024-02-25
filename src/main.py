import logging
import sys

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src import config
from src.auth.router import router as auth_router
from src.cars.router import router as cars_router

logging.basicConfig(stream=sys.stdout, level=config.LOGGING_LEVEL)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(cars_router, prefix="/cars", tags=["Cars"])

if __name__ == "__main__":
    import uvicorn

    # todo use uvloop for NOT windows
    uvicorn.run(app, host="localhost", port=7070)
    # uvicorn.run(app, host="127.0.0.1", port=7000)
