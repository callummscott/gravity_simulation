import pytest
from copy import deepcopy
from numpy.linalg import norm

from src.energy import calculate_kinetic_energy_of_particles, calculate_potential_energy_of_particles, calculate_total_energy_of_particles
from src.motion_calcs import simulate_timestep


@pytest.fixture
def assert_energy_conservation_after_n_timesteps(initialised_particles, config):
    def do_assert(n: int, rel: float = 1e-6):
        sim_particles = initialised_particles.copy()
        start_copy = deepcopy(sim_particles)  #* deepcopy required for this test to mean anything at all.

        for _ in range(n):
            simulate_timestep(sim_particles, config)
        total_start_energy = calculate_total_energy_of_particles(start_copy, config)
        total_end_energy = calculate_total_energy_of_particles(sim_particles, config)

        no_collisions = len(sim_particles) == len(start_copy)

        if no_collisions:
            assert total_end_energy == pytest.approx(total_start_energy, rel=rel)
        else:
            assert total_end_energy > total_start_energy # I reckon this could also sometimes go the other way around tbh.
    return do_assert


class TestEnergy:
    def test_timestep_changes_particles(self, initialised_particles, config):
        start_particles = deepcopy(initialised_particles)
        simulate_timestep(initialised_particles, config)
        end_particles = initialised_particles
        # deepcopy is required, otherwise this equality check fails.
        assert end_particles != start_particles

    def test_total_energy_single_particle(self, particle, config):
        kinetic_energy = .5 * particle.mass * norm(particle.velocity)**2
        assert calculate_kinetic_energy_of_particles([particle]) == kinetic_energy
        assert calculate_potential_energy_of_particles([particle], config) == 0        

    def test_potential_energy_is_negative(self, particles, config):
        potential_energy = calculate_potential_energy_of_particles(particles, config)
        assert (potential_energy < 0) or (potential_energy == pytest.approx(0, rel=1e-6))

    def test_energy_conservation_after_1_timestep(self, assert_energy_conservation_after_n_timesteps):
        assert_energy_conservation_after_n_timesteps(1, 1e-5)

    def test_energy_conservation_after_10_timestep(self, assert_energy_conservation_after_n_timesteps):
        assert_energy_conservation_after_n_timesteps(10, 1e-5)

    def test_energy_conservation_after_100_timestep(self, assert_energy_conservation_after_n_timesteps):
        assert_energy_conservation_after_n_timesteps(100, 1e-4)

    def test_energy_conservation_after_1000_timestep(self, assert_energy_conservation_after_n_timesteps):
        assert_energy_conservation_after_n_timesteps(1000, 1e-4)


if __name__ == "__main__":
    ...