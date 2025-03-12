""" Methods to generate and supply particle data for simulation purposes """

from random import random, uniform
from numpy import isfinite
from src.classes.config import Config

CONFIG = Config()


def vector_length(vector: list):
    return sum(x**2 for x in vector)**.5


##----- Single Proprties -----##
def get_mass(max_mass: float):
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
    if max_distance <= 0:
        raise ValueError("Distances cannot be less than or equal to 0")
    if not isfinite(max_distance):
        raise ValueError("Maximum distance is too large")
    vector = [uniform(-1,1) for _ in range(3)]
    length = vector_length(vector)
    position = [ max_distance*x / length for x in vector]
    return position

def get_velocity(max_speed: float):
    if max_speed < 0:
        raise ValueError("Speeds cannot be less than 0")
    if not isfinite(max_speed):
        raise ValueError("Maximum speed is too large")
    vector = [uniform(-1,1) for _ in range(3) ]
    length = vector_length(vector)
    velocity = [ max_speed*x / length for x in vector]
    return velocity


##----- Multiple properties -----##
def get_masses(N: int, max_mass: float):
    if not isinstance(N, int):
        raise TypeError("n is not an integer")
    elif N > 16:
        raise ValueError("Too many particles (>16) for the number of colours available")
    elif N == 0:
        raise ValueError("At least one mass must be specified")
    elif N < 0:
        raise ValueError("n cannot be negative")
    return [get_mass(max_mass) for _ in range(N)]


def get_positions(N: int, max_distance: float):
    if not isinstance(N, int):
        raise TypeError
    elif N > 16:
        raise ValueError("Too many particles (>16) for the number of colours available")
    elif N == 0:
        raise ValueError("At least one number must be specified")
    elif N < 0:
        raise ValueError("n cannot be negative")
    return [get_position(max_distance) for _ in range(N)]


def get_velocities(N, max_speed):
    if not isinstance(N, int):
        raise TypeError
    elif N > 16:
        raise ValueError("Too many particles (>16) for the number of colours available")
    elif N == 0:
        raise ValueError("At least one number must be specified")
    elif N < 0:
        raise ValueError("n cannot be negative")
    return [get_velocity(max_speed) for _ in range(N)]


def get_random_input_variables(n: int, max_mass, max_distance, max_speed):
    """ Returns pre-packaged tuple of all random config-constrained input variables for n particles"""
    CONFIG.logger.info("Gathering input variables")

    masses = get_masses(n, max_mass)
    positions = get_positions(n, max_distance)
    velocities = get_velocities(n, max_speed)

    return (masses, positions, velocities)