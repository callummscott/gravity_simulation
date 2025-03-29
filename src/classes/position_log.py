from numpy import ndarray as array

class PositionLog:
    def __init__(self):
        self.xs = []
        self.ys = []
        self.zs = []

    def cache_position(self, value):
        """ Adds an (x,y,z) position tuple """
        if type(value) != array:
                raise TypeError
        try:
            x,y,z = value
            self.xs.append(x)
            self.ys.append(y)
            self.zs.append(z)
        except Exception:
            if len(value) != 3:
                raise IndexError("Position not 3 dimensional")
            for item in value:
                try:
                    float(item)
                except TypeError as e:
                    raise e("Coordinates not a valid numerical value")

    def get_xyz_tuple(self):
        return (self.xs, self.ys, self.zs)