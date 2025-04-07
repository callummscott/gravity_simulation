import pytest
from numpy.linalg import norm
from src.particle_setup import get_initial_random_particle_attributes


@pytest.fixture(params=[1, 4542243, 54254543452, 8127743453232155])
def seed(request):
    return request.param

class TestInitialParticleAttributes:
    @pytest.mark.parametrize("config", [{"max_mass": 1}, {"max_mass": 522_342_223}, {"max_mass": 1e15}], indirect=True)
    def test_mass_attribute_in_bounds(self, seed, config):
        mass = get_initial_random_particle_attributes(seed, config)[0]
        assert (0 < mass) and (mass <= config.max_mass)

    @pytest.mark.parametrize("config", [{"max_distance": 1.64}, {"max_distance": 131_123_654}, {"max_distance": 1e17}], indirect=True)
    def test_position_attribute_in_bounds(self, seed, config):
        position = get_initial_random_particle_attributes(seed, config)[1]
        distance = norm(position)
        assert (0 <= distance) and (distance <= config.max_distance)
    
    @pytest.mark.parametrize("config", [{"max_speed": 1.213}, {"max_speed": 31_321_714}, {"max_speed": 1e14}], indirect=True)
    def test_velocity_attribute_in_bounds(self, seed, config):
        velocity = get_initial_random_particle_attributes(seed, config)[2]
        speed = norm(velocity)
        assert (0 <= speed) and (speed <= config.max_speed)
