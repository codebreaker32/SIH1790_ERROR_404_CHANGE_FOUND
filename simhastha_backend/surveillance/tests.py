
import redis

# Create a Redis connection (ensure Redis is running on the specified host/port)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Test Redis connection
print("Testing Redis...")
r.set('test_key', 'test_value')
result = r.get('test_key')

if result:
    print(f"Redis is working! Stored value: {result.decode()}")
else:
    print("Redis is not working correctly.")
