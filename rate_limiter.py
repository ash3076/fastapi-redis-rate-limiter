from fastapi import Request, HTTPException
from redis_client import redis_client


MAX_REQUESTS = 5
WINDOW_SECONDS = 60


def rate_limit(request: Request):
    client_ip = request.client.host

    key = f"rate_limit:{client_ip}"

    request_count = redis_client.incr(key)

    if request_count == 1:
        redis_client.expire(key, WINDOW_SECONDS)

    if request_count > MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Try again later."
        )