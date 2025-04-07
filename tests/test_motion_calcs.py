import pytest
from copy import deepcopy
from numpy.linalg import norm 

from src.classes.particle import Particle
from src.particle_setup import get_configured_particles
from src.motion_calcs import initialise_particles, simulate_timestep


@pytest.fixture
def assert_simple_collision(config):
    def do_assert(particle_distance: float, collision_distance: float, collision_expected: bool) -> None:
        """ Tests that what would be expected of collisions is accurate given `collision_distance` and `particle_distance`. """
        config.collision_distance = collision_distance
        particle_0 = Particle(0, 1, [0,0,0], [0,0,0])
        particle_1 = Particle(1, 1, [particle_distance, 0, 0], [0,0,0])
        particles = [particle_0, particle_1]
        initialise_particles(particles, config)
        if collision_expected:
            assert len(particles) < 2
            assert particle_distance <= collision_distance
        else:
            assert len(particles) == 2
            assert particle_distance > collision_distance
    return do_assert


@pytest.fixture
def assert_linear_approximation(config):
    def do_assert(G: float, dt: float, expected_distance: float):
        config.G, config.half_dtsq = G, 0.5*dt**2
        particle_0 = Particle(0, 1, [0,0,1e5], [0,0,0])
        particle_1 = Particle(1, 1e10, [0,0,0], [0,0,0])
        particles = [particle_0, particle_1]

        initialise_particles(particles, config)
        start_position = particle_0.position
        simulate_timestep(particles, config)
        assert norm(particle_0.position - start_position) == pytest.approx(expected_distance)
    return do_assert



class TestInitialiseParticles:
    def test_acceleration_is_defined(self, particles, config):
        for particle in particles:
            assert particle.acceleration == None
        initialise_particles(particles, config)
        for particle in particles:
            try:
                accel = list(particle.acceleration)
                assert accel != None
            except TypeError:
                assert False, "Acceleration isn't defined."
        del particles


    @pytest.mark.parametrize("config", [
        {"collision_distance": 100, "max_distance": 50},
        {"collision_distance": 10, "max_distance": 20, "number_of_particles": 100}
    ], indirect=True)
    def test_collision_handling(self, config):
        particles = get_configured_particles(config)
        start_length = len(particles)

        initialise_particles(particles, config)
        assert len(particles) < start_length
        del particles
    

    def test_collision_filtering_in_simple_collision_case(self, assert_simple_collision):
        """ (particle_distance, collision_distance, collision_expected) """
        assert_simple_collision(1, 1, True)
        assert_simple_collision(2, 5, True)
        assert_simple_collision(5, 2, False)
        assert_simple_collision(5, 5.0001, True)
        assert_simple_collision(10, 5, False)
        assert_simple_collision(1e10, 1e10+1, True)



class TestSimulateTimestep:
    def test_that_particles_change(self, initialised_particles, config):
        start_particles = deepcopy(initialised_particles)
        
        simulate_timestep(initialised_particles, config)
        assert start_particles != initialised_particles
        del start_particles, initialised_particles


    def test_momentum_conservation(self, initialised_particles, config):
        momentum = lambda ptcls: sum([ptcl.mass*ptcl.velocity for ptcl in ptcls])

        initial_momentum = list(momentum(initialised_particles))
        simulate_timestep(initialised_particles, config)
        final_momentum = list(momentum(initialised_particles))

        assert final_momentum == pytest.approx(initial_momentum)


    def test_linear_approximation_for_large_distances(self, assert_linear_approximation):
        """
        (G, dt, distance_covered)
        Masses and distances cancel, so accel should be -G m/s^2, therefore distance should be 0.5*G*dt^2
        """
        assert_linear_approximation(10, 0.1, .5*10*.1**2)
        assert_linear_approximation(10, 0.01, .5*10*.01**2)
        assert_linear_approximation(250, 1e-3, .5*250*1e-6)

    def test_energy_conservation(self):
        pass



class TestCollisionPairsFinder:
    def test_qualifying_distances_are_identified(self, particles, config):

        ...

    def test_each_list_element_is_two_item_set(self):
        ...

    def test_each_pair_is_unique(self):
        ...



class TestCollidedIdGrouper:
    pass


class TestCollisionHandler:
    pass


class TestGetDisplacementAndDistancesFromOrderedPairs:
    pass
