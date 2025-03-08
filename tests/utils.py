from random import random, randint
from gravity_simulation.particle_setup import get_random_input_variables 
from gravity_simulation.simulation import initialise_random_particles

class TestConfig:
    max_mass = 10_000
    max_distance = 100_000
    max_speed = 100_000
    number_of_steps = 1_000

def random_mass():
    result = random()*TestConfig.max_mass
    if result == 0:
        return random_mass()
    else:
        return result

def random_distance():
    return random()*TestConfig.max_distance

def random_speed():
    return random()*TestConfig.max_speed

def get_test_particles(n=None, max_mass=None, max_distance=None, max_speed=None):

    #* Potential errors here will be handled by the initialise_random_particles function
    if n==None:
        final_n = randint(1, 16)
    else:
        final_n = n
    
    if max_mass == None:
        final_mass = random()*TestConfig.max_mass
    else:
        final_mass = max_mass

    if max_distance == None:
        final_distance = random()*TestConfig.max_distance
    else:
        final_mass = max_mass
        
    if max_speed == None:
        final_speed = random()*TestConfig.max_speed
    else:
        final_speed = max_speed

    particles = initialise_random_particles(final_n, final_mass, final_distance, final_speed)

    return particles