# from random import random, randint
import random
import json
import numpy as np
from tests.config import TestConfig
from src.simulation import initialise_random_particles

    
CONFIG = TestConfig()

random.seed("testing purposes")

def utils_random_mass():
    result = random.random()*CONFIG.max_mass
    if result == 0:
        return utils_random_mass()
    else:
        return result

def utils_random_distance():
    return random.random()*CONFIG.max_distance


def utils_random_speed():
    return random.random()*CONFIG.max_speed


def utils_get_test_particles(n=None, max_mass=None, max_distance=None, max_speed=None):

    #* Potential errors here will be handled by the initialise_random_particles function
    if n==None:
        final_n = random.randint(1, 16)
    else:
        final_n = n

    if max_mass == None:
        final_mass = random.random()*CONFIG.max_mass
    else:
        final_mass = max_mass

    if max_distance == None:
        final_distance = random.random()*CONFIG.max_distance
    else:
        final_distance = max_distance
        
    if max_speed == None:
        final_speed = random.random()*CONFIG.max_speed
    else:
        final_speed = max_speed

    particles = initialise_random_particles(final_n, final_mass, final_distance, final_speed)

    return particles


def utils_calculate_total_momentum(particles: dict):
    total_momentum = np.array([.0,.0,.0], dtype=np.float64)
    for particle in particles.values():
        total_momentum += particle.momentum()
    return total_momentum

def utils_particles_to_json(n=None, max_mass=None, max_distance=None, max_speed=None):

    test_cases = dict()
    for case_number in range(10):
        particles_data = dict()
        particles = utils_get_test_particles(n, max_mass, max_distance, max_speed)
        for particle in particles.values():
            particles_data[particle.id] = {
                "mass": particle.mass,
                "position": [float(coord) for coord in particle.position],
                "velocity": [float(vel) for vel in particle.velocity]
            }
        test_cases[case_number] = { "particles data" : particles_data }

    data = { "test cases" : test_cases }
    json_data = json.dumps(data, indent=4)
    with open("tests/example_particles.json", 'w') as jsonfile:
        # jsonfile.write(json_data)
        pass

def utils_get_example_particles():
    ...