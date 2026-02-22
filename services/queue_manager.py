import heapq

class TicketQueue:
    def __init__(self):
        self._queue = []
        self._index = 0  # Tie-breaker for tickets with the same priority

    def push(self, ticket: dict):
        # Priority 0 is highest (urgent), Priority 1 is normal
        priority = 0 if ticket["is_urgent"] else 1
        
        # heapq sorts by the first element of the tuple. 
        # If priorities match, it sorts by _index (FIFO)
        heapq.heappush(self._queue, (priority, self._index, ticket))
        self._index += 1

    def pop(self):
        if not self._queue:
            return None
        # Return the actual ticket dictionary (index 2 of the tuple)
        return heapq.heappop(self._queue)[2]

    def size(self):
        return len(self._queue)

# Global singleton instance for single-threaded execution
ticket_queue = TicketQueue()