import numpy as np

class Queue:
    maxSize = 0
    queue = []

    def __init__(self, maxSize):
        self.maxSize = maxSize

    def put(self, value):
        if len(self.queue) < self.maxSize:
            self.queue.append(value)
        else:
            self.queue.pop(0)
            self.queue.append(value)

    def contains(self, item):
        index = 0
        isContain = False
        for element in self.queue:
            if np.array_equal(element, item):
                isContain = True
                return isContain, index
            index += 1
        return isContain, index

    def remove(self, index):
        del self.queue[index]
