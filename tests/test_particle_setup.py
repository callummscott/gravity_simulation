
import pytest
from numpy.linalg import norm
from random import random, choice

from src.particle_setup import *


## GET_MASS ##

@pytest.mark.parametrize(
    "max_mass", [1, .0001, 123.567, 23.4531e7, 123_653_232]
)
def test_get_mass(max_mass):
    mass = get_mass(max_mass)
    assert (0 < mass < max_mass) or (mass == pytest.approx(max_mass))
    assert isinstance(mass, float)


@pytest.mark.parametrize(
    "max_mass", [0, -100, -23.45, float('inf'), float('-inf')]
)
def test_get_mass_value_error(max_mass):
    with pytest.raises(ValueError):
        get_mass(max_mass)


@pytest.mark.parametrize(
    "max_mass", ["number", [1], ("a", {1:2})]
)
def test_get_mass_type_error(max_mass):
    with pytest.raises(TypeError):
        get_mass(max_mass)

## GET_POSITION ##

@pytest.mark.parametrize(
    "max_distance", [1, 24.86, 100_001, 23.23e12]
)
def test_get_position(max_distance):
    position = get_position(max_distance)
    distance = norm(position)
    assert (0 < distance < max_distance) or (distance == pytest.approx(0)) or (distance == pytest.approx(max_distance))


@pytest.mark.parametrize(
    "max_distance", [0, -10, -5435.34, float('inf')]
)
def test_get_position_value_error(max_distance):
    with pytest.raises(ValueError):
        get_position(max_distance)


@pytest.mark.parametrize(
    "max_distance", ["100", [10,20,30], ("hey", "there")]
)
def test_get_position_type_error(max_distance):
    with pytest.raises(TypeError):
        get_position(max_distance)


## GET_VELOCITY ##

@pytest.mark.parametrize(
    "max_speed", [0, 11, 2465.36, 23.3433e5, 23.23e12, 87534/7]
)
def test_get_velocity(max_speed):
    velocity = get_velocity(max_speed)
    speed = norm(velocity)
    assert (0 < speed < max_speed) or (speed == pytest.approx(0)) or (speed == pytest.approx(max_speed))


@pytest.mark.parametrize(
    "max_speed", [-1, -10, -5435.34, float('inf')]
)
def test_get_velocity_value_error(max_speed):
    with pytest.raises(ValueError):
        get_velocity(max_speed)


@pytest.mark.parametrize(
    "max_speed", ["100", [10,20,30], ("stop", "running!")]
)
def test_get_velocity_type_error(max_speed):
    with pytest.raises(TypeError):
        get_velocity(max_speed)


## GET_MASSES ##

@pytest.mark.parametrize(
    "n, max_mass",
    [
        (1, 10),
        (10, 1000),
        (12, 154.43),
        (10, 123.32e5),
        (16, 123_323_76)
    ]
)
def test_get_masses(n, max_mass):
    """ Tests: 1) that mass list is of expected length, 2) that maximum"""
    assert len(get_masses(n,  max_mass)) == n


@pytest.mark.parametrize(
    "n, max_mass",
    [
        (-56, 100),
        (0, 100),
        (20, 100),
        (100, 100)
    ]
)
def test_get_masses_value_error(n, max_mass):
    with pytest.raises(ValueError):
        get_masses(n, max_mass)


@pytest.mark.parametrize(
    "n, max_mass",
    [
        (37.2, 100),
        ("12.4", 100),
        (201.4, 100),
        ([123], 100),
    ]
)
def test_get_masses_type_error(n, max_mass):
    with pytest.raises(TypeError):
        get_masses(n, max_mass)

## GET_POSITIONS ##

@pytest.mark.parametrize(
    "n, max_distance",
    [
        (1, 100),
        (10, 40.43),
        (3, 100_123_543),
        (12, 34.34e14)
    ]
)
def test_get_positions(n, max_distance):
    assert len(get_positions(n, max_distance)) == n
    for position in get_positions(n, max_distance):
        distance = norm(position)
        assert (0 < distance < max_distance) or (distance == pytest.approx(0)) or (distance == pytest.approx(max_distance))


@pytest.mark.parametrize(
    "n, max_distance", [(17, 1234.567), (0, 256.256e8), (-30, 43.4)]
)
def test_get_positions_value_error(n, max_distance):
    with pytest.raises(ValueError):
        get_positions(n, max_distance)


@pytest.mark.parametrize(
    "n, max_distance", [([1,2], 1234.567), (3.14159, 64), (float('inf'), 100_000)]
)
def test_get_positions_type_error(n, max_distance):
    with pytest.raises(TypeError):
        get_positions(n, max_distance)


## GET_VELOCITIES ##

@pytest.mark.parametrize(
    "n, max_speed",
    [
        (1, 100),
        (10, 100_000),
        (12, 234.45),
        (4, 0),
        (7, 103_312_557.23),
        (3, 4.6754e23),
        (16, 2.222)
    ]
)
def test_get_velocities(n, max_speed):
    velocities = get_velocities(n, max_speed)
    assert len(velocities) == n
    for velocity in velocities:
        speed = norm(velocity)
        assert (0 < speed < max_speed) or (speed == pytest.approx(0)) or (speed == pytest.approx(max_speed))

@pytest.mark.parametrize(
    "n, max_speed", [(100, 1e4), (17, 1_200.6544), (0, 754444.4), (-13, 55), (-1_900, 342e62)]
)
def test_get_velocities_value_error(n, max_speed):
    with pytest.raises(ValueError):
        get_velocities(n, max_speed)


@pytest.mark.parametrize(
    "n, max_speed", [("2", 543), (4.568876, 867.65)]
)
def test_get_velocities_type_error(n, max_speed):
    with pytest.raises(TypeError):
        get_velocities(n, max_speed)


@pytest.mark.parametrize(
    "n, max_mass, max_distance, max_speed",
    [
        (10, 100, 100, 100),
        (16, 100, 100, 100),
        (1, 100, 100, 100),
    ]
)
def test_get_random_input_variables(n, max_mass, max_distance, max_speed):
    variables = get_random_input_variables(n, max_mass, max_distance, max_speed)
    assert len(variables) == 3
    masses, positions, velocities = variables
    assert len(masses) == len(positions) == len(velocities)
    

if __name__ == "__main__":
    test_get_mass()
    test_get_position()
    test_get_velocity()

    test_get_masses()
    test_get_positions()
    test_get_velocities()

    test_get_random_input_variables()