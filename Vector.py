import math


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other, self.y - other)

    def normalize(self):

        self.x = self.x / self.length()
        self.y = self.y / self.length()

    def length(self):
        self.length = math.sqrt(self.x ** 2 + self.y ** 2)
        if self.length <= 0: self.length = 1
        return self.length
