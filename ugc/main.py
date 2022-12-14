import contextvars
import logging
import uuid

import sentry_sdk
import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from logstash_async.handler import AsynchronousLogstashHandler
from motor.motor_asyncio import AsyncIOMotorClient
from sentry_sdk.integrations.fastapi import FastApiIntegration

from core.logger import LOGGING
from core.settings import settings
from src.api.v1 import films, users
from src.db import mongo

sentry_sdk.init(integrations=[FastApiIntegration()])
_request_id = contextvars.ContextVar(
    'request_id', default=f'system:{uuid.uuid4()}'
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = (
        request.headers.get('X-Request-Id') or f'direct:{uuid.uuid4()}'
    )
    _request_id.set(request_id)
    return await call_next(request)


factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = factory(*args, **kwargs)
    record.request_id = _request_id.get()
    return record


app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.INFO)
logstash_handler = AsynchronousLogstashHandler('logstash', 5044, None)
logging.setLogRecordFactory(record_factory)
app.logger.addHandler(logstash_handler)


@app.on_event('startup')
async def startup():
    mongo_uri = f"mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}"
    try:
        mongo.mongo = AsyncIOMotorClient(mongo_uri)
        logging.info(f'mongodb {mongo_uri} successfully connected')
    except (ConnectionError, Exception) as e:
        logging.exception(
            f'Cannot connect to mongo {mongo_uri} \n Exception: {e}'
        )


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
