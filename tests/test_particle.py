import pytest
from numpy import array, array_equal

from src.classes.particle import Particle

class TestParticle:
    @pytest.mark.parametrize("id, mass, pos, vel", [(10, 123, [1,-2,3], [-0.1,0.2,-0.3])])
    def test_values_get_initialised(self, id, mass, pos, vel):
        particle = Particle(id, mass, pos, vel)
        assert particle.id == id
        assert particle.mass == mass
        assert array_equal(particle.position, array(pos))
        assert array_equal(particle.velocity, array(vel))
        assert array_equal(particle.momentum(), particle.mass*particle.velocity)
        assert particle.acceleration == None

    @pytest.mark.parametrize("mass, pos, vel", [(1, [1,1,1],[2,2,2])])
    def test_id_not_an_integer(self, mass, pos, vel):
        with pytest.raises(TypeError):
            Particle("2", mass, pos, vel)
            Particle(1.1, mass, pos, vel)
            Particle(1/12, mass, pos, vel)

    @pytest.mark.parametrize("id, pos, vel", [(10, [-100,100,-50], [-1,-1,-5])])
    def test_mass_not_a_float(self, id, pos, vel):
        with pytest.raises(TypeError):
            Particle(id, [1,2], pos, vel)
            Particle(id, sum, pos, vel)
            Particle(id, "mass", pos, vel)
        
    @pytest.mark.parametrize("id, mass, vel", [(12, 100, [-1.2, 3.2, -2.6])])
    def test_position_not_valid_array_type(self, id, mass, vel):
        with pytest.raises(TypeError):
            Particle(id, mass, [-10,-10,-10,-10], vel)
            Particle(id, mass, [2,4], vel)
            Particle(id, mass, array([1,2,3,4]), vel)
        
    @pytest.mark.parametrize("id, mass, pos", [(12, 100, [-1.2, 3.2, -2.6])])
    def test_velocity_not_valid_array_type(self, id, mass, pos):
        with pytest.raises(TypeError):
            Particle(id, mass, pos, [-10,-10,-10,-10])
            Particle(id, mass, pos, [2,4])
            Particle(id, mass, pos, array([1,2,3,4]))
