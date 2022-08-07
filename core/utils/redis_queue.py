import redis


class RedisQueue:
    """
    Assignee: 김동규
    
    detail:
      > Redis queue
        * 레디스 큐(대기열)를 활용하여 동시성 문제 해결
        * 요청 데이터는 대기열의 왼쪽으로 하나씩 넣어줌
        * 대기열의 오른쪽에서 가장 빠르게 요청한 유저정보를 추출함
        
      > cf: Redis queue(List) info
        * Redis Lists are an ordered list, First In First Out Queue.
        * Redis List pushing new elements on the head(on the left) of the list.
        * Redis List popping first element on the tail(on the right) of the list.
        * The max length of a list is 4,294,967,295
    """
    
    def __init__(self, name, **redis_kwargs):
        """
        레디스 큐의 키와 유저 대기열(queue) 생성
        """
        self.key = name
        self.rq  = redis.Redis(**redis_kwargs)
    
    """
    큐(대기열) 크기 확인
    """    
    def qsize(self):
        return self.rq.llen(self.key)
    
    """
    큐의 데이터 존재여부 확인
    """
    def is_empty(self):
        return self.qsize() == 0
    
    """
    데이터 입력(left push)
    """
    def put(self, element):
        self.rq.lpush(self.key, element)
    
    """
    데이터 추출(right pop)
    """    
    def get(self, block=False, timeout=None):
        """
        blocking right pop
          - 큐(대기열)에 데이터가 존재하지 않으면, pop을 제한하고 데이터가 입력될 때까지 timeout만큼 대기 후 데이터 추출
          - element 인덱싱 0번: queue key
          - element 인덱싱 1번: queue data
        """
        if block:
            element = self.rq.brpop(self.key, timeout=timeout)
            element = element[1]
        else:
            element = self.rq.rpop(self.key)
        
        return element
    
    """
    대기열에 존재하는 모든 데이터 삭제
    """
    def clear(self):
        self.rq.flushall()