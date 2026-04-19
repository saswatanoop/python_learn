'''
1. Coarse-Grained Locking:
    - One lock for entire critical section
    - Simple but can cause contention   
    - Special case: 
    1.1 Reader-Writer Lock (multiple readers, single writer)
    
2. Fine-Grained Locking:
    - One lock per resource instead of one lock for everything. Threads only block when competing for the same resource
    - More complex but can improve performance by reducing contention
'''

# 1. Coarse-Grained Locking Example
import threading    

class BookTicket:
    
    def __init__(self):
        self.tickets={}
        self._lock=threading.Lock()
    
    def add_new_ticket(self,key,val)-> None:
        with self._lock:
            if key not in self.tickets:
                self.tickets[key]=val
    
    def get_ticket_owner(self,key)-> str|None:
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

# 2. Fine-Grained Locking Example

class TicketBookingFineGrained:
    def __init__(self):
        self._locks_lock = threading.Lock() #Acquire this lock before accessing the lock map
        self._seat_locks = {} # Map of seat_id to its lock
        self._seat_owners = {} # Map of seat_id to visitor_id who booked it

    def _get_lock(self, seat_id: str) -> threading.Lock:
        # protect the lock map itself
        with self._locks_lock:
            if seat_id not in self._seat_locks:
                self._seat_locks[seat_id] = threading.Lock()
            return self._seat_locks[seat_id]

    def book_seat(self, seat_id: str, visitor_id: str) -> bool:
        with self._get_lock(seat_id):
            if seat_id in self._seat_owners:
                return False
            self._seat_owners[seat_id] = visitor_id
            return True
    
    def swap_seats(self, visitor1: str, seat1: str,
                   visitor2: str, seat2: str) -> bool:
        # Always acquire locks in consistent order to prevent deadlock
        first = seat1 if seat1 < seat2 else seat2
        second = seat2 if seat1 < seat2 else seat1

        with self._get_lock(first):
            with self._get_lock(second):
                # validate ownership
                if self._seat_owners.get(seat1) != visitor1:
                    return False
                if self._seat_owners.get(seat2) != visitor2:
                    return False
                # actual swap
                self._seat_owners[seat1] = visitor2
                self._seat_owners[seat2] = visitor1
                return True