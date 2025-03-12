from numpy import array, isfinite, ndarray
from numpy.linalg import norm

class Particle:
    """ Instances represent individual particles involved in simulation. Information about their mass, position, velocity are stored here. """
    def __init__(self, id:int, mass:float, initial_position:list, initial_velocity:list):
        if not isinstance(id, int):
            raise TypeError("ID must be an integer")
        if not (0 <= id <= 16):
            raise ValueError("id must be within the range 0-16")
        self.id = id

        if not (isinstance(mass, float) or isinstance(mass, int)):
            raise TypeError("Mass is not a valid scalar value")
        if (mass <= 0):
            raise ValueError("Mass must be greater than 0")
        self.mass = mass

        if not (isinstance(initial_position, list) or isinstance(initial_position, ndarray)):
            raise TypeError("State variables must be an array or a list")
        if not isfinite(norm(initial_position)):
            raise ValueError("Starting distance is too large!")

        if not (isinstance(initial_velocity, list) or isinstance(initial_velocity, ndarray)):
            raise TypeError("State variables must be an array or a list")
        if not isfinite(norm(initial_velocity)):
            raise ValueError("Starting speed is too large!")
        
        if not (len(initial_position) == len(initial_velocity) == 3):
            raise TypeError("State variables are not 3 dimensional")
        
        self._position = array(initial_position)
        self._velocity = array(initial_velocity)

        self.next_position = None
        self.next_velocity = None
        
    """ attr: self.POSITION """
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    """ attr: self.VELOCITY """
    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    def momentum(self):
        return self.mass*self.velocity
    