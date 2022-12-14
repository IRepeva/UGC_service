import logging

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from src.api.v1 import films, users
from src.core.config import settings
from src.core.logger import LOGGING
from src.db import mongo

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    mongo_uri = f"mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}"
    try:
        mongo.mongo = AsyncIOMotorClient(mongo_uri)
        logging.info('mongodb %s successfully connected', mongo_uri)
    except (ConnectionError, Exception) as e:
        logging.exception('Cannot connect to mongo %s', mongo_uri)


@app.on_event("shutdown")
async def shutdown():
    await mongo.mongo.close()
    logging.debug('mongodb successfully closed')


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(users.router, prefix='/api/v1/users', tags=['users'])


if __name__ == '__main__':
    uvicorn.run(
        'main:src',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_config=LOGGING,
        log_level='info'
    )
