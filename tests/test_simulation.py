
import pytest

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


##* GET_DISTANCE_MATRIX *##

@pytest.mark.parametrize(
    "pos_array_1, pos_array_2, expected_distance",
    [
        ([-10,0,0], [10,0,0], 20),
        ([-23,0,0], [15,0,0], 38),
        ([1,1,1], [0,0,0], 3**.5),
        ([10,20,30], [-10,50,20], 37.416573867739416),
        ([0,-1,0], [0,1,0], 2),
        ([0,-10,0], [0,10,0], 20)
    ]
)
def test_get_distance_matrix_two_simple_particles(pos_array_1, pos_array_2, expected_distance):
    particles = { 0: Particle(0,1,pos_array_1,[0]*3), 1: Particle(1,1,pos_array_2,[0]*3)}
    assert get_distance_matrix(particles)[0,1] == pytest.approx(expected_distance)


##* CALCULATE_KINETIC_ENERGY_OF_PARTICLES *##

@pytest.mark.parametrize(
    "mass_1, init_vel_1, mass_2, init_vel_2, expected_energy",
    [
        (1, [0,0,0], 1, [0,0,0], 0),
        (1, [2,2,2], 1, [2,2,2],  12),
        (10, [10,10,10], 1, [1,1,1], 1501.5),
        (1, [-2,4,-8], 16, [-32,64,-128], 172074.0),
    ]
)
def test_calculate_kinetic_energy_of_particles_two_particles(mass_1, init_vel_1, mass_2, init_vel_2, expected_energy):
    particles = { 0: Particle(0, mass_1, [0]*3, init_vel_1), 1: Particle(1, mass_2, [0]*3, init_vel_2) }
    assert calculate_kinetic_energy_of_particles(particles) == pytest.approx(expected_energy)

# Don't really have reason to doubt that kinetic energy calcs work for more particles


##* CALCULATE_POTENTIAL_ENERGY_OF_PARTICLES *##

@pytest.mark.parametrize(
    "mass_1, init_pos_1, mass_2, init_pos_2, expected_energy",
    [
        (10, [-10,-10,-10], 10, [10,10,10], -CONFIG.G*100/34.64101615137754),
        (1, [-10,-10,-10], 100, [10,10,10], -CONFIG.G*100/34.64101615137754),
        (1, [1e3,-10,2], 1, [1e3,10,2], -CONFIG.G/20),
        (123, [-4,1.45,25.2], 43, [3,-17.53,4.32], -CONFIG.G*5289/29.07257814504933),
    ]
)
def test_calculate_potential_energy_of_particles_two_particles(mass_1, init_pos_1, mass_2, init_pos_2, expected_energy):
    particles = { 0: Particle(0, mass_1, init_pos_1, [0]*3), 1: Particle(1, mass_2, init_pos_2, [0]*3) }
    assert calculate_potential_energy_of_particles(particles) == pytest.approx(expected_energy)


@pytest.mark.parametrize(
    "mass_1, init_pos_1, mass_2, init_pos_2, mass_3, init_pos_3, expected_energy",
    [
        (1, [10,0,0], 1, [0,0,0], 1, [-10,0,0], -CONFIG.G/4),
        (1, [10,0,0], 10, [0,0,0], 1, [-10,0,0], -CONFIG.G*2.05),
        (4.2, [12.1,3.23,5], 3.7, [2,3.2,5.4], 11.54, [-3.12,-100.2,45.5], -CONFIG.G*(2.354301877456737))
    ]
)
def test_calculate_potential_energy_of_particles_three_particles(
        mass_1, init_pos_1, mass_2, init_pos_2, mass_3, init_pos_3, expected_energy
    ):
    particles = {
        0: Particle(0, mass_1, init_pos_1, [0]*3),
        1: Particle(1, mass_2, init_pos_2, [0]*3),
        2: Particle(2, mass_3, init_pos_3, [0]*3)
    }
    assert calculate_potential_energy_of_particles(particles) == pytest.approx(expected_energy)


##* CALCULATE_TOTAL_ENERGY_OF_PARTICLES *##

@pytest.mark.parametrize(
    "mass, init_pos, init_vel, total_energy",
    [
        (1, [0,0,0], [0,0,0], 0),
        (1, [0,0,0], [0,0,4], 8),
        (1, [0,0,0], [0,0,2.4], 2.88),
        (10, [0,0,0], [0,0,3], 45)
    ]
)
def test_calculate_energy_of_particles_single_particle(mass, init_pos, init_vel, total_energy):
    particles = { 0: Particle(0, mass, init_pos, init_vel) }
    assert calculate_total_energy_of_particles(particles) == pytest.approx(total_energy)
    assert calculate_total_energy_of_particles(particles) == calculate_kinetic_energy_of_particles(particles)


@pytest.mark.parametrize(
    "mass_1, init_pos_1, init_vel_1, mass_2, init_pos_2, init_vel_2, expected_energy",
    [
        (1, [0,-1,0], [0,0,0], 1, [0,1,0], [0,0,0], -CONFIG.G/2),
        (1, [0,-10,0], [0,0,0], 1, [0,10,0], [0,0,0], -CONFIG.G/20),
        (1, [1e3,-10,0], [0,0,0], 1, [1e3,10,0], [0,0,0], -CONFIG.G/20),
        (1, [1e3,-10,2], [2,2,2], 1, [1e3,10,2], [2,2,2], -CONFIG.G/20 + 12),
        (100, [20,-6.5,13], [1,5,-10], .5, [27,-43,72], [15,-9,0], -CONFIG.G*50/69.72983579501675 + 6376.5),
    ]
)
def test_calculate_energy_of_particles_two_particles( mass_1, init_pos_1, init_vel_1, mass_2, init_pos_2, init_vel_2, expected_energy ):
    particles = {
        0: Particle(0, mass_1, init_pos_1, init_vel_1),
        1: Particle(1, mass_2, init_pos_2, init_vel_2)
    }
    total_energy = calculate_total_energy_of_particles(particles)
    kinetic_energy = calculate_kinetic_energy_of_particles(particles)
    potential_energy = calculate_potential_energy_of_particles(particles)
    
    assert total_energy == pytest.approx(expected_energy)
    assert total_energy == pytest.approx(kinetic_energy + potential_energy)


##* 

##* GET_NEXT_PARTICLE_STATES *##

@pytest.mark.parametrize(
    "timesteps, mass_1, pos_1, vel_1, mass_2, pos_2, vel_2, energy",
    [
        #* These are the same examples as listed above, + timesteps
        (1,  1, [0,-1,0], [0,0,0], 1, [0,1,0], [0,0,0], -CONFIG.G/2),
        (10, 1, [0,-1,0], [0,0,0], 1, [0,1,0], [0,0,0], -CONFIG.G/2),
        (2,  1, [0,-10,0], [0,0,0], 1, [0,10,0], [0,0,0], -CONFIG.G/20),
        (50, 1, [0,-10,0], [0,0,0], 1, [0,10,0], [0,0,0], -CONFIG.G/20),
        (4,   1, [1e3,-10,0], [0,0,0], 1, [1e3,10,0], [0,0,0], -CONFIG.G/20),
        (100, 1, [1e3,-10,0], [0,0,0], 1, [1e3,10,0], [0,0,0], -CONFIG.G/20),
        (0,  1, [1e3,-10,2], [2,2,2], 1, [1e3,10,2], [2,2,2], -CONFIG.G/20 + 12),
        (1,  1, [1e3,-10,2], [2,2,2], 1, [1e3,10,2], [2,2,2], -CONFIG.G/20 + 12), #! Breaking why???
        # (75, 1, [1e3,-10,2], [2,2,2], 1, [1e3,10,2], [2,2,2], -CONFIG.G/20 + 12),
        # (10,  100, [20,-6.5,13], [1,5,-10], .5, [27,-43,72], [15,-9,0], -CONFIG.G*50/69.72983579501675 + 6376.5),
        # (250, 100, [20,-6.5,13], [1,5,-10], .5, [27,-43,72], [15,-9,0], -CONFIG.G*50/69.72983579501675 + 6376.5),
    ]
)
def test_get_next_particle_states_two_particles(timesteps, mass_1, pos_1, vel_1, mass_2, pos_2, vel_2, energy):
    """ Checking energy and momentum before and after timesteps """
    particles = {
        0: Particle(0, mass_1, pos_1, vel_1),
        1: Particle(1, mass_2, pos_2, vel_2)
    }
    def get_total_momentum(particles):
        return sum([ particle.momentum() for particle in particles.values() ])
            
    total_momentum_before = get_total_momentum(particles)
    for _ in range(timesteps):
        particles = get_next_particle_states(particles)
    total_momentum_after = get_total_momentum(particles)

    #! Got to be careful/strict with the absolute and relative error values here; what's their reasoning?
    assert calculate_total_energy_of_particles(particles) == pytest.approx(energy, abs=1e-4)
    assert total_momentum_before == pytest.approx(total_momentum_after, abs=1e-4)

    

    # for particle_dicts in example_particle_dicts:
    #     total_momentum = utils_calculate_total_momentum(particle_dicts)
    #     example_particles_updated = get_next_particle_states(particle_dicts)
    #     total_momentum_updated = utils_calculate_total_momentum(example_particles_updated)

    # assert norm(total_momentum) == pytest.approx(norm(total_momentum_updated))

    # energy_log = dict()
    # for i in range(CONFIG.number_of_steps):
    #     get_next_particle_states(particles)
    #     if i % 100 == 0:
    #         energy_log[i] = utils_calculate_energy_of_particles(particles)    
    
    # energy_seq = [ i for i in energy_log.values() ]
    # energy_diff = [ energy_seq[i+1] - value for i, value in enumerate(energy_seq[:-1]) ]
    
    # for i in range(len(energy_diff) - 1):
    #     assert energy_diff[i+1] == pytest.approx(energy_diff[i]) 
