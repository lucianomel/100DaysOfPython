# Python arguments - advanced python arguments
# Arguments with default values -> def add(x=1,y):...

# Unlimited arguments
# Any number of arguments - UNLIMITED POSITIONAL ARGUMENTS
def add(*args):
    print(args[0])
    res = 0
    for n in args:
        res += n
    return res


print(add(1, 2, 3, 4, 5))


# Many keyword arguments
def calculate(n, **kwargs):
    n += kwargs["add"]
    n *= kwargs["multiply"]
    return n


# First add then multiply
print(calculate(2, add=3, multiply=5))

# Use of get keyword in kwargs
class Car:
    def __init__(self, **kw):
        # get -> if key doesn't exist, it returns None
        self.make = kw.get("make")
        self.model = kw.get("model")
        self.seats = kw.get("seats")


my_car = Car(make="Nissan")

print(my_car.make)
