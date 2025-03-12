import pytest
from numpy import array, array_equal

from src.classes.particle import Particle


@pytest.mark.parametrize(
    "id, mass, pos, vel",
    [
        (4, 10, [0,0,0], [0,0,0]),
        (6, 256, [2,4,8], array([10,-22,-100])),
        (14, 6234.232, array([1,-1,-1]), array([222,22,2])),
    ]
)
def test_particle(id, mass, pos, vel):
    particle = Particle(id, mass, pos, vel)
    assert particle.id == id
    assert particle.mass == mass
    assert array_equal(particle.position, array(pos))
    assert array_equal(particle.velocity, array(vel))
    assert particle.next_position == None
    assert particle.next_velocity == None
    assert array_equal(particle.momentum(), particle.mass*particle.velocity) 


@pytest.mark.parametrize(
    "id, mass, pos, vel",
    [
        # -- id not an integer --
        ("2", 1, [1,1,1],[2,2,2]),
        (1.1, 10, [1,1,1],[2,2,2]),
        (1/12, 10, [1,1,1],[2,2,2]),
        # -- mass not an integer --
        (5, [1,2], [0,0,0], [0,0,0]),
        (10, "mass", [0,0,0], [0,0,0]),
        # -- position is not a valid array-type --
        (2, 102.348, [-10,-10,-10,-10], [0,0,0]),
        (14, 1028.256, [2,4], [0,0,0]),
        (14, 1028.256, array([1,2,3,4]), [0,0,0])
    ]
)
def test_particle__init__type_error(id, mass, pos, vel):
    with pytest.raises(TypeError):
        Particle(id, mass, pos, vel)


@pytest.mark.parametrize(
    "id, mass, pos, vel",
    [
        (-1, 10, [.5,.2,-.1], [-1.42e3,504,12]),
        (17, 10, [101,-110,11], [-4,8,-16]),
        (6, 0, [0,0,0], [0,0,0]),
        (4, 23e3, [1e440,1,1], [20,20,20]),
        (2, 10, [-10,20,10], [10,float('inf'),10])
    ]
)
def test_particle__init__value_error(id, mass, pos, vel):
    with pytest.raises(ValueError):
        Particle(id, mass, pos, vel)


if __name__ == "__main__":
    test_particle()
    test_particle__init__type_error()
    test_particle__init__value_error()