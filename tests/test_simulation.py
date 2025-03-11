
from numpy.linalg import norm
from pytest import approx, raises

from tests.utils import *
from tests.config import TestConfig
from src.simulation import initialise_random_particles, get_distance_matrix, get_next_particle_states, calculate_energy_of_particles

CONFIG = TestConfig()

def test_initialise_random_particles():

    for _ in range(20): # This I think runs through the same 20 tests each time it's run -- I hope
        particles = utils_get_test_particles() #* Utils # Generating the same thing like every time due to the seed
 
        for particle in particles.values():

            particle_distance = norm(particle.position)
            particle_speed    = norm(particle.velocity)

            assert (0 < particle.mass <= CONFIG.max_mass) # no approx necessary
            assert (0 <= particle_distance <= CONFIG.max_distance) or (particle_distance == approx(0)) or (particle_distance == approx(CONFIG.max_distance))
            assert (0 <= particle_speed <= CONFIG.max_speed) or (particle_speed == approx(0)) or (particle_speed == approx(CONFIG.max_speed))

    with raises(TypeError):
        initialise_random_particles(n="8", max_mass=utils_random_mass(), max_distance=utils_random_distance(), max_speed=utils_random_speed())
        initialise_random_particles(n=10.99, max_mass=utils_random_mass(), max_distance=utils_random_distance(), max_speed=utils_random_speed())

    with raises(ValueError):
        initialise_random_particles(n=-3, max_mass=utils_random_mass(), max_distance=utils_random_distance(), max_speed=utils_random_speed())
        initialise_random_particles(n=17, max_mass=utils_random_mass(), max_distance=utils_random_distance(), max_speed=utils_random_speed())
        initialise_random_particles(n=0, max_mass=utils_random_mass(), max_distance=utils_random_distance(), max_speed=utils_random_speed())


def test_get_distance_matrix():

        example_ns = [ 1, 3, 4, 6, 7, 10, 12, 13, 15 ]
        particles_dict_examples = [ utils_get_test_particles(n) for n in example_ns ]
        for particles_dict in particles_dict_examples:

            distance_matrix = get_distance_matrix(particles_dict)
            n = len(particles_dict)
            assert distance_matrix.shape == (n, n), "Wrong shape" # Check size is accurate
            for i in range(n):
                for j in range(i, n):
                    # Check the matrix is symmetric
                    assert distance_matrix[i, j] == distance_matrix[j, i], "Values are not symmetric"
                    if i == j:
                        assert distance_matrix[i, i] == 0


def test_get_force_on_particle():
    ...
    #TODO: Might as well just be testing the step_and_log function

def test_get_impulse_on_particle():
    ...
    # TODO: ...

def test_calculate_energy_of_particles():

    particle_dict = utils_get_test_particles(n=1) #* Utils
    particle = particle_dict[0]
    expected_energy = .5*particle.mass*norm(particle.velocity)**2
    assert calculate_energy_of_particles(particle_dict) == approx(expected_energy), "Single particle energy not accurate."
    
    particles = utils_get_test_particles()
    start_energy = calculate_energy_of_particles(particles)
    #* Essentially we're scaling velocities of individual particles and seeing if the total energy changes by how much you'd expect it to change.
    for particle in particles.values():
        for k in [1.1, 1.2, 1.3]:
            particle.velocity *= k
            added_energy = (k**2 - 1)*.5*particle.mass*norm(particle.velocity)**2
            end_energy = calculate_energy_of_particles(particles)
            particle.velocity /= k
            assert end_energy - start_energy == approx(added_energy), "The energy is way off"


def test_get_next_particle_states():

    example_particle_dicts = [ utils_get_test_particles() for _ in range(10) ]

    for particle_dicts in example_particle_dicts:
        total_momentum = utils_calculate_total_momentum(particle_dicts)
        example_particles_updated = get_next_particle_states(particle_dicts)
        total_momentum_updated = utils_calculate_total_momentum(example_particles_updated)

    assert norm(total_momentum) == approx(norm(total_momentum_updated))

    # energy_log = dict()
    # for i in range(CONFIG.number_of_steps):
    #     get_next_particle_states(particles)
    #     if i % 100 == 0:
    #         energy_log[i] = utils_calculate_energy_of_particles(particles)    
    
    # energy_seq = [ i for i in energy_log.values() ]
    # energy_diff = [ energy_seq[i+1] - value for i, value in enumerate(energy_seq[:-1]) ]
    
    # for i in range(len(energy_diff) - 1):
    #     assert energy_diff[i+1] == approx(energy_diff[i]) 


if __name__ == "__main__":
    test_get_distance_matrix()
    test_get_force_on_particle()
    test_get_impulse_on_particle()
    test_initialise_random_particles()
    test_get_next_particle_states()