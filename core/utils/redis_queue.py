import redis


class RedisQueue:
    
    def __init__(self, name, **redis_kwargs):
        self.key = name
        self.rq  = redis.Redis(**redis_kwargs)
        
    def qsize(self):
        return self.rq.llen(self.key)
    
    def is_empty(self):
        return self.qsize() == 0
    
    def put(self, element):
        self.rq.lpush(self.key, element)
        
    def get(self, block=False, timeout=None):
        if block:
            element = self.rq.brpop(self.key, timeout=timeout)
            element = element[1]
        else:
            element = self.rq.rpop(self.key)
        
        return element
    
    def clear(self):
        self.rq.flushall()