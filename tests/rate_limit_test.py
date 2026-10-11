import redis
from concurrent.futures import ThreadPoolExecutor

redis_client = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses=True
)


REDIS_SCRIPT = """
    local count = redis.call("INCR" , KEYS[1])
    if count == 1 then
        redis.call("EXPIRE" , KEYS[1] , ARGV[1])
    end
    if count > tonumber(ARGV[2]) then
        return 0
    end
    return 1
"""

MAX_REQUESTS = 5
WINDOW_SECONDS = 60
key= "rate-lmit:test_user"

TOTAL_REQ = 1000

redis_client.delete(key)

def send_req():
    return redis_client.eval(
        REDIS_SCRIPT,
        1,
        key,
        WINDOW_SECONDS,
        MAX_REQUESTS
    )

with ThreadPoolExecutor(max_workers=100) as executor:
    results = list(
        executor.map(
            lambda _: send_req(),
            range(TOTAL_REQ)
        )
    )

allowed_count = sum(1 for result in results if result == 1)
rejected_count = sum(1 for result in results if result == 0)

final_count = int(redis_client.get(key))

print("Requests sent:", TOTAL_REQ)
print("Allowed:", allowed_count)
print("Rejected:", rejected_count)
print("Final Redis counter:", final_count)
print("TTL:", redis_client.ttl(key))

assert allowed_count == MAX_REQUESTS
assert rejected_count == TOTAL_REQ - MAX_REQUESTS
assert final_count == TOTAL_REQ

print("Rate limit concurrency test passed!")