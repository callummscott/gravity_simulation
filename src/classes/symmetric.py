from numpy import zeros, ndarray, float64

class Symmetric(ndarray):
    """ Class to define symmetric matrices that serve to represent distances -- theoretically saves (n-1)/2n ~= 40% the distance calculations. """
    # Has problems with non-2d-element-specific assignment.
    def __new__(cls, n: int):
        if not isinstance(n, int):
            raise TypeError("n is not an integer.")
        if n < 1:
            raise ValueError("Value must be greater than 0.")
        obj = zeros((n, n), dtype=float64).view(cls)
        return obj

    def __setitem__(self, index, value):
        
        if value < 0:
            raise ValueError("Distance cannot be less than 0!")
        if not isinstance(index, slice): #? Don't remember why this was important tbh
            try:
                i, j = index
            except TypeError:
                print("Indexing cannot be unpacked as 2-tuple.")
                raise
            
            if not (isinstance(i, int) and isinstance(j, int)):
                raise IndexError("Index must be a tuple of two integers")
            if ((i < 0) or (j < 0)) or ((i > self.shape[0]) or (j > self.shape[1])):
                raise ValueError("Indexing is out of range")
            
            if i == j:
                self.data[i, i] = 0 # was 'value'
            else:
                self.data[i, j] = value
                self.data[j, i] = value

    def __array_finalize__(self, obj):
        if obj is None: return

    def __repr__(self):
        return f"symmetric({self.__array__().__str__()})"
