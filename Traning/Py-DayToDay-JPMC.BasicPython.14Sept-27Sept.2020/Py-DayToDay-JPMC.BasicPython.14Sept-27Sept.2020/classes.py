class MyInt:
    def __init__(self, v): #1
        self.inner_value = v 
    def __add__(self, other): #2
        z = self.inner_value + other.inner_value 
        return z 
    def __str__(self): #3
        return "MyInt("+str(self.inner_value)+")"
    def square(self):
        return self.inner_value**2

