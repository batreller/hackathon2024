import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import sys

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src import config
from src.auth.router import router as auth_router
from src.cars.router import router as cars_router
from src.frontend.router import router as frontend_router

logging.basicConfig(stream=sys.stdout, level=config.LOGGING_LEVEL)

app = FastAPI()

app.mount("/static", StaticFiles(directory='templates', html=True), name="templates")

app.include_router(frontend_router, tags=["Frontend"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(cars_router, prefix="/cars", tags=["Cars"])

if __name__ == "__main__":
    import uvicorn

    # todo use uvloop for NOT windows
    uvicorn.run(app, host="localhost", port=8080)
