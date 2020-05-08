import logging.config


def configureCliLogging():
    """Configure the logging for the case when the program is ran as standalone code."""
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s %(name)-15s [%(levelname)-8s] %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'stream': 'ext://sys.stderr',
                'formatter': 'detailed',
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'disable_existing_loggers': False,
    })
