""" Module for generating random quantities for setting up the list of `Particle` objects. """

from random import random, uniform
from numpy import isfinite
from numpy.linalg import norm
from src.data_types import Particles
from src.classes.config import Config
from src.classes.particle import Particle


##----- Single Properties -----##

def get_mass(max_mass: float):
    """ Returns single float value in the range (0, max_mass] """
    if max_mass <= 0:
        raise ValueError("Masses cannot be less than or equal to 0")
    if not isfinite(max_mass):
        raise ValueError("Maximum mass is too large")
    result = random()*max_mass
    if result == 0:
        return get_mass(max_mass)
    else:
        return result


def get_position(max_distance: float):
    """  """
    if max_distance <= 0:
        raise ValueError("Distances cannot be less than or equal to 0")
    if not isfinite(max_distance):
        raise ValueError("Maximum distance is too large")
    vector = [uniform(-1,1) for _ in range(3)]
    position = [ max_distance*x / norm(vector) for x in vector]
    return position


def get_velocity(max_speed: float):
    """  """
    if max_speed < 0:
        raise ValueError("Speeds cannot be less than 0")
    if not isfinite(max_speed):
        raise ValueError("Maximum speed is too large")
    vector = [uniform(-1,1) for _ in range(3) ]
    velocity = [ max_speed*x / norm(vector) for x in vector]
    return velocity


##----- Multiple Properties -----##

def n_is_valid(n: int) -> bool:
    """ Checks that n is a positive integer. """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    elif n == 0:
        raise ValueError("n must be at least 1")
    elif n < 0:
        raise ValueError("n cannot be negative")
    return True


def get_masses(n: int, max_mass: float):
    """  """
    return [get_mass(max_mass) for _ in range(n)]


def get_positions(n: int, max_distance: float):
    """  """
    return [get_position(max_distance) for _ in range(n)]


def get_velocities(n:int, max_speed: float):
    """  """
    return [get_velocity(max_speed) for _ in range(n)]


##----- Finalizing Particles -----##

def get_particle_config_data(config_object: Config) -> tuple[int, float, float, float]:
    """ Returns data from `config.yaml` relevant to creation of the particles. """
    n = config_object.number_of_particles
    max_mass = config_object.max_mass
    max_distance = config_object.max_distance
    max_speed = config_object.max_speed
    
    if n_is_valid(n):
        return n, max_mass, max_distance, max_speed


def get_random_particle_attributes(config_object: Config) -> tuple[list, list, list]:
    """ Returns tuple containing mass, position and velocity value lists used to initialise particles. """
    n, max_mass, max_distance, max_speed = get_particle_config_data(config_object)

    masses = get_masses(n, max_mass)
    positions = get_positions(n, max_distance)
    velocities = get_velocities(n, max_speed)

    return masses, positions, velocities


def get_configured_particles(config_object: Config) -> Particles:
    """ Returns a finalised list of particles. """
    masses, positions, velocities = get_random_particle_attributes(config_object)
    particles = [
        Particle(id=i, mass=masses[i], initial_position=positions[i], initial_velocity=velocities[i])
        for i in range(config_object.number_of_particles)
    ]
    return particles
