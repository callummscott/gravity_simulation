""" Module for generating random quantities for setting up the list of `Particle` objects. """

import numpy.random as random
from numpy.linalg import norm
from numpy import array

from src.data_types import Particles
from src.classes.config import Config
from src.classes.particle import Particle


def get_initial_random_particle_attributes(seed: int, config_object: Config) -> tuple:
    """ Takes in a `seed` and a `config_object` and generates a tuple of random (`mass`, `position`, `velocity`) values for generating a `Particle`. """
    rng = random.default_rng(seed)

    mass = config_object.max_mass * (1 - rng.random()) #* (1-x) strat avoids the possibility of 0.

    def unit_vector():
        """ Marsaglia (1972) """
        x, y, z = rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)
        while (x**2 + y**2 + z**2) > 1:
            x = rng.uniform(-1, 1)
            y = rng.uniform(-1, 1)
            z = rng.uniform(-1, 1)
        return array([x, y, z])
        
    position = config_object.max_distance * unit_vector()
    velocity = config_object.max_speed * unit_vector()

    return (mass, position, velocity)


def get_configured_particles(config_object: Config) -> Particles:
    """ Takes in a `Config` instance. Returns a finalised list of `Particles`. """
    seed = config_object.random_seed
    random_attributes = lambda x : get_initial_random_particle_attributes(x, config_object)
    particles = [
        Particle(i, *random_attributes(seed + i)) for i in range(config_object.number_of_particles)
    ]
    return particles