
import pytest
from numpy.linalg import norm

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


## N_IS_VALID ##

@pytest.mark.parametrize( "n", [1, 10, 12, 10, 16, 4, 7] )
def test_n_is_valid(n):
    assert n_is_valid(n)


@pytest.mark.parametrize( "n", [0, 17, -10, 20, 128] )
def test_n_is_vlaid_value_error(n):
    with pytest.raises(ValueError):
        n_is_valid(n)


@pytest.mark.parametrize( "n", ["test", [1,2,3], None, [], 2.34])
def test_n_is_valid_type_error(n):
    with pytest.raises(TypeError):
        n_is_valid(n)


## GET_MASSES ##

@pytest.mark.parametrize(
    "n, max_mass",
    [
        (1, 100),
        (10, 40.43),
        (3, 100_123_543),
        (12, 34.34e14)
    ]
)
def test_get_masses(n, max_mass):
    assert len(get_masses(n, max_mass)) == n
    for mass in get_masses(n, max_mass):
        assert (0 < mass < max_mass) or (mass == pytest.approx(0)) or (mass == pytest.approx(max_mass))


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



## INITIALISE_RANDOM_PARTICLES ##

@pytest.mark.parametrize(
    "n, max_mass, max_distance, max_speed",
    [
        (3, 100, 100, 100),
        (1, 10, 20, 20),
        (16, 1e5, 3.2e4, 5.5e2),
        (12, 2.345, 1323.4123, 8654.231)
    ]
)
def test_initialise_random_particles(n, max_mass, max_distance, max_speed):
    particles = initialise_random_particles(n, max_mass, max_distance, max_speed)
    for particle in particles.values():
        distance, speed = norm(particle.position), norm(particle.velocity)
        assert (0 < particle.mass < max_mass) or (particle.mass == pytest.approx(max_mass))
        assert (distance < max_distance) or (distance == pytest.approx(max_distance))
        assert (speed < max_speed) or (speed == pytest.approx(speed))

            # assert (0 < particle.mass <= CONFIG.max_mass) # no approx necessary
            # assert (0 <= particle_distance <= CONFIG.max_distance) or (particle_distance == pytest.approx(0)) or (particle_distance == pytest.approx(CONFIG.max_distance))
            # assert (0 <= particle_speed <= CONFIG.max_speed) or (particle_speed == pytest.approx(0)) or (particle_speed == pytest.approx(CONFIG.max_speed))

@pytest.mark.parametrize(
    "n, max_mass, max_distance, max_speed",
    [
        ("8", 1, 1, 1),
        (10.5, 1, 1, 1)
    ]
)
def test_initialise_random_particles_type_error(n, max_mass, max_distance, max_speed):
    with pytest.raises(TypeError):
        initialise_random_particles(n, max_mass, max_distance, max_speed)


@pytest.mark.parametrize(
    "n, max_mass, max_distance, max_speed",
    [
        # -- n values --
        (0, 1, 1, 1),
        (-3, 1, 1, 1),
        (-10, 1, 1, 1),
        (17, 1, 1, 1),
        (30, 1, 1, 1),
        # -- mass values --
        (7, 0, 1, 1),
        (12, -1, 1, 1),
        (10, -12.3, 1, 1),
        # -- distance values --
        (9, 12e3, 0, 123.32),
        (6, 111.11, -10, 4234.3),
        (1, 123123.2, -12.3, 4234.3),
        # -- speed values --
        (3, 111.11, 4234.3, -10),
        (14, 123123.2, 32341421312.3232, -12.3)
    ]
)
def test_initialise_random_particles_value_error(n, max_mass, max_distance, max_speed):
    with pytest.raises(ValueError):
        initialise_random_particles(n, max_mass, max_distance, max_speed)

