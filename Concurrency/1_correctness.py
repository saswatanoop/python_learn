'''
1. Coarse-Grained Locking:
    - One lock for entire critical section
    - Simple but can cause contention   
    - Special case: 
    1.1 Reader-Writer Lock (multiple readers, single writer)
'''

# 1. Coarse-Grained Locking Example
import threading    

class BookTicket:
    
    def __init__(self):
        self.tickets={}
        self._lock=threading.Lock()
    
    def add_new_ticket(self,key,val):
        with self._lock:
            if key not in self.tickets:
                self.tickets[key]=val
    
    def get_ticket_owner(self,key):
        with self._lock:
            if key in self.tickets:
                return self.tickets[key]

# 1.1 Reader-Writer Lock Example(Heavy read, light write)
# The code below has starvation issue, as if there are too many readers, the writer will never get a chance to acquire the lock and update the cache. 
class Cache:
    
    def __init__(self):
        self._cache = {}
        self._lock=threading.Lock()
        self._read_count=0
        self._read_count_lock=threading.Lock()
    
    # Heavy read
    def get_value(self, key):
        registered = False
        try:
            with self._read_count_lock:
                self.read_count += 1
                registered = True
                # need to acquire lock on cache, as first thread is going to read
                if self.read_count == 1:
                    self._lock.acquire()

            return self._cache.get(key)
        finally:
            # only if registered, reduce the read count lock only if it was increased
            if registered:
                with self._read_count_lock:
                    self.read_count -= 1
                    if self.read_count == 0:
                        self._lock.release()
    
    def set_value(self,key,value):
        with self._lock:
            self._cache[key]=value
        
                