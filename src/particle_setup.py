""" Module for generating random quantities for setting up the list of `Particle` objects. """

import numpy.random as random

from src.data_types import Particles
from src.classes.config import Config
from src.classes.particle import Particle


def get_initial_random_particle_attributes(seed: int, config_object: Config) -> tuple:
    """ Takes in a `seed` and a `config_object` and generates random attribute values for generating `Particles`. """
    rng = random.default_rng(seed)

    mass = config_object.max_mass * (1 - rng.random()) #* (1-x) strat avoids the possibility of 0.
    position = config_object.max_distance * rng.standard_normal(3)
    velocity = config_object.max_speed * rng.standard_normal(3)

    return (mass, position, velocity)


def get_configured_particles(config_object: Config) -> Particles:
    """ Returns a finalised list of particles. """
    seed = config_object.random_seed
    random_attributes = lambda x : get_initial_random_particle_attributes(x, config_object)
    particles = [
        Particle(i, *random_attributes(seed + i)) for i in range(config_object.number_of_particles)
    ]
    return particles