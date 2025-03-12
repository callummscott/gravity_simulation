# from random import random, randint
import random
import json
import numpy as np
from tests.config import TestConfig
from src.classes.particle import Particle
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


def utils_get_test_particles(n=None, max_mass=None, max_distance=None, max_speed=None) -> dict[int:Particle]:
    """ Takes in constraints on random test particles and returns a dictionary of particles """
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

def utils_calculate_total_momentum(particles: dict) -> np.ndarray:
    """ Takes in a particles dictionary as input, returns total momentum numpy array """
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
        # jsonfile.write(json_data) #* Commented to stop me from accidentally using it.
        pass

def utils_get_test_case_to_particles_dict() -> dict[int:dict]:
    with open("tests/example_particles.json", "r") as jsonfile:
        json_data = json.load(jsonfile)
        test_cases_dict = dict()
        for key, value in json_data["test cases"].items():
            assert key.isdigit()
            # Parse JSON formatting into more python-friendly dict format.
            test_case_id = int(key)
            test_case_data = value["particles data"]
            test_cases_dict[test_case_id] = test_case_data

    #* Builds a {test_id: particles} dictionary out of stored particle data
    test_case_to_particles_dict = dict()
    for test_id, test_data in test_cases_dict.items():
        particles = dict()
        for particle_id, particle_data in test_data.items():
            assert (type(particle_id)==int or particle_id.isdigit()) #* Checks that id can be converted to int
            particles[int(particle_id)] = Particle(
                id = int(particle_id),
                mass = particle_data["mass"],
                initial_position = particle_data["position"],
                initial_velocity = particle_data["velocity"]
            )
        assert ((type(test_id) == int) or (test_id.isdigit())) #* Similar `int` checks
        test_case_to_particles_dict[int(test_id)] = particles
    return test_case_to_particles_dict
