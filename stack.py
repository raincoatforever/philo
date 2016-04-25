class Stack:
    def __init__(self):
        self.items = []

    def empty(self):
        return len(self.items) == 0

    def full(self):
        return len(self.items) == 100

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def print_stack(self):
        print self.items