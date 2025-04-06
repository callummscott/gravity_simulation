import pytest
from numpy import array, ndarray
from logging import getLogger, basicConfig, INFO
from src.motion_calcs import initialise_particles


class Particle:
    def __init__(self, id: int, mass: float, position: ndarray, velocity: ndarray, acceleration=None) -> None:
        self.id = id
        self.mass = mass
        self.position = array(position)
        self.velocity = array(velocity)
        self.acceleration = array(acceleration)

    def __repr__(self):
        return f"Particle({self.id}, {self.mass:.2g}, ...)"


class Config:
    """ For testing purposes only """
    __test__ = False
    def __init__(
            self, 
            number_of_particles: int = 4,
            max_mass: float = 100,
            max_distance: float = 10,
            max_speed: float = 1,
            timesteps: int = 1_000,
            G: float = 1,
            collision_distance: float = 1e-4,
            dt: float = 0.001,
            random_seed : int = 1
        ):
        self.number_of_particles = number_of_particles
        self.max_mass = max_mass
        self.max_distance = max_distance
        self.max_speed = max_speed
        self.timesteps = timesteps
        self.G = G
        self.collision_distance = collision_distance
        self.dt = dt
        self.random_seed = random_seed
        self.half_dtsq = .5 * self.dt**2
        self.simple_log_rate = int(self.number_of_particles *  self.timesteps / 1_000)

    logger = getLogger(__name__)
    basicConfig(
        filename="testing.log",
        level=INFO,
        format='%(asctime)s [%(levelname)s] %(module)s > %(funcName)s: %(message)s',
        datefmt='%I:%M:%S',
        filemode="w"
    )


@pytest.fixture
def config(request):
    return Config(**request.param) if hasattr(request, "param") else Config()


@pytest.fixture
def particles_data():
    particles_data = [
        (1, [-1, 1, 1], [-.1, .1, .1]),
        (10, [1, -1, -1], [.1, .1, -.1]),
        (1e3, [10,10,10], [1, -1, 1]),
        (1e5, [1e3,1e3,1e3], [100, -100, 100]),
        (1e10, [-1e6,1e6,-1e6], [-1e5, -1e5, 1e5]),
        (15.2, [124.2,23.2,54.32], [0.3,2.23,1.8]),
        (100, [23.32, 21.32, 43.63], [-2.12, 0.45, -.99]),
        (776.4, [137.54, 776.23, -561.4], [7.67, -23.51, 71.57]),
        (5_454, [3_443, 3_875, -8_432], [54.67, -65.67, 11.256]),
        (54.433e3, [412_322, -323_566, 862_654], [-434.54, 863.52, -776.23]),
    ]
    return particles_data


# Indices are dependent upon the size of the above `particles_data` list.
@pytest.fixture(params=[
    ([0, 1, 2]),
    ([5, 4, 2]),
    ([1, 4, 2, 8]),
    ([5, 6, 7, 8, 9]),
    ([3, 4, 5, 6, 7, 8, 9]),
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
])
def particles(particles_data, request):
    indices = request.param
    assert max(indices) < len(particles_data) # A small test-check
    particles = [ Particle(index, *particles_data[index]) for index in indices ]
    return particles


@pytest.fixture
def initialised_particles(particles):
    initialise_particles(particles, Config())
    return particles


# indices are dependent upon length of particles
@pytest.fixture(params=[i for i in range(10)])
def particle(particles_data, request):
    index = request.param
    return Particle(0, *particles_data[index])
