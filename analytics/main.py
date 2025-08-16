from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.analytics import router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown complete")

app = FastAPI(title="Analytics Microservice", lifespan=lifespan)

app.include_router(router, prefix="/analytics")

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}
