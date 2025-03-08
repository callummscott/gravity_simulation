
from numpy.linalg import norm
from pytest import approx, raises
from random import randint

from gravity_simulation.config import Config
from tests.utils import TestConfig, get_test_particles, random_mass, random_distance, random_speed
from gravity_simulation.simulation import initialise_random_particles, get_distance_matrix, step_and_log_particle_motion

CONFIG = Config()

def test_initialise_random_particles():
    for _ in range(50):

        particles = get_test_particles() #* Utils

        for particle in particles.values():

            particle_distance = norm(particle.position)
            particle_speed    = norm(particle.velocity)

            assert (0 < particle.mass <= TestConfig.max_mass) # no approx necessary
            assert (0 <= particle_distance <= TestConfig.max_distance) or (particle_distance == approx(0)) or (particle_distance == approx(TestConfig.max_distance))
            assert (0 <= particle_speed <= TestConfig.max_speed) or (particle_speed == approx(0)) or (particle_speed == approx(TestConfig.max_speed))

    with raises(TypeError):
        assert initialise_random_particles(n="8",   max_mass=random_mass(), max_distance=random_distance(), max_speed=random_speed())
        assert initialise_random_particles(n=10.99, max_mass=random_mass(), max_distance=random_distance(), max_speed=random_speed())

    with raises(ValueError):
        assert initialise_random_particles(n=-3, max_mass=random_mass(), max_distance=random_distance(), max_speed=random_speed())
        assert initialise_random_particles(n=17, max_mass=random_mass(), max_distance=random_distance(), max_speed=random_speed())
        assert initialise_random_particles(n=0,  max_mass=random_mass(), max_distance=random_distance(), max_speed=random_speed())


def test_get_distance_matrix():

    for _ in range(40):
        n = randint(1, 16)

        test_particles = get_test_particles(n=n)

        distance_matrix = get_distance_matrix(test_particles)
        assert distance_matrix.shape == (n, n) # Check size is accurate
        for i in range(n):
            for j in range(i, n):
                # Check the matrix is symmetric
                assert distance_matrix[i, j] == distance_matrix[j, i]


def test_get_force_on_particle():
    ...
    #TODO: Might as well just be testing the step_and_log function

def test_get_impulse_on_particle():
    ...
    # TODO: ...

def test_step_and_log_particle_motion():
    # Going to mainly test energy conservation on this part
    particles = get_test_particles() #* Utils

    def calculate_energy_of_particles(particles: dict):
        total_energy = 0
        for id in particles:
            particle = particles[id]
            particle_mass = particle.mass
            particle_velocity = particle.velocity
            distances = get_distance_matrix(particles)

            kinetic_energy = .5*particle_mass*norm(particle_velocity)**2
            potential_energy = 0
            for other_id in particles:
                if other_id != id:
                    other_particle = particles[other_id]
                    potential_energy += CONFIG.G*particle.mass*other_particle.mass / distances[id, other_id]
            
            total_energy += kinetic_energy + potential_energy
        return total_energy
    
    energy_log = dict()
    for i in range(TestConfig.number_of_steps):
        step_and_log_particle_motion(particles)
        if i % 100 == 0:
            energy_log[i] = calculate_energy_of_particles(particles)    
    
    energy_seq = [ i for i in energy_log.values() ]
    energy_diff = [ energy_seq[i+1] - value for i, value in enumerate(energy_seq[:-1]) ]
    
    for i in range(len(energy_diff) - 1):
        assert energy_diff[i+1] == approx(energy_diff[i]) 