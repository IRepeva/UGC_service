import logging

import sentry_sdk
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from logstash_async.handler import AsynchronousLogstashHandler
from motor.motor_asyncio import AsyncIOMotorClient
from sentry_sdk.integrations.fastapi import FastApiIntegration

from core.logger import LOGGING
from core.settings import settings
from src.api.v1 import films, users
from src.db import mongo

sentry_sdk.init(integrations=[FastApiIntegration()])

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.INFO)
logstash_handler = AsynchronousLogstashHandler('logstash', 5044, None)
app.logger.addHandler(logstash_handler)


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
    try:
        await mongo.mongo.close()
        logging.debug('mongodb successfully closed')
    except Exception as e:
        logging.exception(
            f'The following exception occurred while closing connection: {e}'
        )


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
