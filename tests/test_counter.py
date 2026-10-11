import redis 

#  setup connection 

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# lua script 

REDIS_SCRIPT= """
    local count = redis.call("INCR",KEYS[1])

    if count == 1 then
        redis.call("EXPIRE",KEYS[1],ARGV[1])
    end

    return count
"""

key = "rate-limi:test_user"

# delete any prev key stored
redis_client.delete(key)

# execute teh lua script
for i in range(1,20):
    count = redis_client.eval(
        REDIS_SCRIPT,
        1,
        key,
        10

    )
    ttl = redis_client.ttl(key)

    print(
        f"Request: {i}, "
        f"Counter: {count}, "
        f"TTL: {ttl}"
    )

