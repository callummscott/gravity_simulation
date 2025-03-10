from numpy import zeros, ndarray, float64

class Symmetric(ndarray):
    """ Class to define symmetric matrices that serve to represent distances -- theoretically saves (n-1)/2n ~= 40% the distance calculations. """
    # Has problems with non-2d-element-specific assignment.
    def __new__(cls, n: int):
        obj = zeros((n, n), dtype=float64).view(cls)
        return obj

    def __setitem__(self, index, value):
        if not isinstance(index, slice):
            i, j = index
            if not (isinstance(i, int) and isinstance(j, int)):
                raise IndexError("Index must be a tuple of two integers")
            if i == j:
                self.data[i, i] = 0 # was 'value'
            else:  # Not sure if this check is actually faster than the double-assignment
                self.data[i, j] = value
                self.data[j, i] = value

    def __array_finalize__(self, obj):
        if obj is None: return

    def __repr__(self):
        return f"symmetric({self.__array__().__str__()})"
