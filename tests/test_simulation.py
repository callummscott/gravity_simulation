
import pytest
from numpy.linalg import norm

from tests.config import TestConfig
from src.classes.particle import Particle

from src.simulation import *


CONFIG = TestConfig()

# @pytest.mark.parametrize(
#     "mass_1, init_pos_1, init_vel_1, mass_2, init_pos_2, init_vel_2"
# )
# def test_get_distance_matrix_():

    # test_cases = utils_get_test_case_to_particles_dict()
    # for particles in test_cases.values():
    #     distance_matrix = get_distance_matrix(particles)
    #     n = len(particles)
    #     assert distance_matrix.shape == (n, n), "Wrong shape" # Check size is accurate
    #     for i in range(n):
    #         for j in range(i, n):
    #             # Check the matrix is symmetric
    #             assert distance_matrix[i, j] == distance_matrix[j, i], "Values are not symmetric"
    #             if i == j:
    #                 assert distance_matrix[i, i] == 0


@pytest.mark.parametrize(
    "pos_array_1, pos_array_2, expected_distance",
    [
        ([-10,0,0], [10,0,0], 20),
        ([-23,0,0], [15,0,0], 38),
        ([1,1,1], [0,0,0], 3**.5),
        ([10,20,30], [-10,50,20], 37.416573867739416),
    ]
)
def test_get_distance_matrix_two_simple_particles(pos_array_1, pos_array_2, expected_distance):
    particles = { 0: Particle(0,1,pos_array_1,[0]*3), 1: Particle(1,1,pos_array_2,[0]*3)}
    assert get_distance_matrix(particles)[0,1] == pytest.approx(expected_distance)


def test_get_force_on_particle():
    ...
    #TODO: Might as well just be testing the step_and_log function

def test_get_impulse_on_particle():
    ...
    # TODO: ...
        

@pytest.mark.parametrize(
    "mass, init_pos, init_vel, expected_energy",
    [
        (1, [0,0,0], [0,0,0], 0),
        (1, [0,0,0], [0,0,4], 8),
        (1, [0,0,0], [0,0,2.4], 2.88),
        (10, [0,0,0], [0,0,3], 45)
    ]
)
def test_calculate_energy_of_particles_single_particle(mass, init_pos, init_vel, expected_energy):
    
    particles = {0: Particle(0, mass, init_pos, init_vel)}
    assert calculate_energy_of_particles(particles) == pytest.approx(expected_energy)


@pytest.mark.parametrize(
    "mass_1, init_pos_1, init_vel_1, mass_2, init_pos_2, init_vel_2, expected_energy",
    [
        (1, [0,-1,0], [0,0,0], 1, [0,1,0], [0,0,0], -CONFIG.G/2),
        (1, [0,-10,0], [0,0,0], 1, [0,10,0], [0,0,0], -CONFIG.G/20)
    ]
)
def test_calculate_energy_of_particles_two_particles(
        mass_1, init_pos_1,init_vel_1, mass_2, init_pos_2, init_vel_2, expected_energy
    ):
    particles = {
        0: Particle(0, mass_1, init_pos_1, init_vel_1),
        1: Particle(1, mass_2, init_pos_2, init_vel_2)
    }
    assert calculate_energy_of_particles(particles) == pytest.approx(expected_energy)


    #* Checks that if we manually scale a single particle's velocity that the total energy changes how you'd expect
    # for particles in test_cases.values():
    #     start_energy = calculate_energy_of_particles(particles)
    #     for particle in particles.values():
    #         for k in [1.1, 1.2, 1.3]:
    #             particle.velocity *= k
    #             added_energy = (k**2 - 1)*.5*particle.mass*norm(particle.velocity)**2
    #             end_energy = calculate_energy_of_particles(particles)
    #             particle.velocity /= k
    #             assert end_energy - start_energy == pytest.approx(added_energy), "The energy is way off"
    



def test_get_next_particle_states():
    return #! Holding off on this for now.
    example_particle_dicts = [ utils_get_test_particles() for _ in range(10) ]

    for particle_dicts in example_particle_dicts:
        total_momentum = utils_calculate_total_momentum(particle_dicts)
        example_particles_updated = get_next_particle_states(particle_dicts)
        total_momentum_updated = utils_calculate_total_momentum(example_particles_updated)

    assert norm(total_momentum) == pytest.approx(norm(total_momentum_updated))

    # energy_log = dict()
    # for i in range(CONFIG.number_of_steps):
    #     get_next_particle_states(particles)
    #     if i % 100 == 0:
    #         energy_log[i] = utils_calculate_energy_of_particles(particles)    
    
    # energy_seq = [ i for i in energy_log.values() ]
    # energy_diff = [ energy_seq[i+1] - value for i, value in enumerate(energy_seq[:-1]) ]
    
    # for i in range(len(energy_diff) - 1):
    #     assert energy_diff[i+1] == pytest.approx(energy_diff[i]) 


if __name__ == "__main__":
    test_calculate_energy_of_particles_single_particle()
    test_calculate_energy_of_particles_two_particles()

    test_get_distance_matrix_two_simple_particles()
    test_get_force_on_particle()
    test_get_impulse_on_particle()
    test_get_next_particle_states()