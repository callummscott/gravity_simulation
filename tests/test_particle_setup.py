
from pytest import raises, approx
from random import random, randrange, choice

from src.particle_setup import get_masses, get_positions, get_velocities, get_position, vector_length


def test_get_masses():
    """ Tests: 1) that mass list is of expected length, 2) that maximum"""

    N_cases = [ i for i in range(1,16+1) ]
    mass_cases = [ random()*100_000 for _ in range(50) ]

    test_cases = [ {"N":choice(N_cases), "max_mass":choice(mass_cases) } for _ in range(50) ]

    for case in test_cases:
        n = case['N']
        max_mass = case['max_mass']

        assert len(get_masses(n,  max_mass)) == case['N']
        for mass in get_masses(n, max_mass):
            assert 0 < mass <= max_mass # No approx necessary; also must exclude 0

    with raises(ValueError):
        get_masses(N=16,  max_mass=-15)
        get_masses(N=-56, max_mass=100_000)
        get_masses(N=0,   max_mass=10)
        get_masses(N=16,  max_mass=0)

    with raises(TypeError):
        get_masses(N=37.2,   max_mass=2)
        get_masses(N="12.4", max_mass=2)
        get_masses(N=4,      max_mass=["test"])


def test_get_position():
    """ Tests: 1) Length of each position vector is below defined maximum """

    max_distance_cases = [ randrange(0, 10_000, 4) + random() for _ in range(50)]

    for max_distance in max_distance_cases:
        distance = vector_length(get_position(max_distance))
        assert (0 <= distance <= max_distance) or (distance == approx(0)) or (distance == approx(max_distance))

    with raises(ValueError):
        get_position(max_distance=-10)
        get_position(max_distance=-5435.34)

    with raises(TypeError):
        get_position(max_distance="100")
        get_position(max_distance=[10,20,30])
        get_position(max_distance=("hello", "there"))


def test_get_positions():
    """ Tests: 1) Length of positions array is accurate, 2) Positions are all within distance """
    
    N_cases = [ i for i in range(1,16+1) ]
    max_distance_cases = [ random()*100_000 for _ in range(50) ]

    test_cases = [ {"N":choice(N_cases), "max_distance":choice(max_distance_cases) } for _ in range(50) ]

    for case in test_cases:
        n = case['N']
        max_distance = case['max_distance']

        assert len(get_positions(n, max_distance)) == n
        for position in get_positions(n, max_distance):
            distance = vector_length(position)
            assert (0 <= distance <= max_distance) or (distance == approx(0)) or (distance == approx(max_distance))
    
    with raises(ValueError):
        get_positions(N=17, max_distance=1234.567)
        get_positions(N=0,  max_distance=1234.567)
        get_positions(N=12, max_distance=-43.4)

    with raises(TypeError):
        get_positions(N=[1,2], max_distance=1234.567)
        get_positions(N=3,     max_distance="1234.567")
        get_positions(N=3.14159, max_distance=64)


def test_get_velocities():

    N_cases = [ i for i in range(16) ]
    max_speed_cases = [ random()*10_000 for _ in range(50) ]
    test_cases = [ {'N': choice(N_cases), 'max_speed': choice(max_speed_cases)} ]

    for case in test_cases:

        n = case['N']
        max_speed=  case['max_speed']
        velocities = get_velocities(n, max_speed)

        assert len(velocities) == n
        for velocity in velocities:
            speed = vector_length(velocity)
            assert (0 <= speed <= max_speed) or (speed == approx(0)) or (speed == approx(max_speed))
    
    with raises(ValueError):
        get_velocities(N=100, max_speed=10_000)
        get_velocities(N=12, max_speed=-100)
        get_velocities(N=17, max_speed=100)
        get_velocities(N=0, max_speed=123.456)
        get_velocities(N=-13, max_speed=21)
        get_velocities(N=-19, max_speed=27)
        get_velocities(N=6, max_speed=-10)

    with raises(TypeError):
        get_velocities(N="2", max_speed=643)
        get_velocities(N=4.56678, max_speed=64.234)
        get_velocities(N=1, max_speed=[1,2,3])


if __name__ == "__main__":
    test_get_masses()
    test_get_position()
    test_get_positions()
    test_get_velocities()