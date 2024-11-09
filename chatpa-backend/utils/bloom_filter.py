from django.conf import settings
import hashlib
import redis

class BloomFilter:
    def __init__(self, redis_client, key, size, hash_count):
        self.redis_client = redis_client
        self.key = key
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [False] * self.size

    def _hash(self, item, seed):
        hash_obj = hashlib.md5(f"{item}-{seed}".encode())
        return int(hash_obj.hexdigest(), 16) % self.size
    
    def add(self, item, seed):
        for i in range(self.hash_count):
            index = self._hash(item, i)
            self.redis.setbit(self.key, index, 1)
    
    def contains(self, item):
        for i in range(self.hash_count):
            index = self._hash(item, i)
            if not self.redis.getbit(self.key, index):
                return False
        return True
    