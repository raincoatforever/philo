import heapq
import time


class MaxHeap(object):
    def __init__(self):
        self.heap = []

    def push(self, value):
        heapq.heappush(self.heap, (-int(time.time()), value))

    def pop(self):
        tuple = heapq.heappop(self.heap)
        return -tuple[0], tuple[1]

    def peek(self):
        tuple = self.heap[0]
        return -tuple[0], tuple[1]

    def print_heap(self):
        print self.heap

    def remove(self, thread_id):
        index = -1
        for item in self.heap:
            index += 1
            if item[1] == thread_id:
                break

        self.heap[index] = self.heap[-1]
        removed = self.heap.pop()
         #print "removing %s " % (removed,)
        heapq.heapify(self.heap)

    def size(self):
        return len(self.heap)

    def full(self):
        return self.size() == 100