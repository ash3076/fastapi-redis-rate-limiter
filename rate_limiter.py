from fastapi import Request, HTTPException
from redis_client import redis_client

MAX_REQUESTS = 5
WINDOW_SECONDS = 60

# Lua script executes inside Redis
RATE_LIMIT_SCRIPT = """
local count = redis.call("INCR", KEYS[1])

if count == 1 then
    redis.call("EXPIRE", KEYS[1], ARGV[1])
end

return count
"""


def rate_limit(request: Request):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"

    # Execute the Lua script inside Redis
    request_count = redis_client.eval(
        RATE_LIMIT_SCRIPT,
        1,              # Number of Redis keys
        key,            # KEYS[1] , key value 
        WINDOW_SECONDS  # ARGV[1] , and window size of teh expiration 
    )

    # Reject requests exceeding the limit
    if request_count > MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Try again later."
        )