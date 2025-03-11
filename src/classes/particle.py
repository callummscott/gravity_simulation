from numpy import array

class Particle:
    """ Instances represent individual particles involved in simulation. Information about their mass, position, velocity are stored here. """
    def __init__(self, id:int, mass:float, initial_position:list, initial_velocity:list):
        self.id = id
        self.mass = mass
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

    @classmethod
    def from_test_case(cls, data):
        return Particle(len(data), data["mass"], data["position"], data["velocity"])
        # mass = float
        # position = [x,y,z]
        # velocity = []
    
    