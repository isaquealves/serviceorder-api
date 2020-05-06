from flask_redis import FlaskRedis

redis = FlaskRedis()
cache = FlaskRedis(config_prefix="REDIS_CACHE")

redisClient = redis.provider_class()
cacheClient = cache.provider_class(db=2)
