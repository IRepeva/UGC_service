BASE_LOG_FORMAT = "%(asctime)s.%(msecs)03d - %(levelname)s - %(module)s.%(funcName)s::%(lineno)d - %(message)s"
LOG_FORMAT = "%(asctime)s.%(msecs)03d - %(levelname)s - %(request_id)s - %(module)s.%(funcName)s::%(lineno)d - %(message)s"
NGINX_FORMAT = "%(asctime)s.%(msecs)03d - %(levelname)s - %(client_addr)s - %(request_id)s - '%(request_line)s' - %(status_code)s"
LOG_DEFAULT_HANDLERS = ['console', ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        'main': {
            'format': BASE_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': NGINX_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'formatter': 'base',
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
        'main': {
            'formatter': 'main',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'log': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'INFO',
        },
        'main': {
            'handlers': ['main', ],
            'level': 'INFO',
        },
        'uvicorn.error': {
            'level': 'INFO',
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
