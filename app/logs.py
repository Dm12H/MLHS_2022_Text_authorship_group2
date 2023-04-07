import logging
from fastapi import Request


def log_connection(logger: logging.Logger, id: int, request: Request):
    logger.info(f'session {id}: request to {request.url.path} from {request.client.host}')


def log_duration(logger: logging.Logger, id: int, duration: float):
    logger.info(f'session {id}: spend {duration:.2f}ms on request')