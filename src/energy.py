""" Module for calculating `Particles` system energies. """

from numpy import float64
from numpy.linalg import norm

from src.classes.config import Config
from src.motion_calcs import Particles
from src.permutations import ordered_pairs_permutations
from src.data_types import IdPairVectorDict, IdPairFloatDict


def get_displacements_and_distances(particles: Particles) -> tuple[IdPairVectorDict, IdPairFloatDict]:
    """
    Takes in a `particles` list.\n
    Returns a tuple containing displacement and distance dictionaries. 
    """
    displacements, distances = dict(), dict()
    for x, y in ordered_pairs_permutations(particles):
        # Calculate variables
        displacement = x.position - y.position
        id_pair, id_pair_rev = (x.id, y.id), (y.id, x.id)
        # Update displacements
        displacements[id_pair] = displacement
        displacements[id_pair_rev] = -displacement
        # Update distances
        distances[id_pair] = norm(displacement)
        distances[id_pair_rev] = distances[id_pair]
    return displacements, distances


def calculate_kinetic_energy_of_particles(particles: Particles) -> float64:
    """ Takes in `Particles` list and returns `float64` value representing their total kinetic energy. """
    return sum( .5 * ptcl.mass * norm(ptcl.velocity)**2 for ptcl in particles )


def calculate_potential_energy_of_particles(particles: Particles, config_object: Config) -> float64:
    """ Takes in a `Particles` list, returns a `float64` value representing their total potential energy. """
    total_potential = 0
    _, distances = get_displacements_and_distances(particles)
    for chosen, other in ordered_pairs_permutations(particles):
        total_potential -= config_object.G * chosen.mass * other.mass / distances[(chosen.id, other.id)]
    return total_potential


def calculate_total_energy_of_particles(particles: Particles, config_object: Config) -> float64:
    """ Takes in a `Particles` list and returns their total energy. """
    total_energy = calculate_kinetic_energy_of_particles(particles) + calculate_potential_energy_of_particles(particles, config_object)    
    return total_energy


def print_gravitational_boundedness(particles: Particles, config_object: Config) -> None:
    """ Takes in a `Particles` list and prints the system's total energy and bounded state. """
    total_energy = calculate_total_energy_of_particles(particles, config_object)
    print(f"The total system energy is: {total_energy:.2g} J:", "Bound." if (total_energy <=0 ) else "Unbound.")
