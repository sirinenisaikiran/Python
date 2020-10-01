import functools

@functools.total_ordering
class MyInt:
    def __init__(self, value):
        self.v = value 
    def __str__(self):
        return "MyInt(%d)" % ( self.v,)
    def __add__(self, other):
        return MyInt(self.v + other.v)
    def __sub__(self, other):
        return MyInt(self.v - other.v)
    def square(self):
        return self.v * self.v 
    def __eq__(self, other):
        return self.v == other.v
    def __lt__(self, other):
        return self.v < other.v