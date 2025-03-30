""" Module for finding, grouping, and handling collisions between particles. """

from numpy import zeros
from numpy.linalg import norm
from src.classes.config import CFG
from src.data_types import Particles, IdCollection, IdPairVectorDict, IdPairFloatDict
from src.permutations import ordered_pairs_permutations, get_others


def collision_pairs_finder(distances: IdPairFloatDict, ordered_pairs: list[tuple]) -> IdCollection:
    """
    Takes in `distances` and ordered `ordered_pairs_permutations`.\n
    Outputs a list of sets containing pairs of IDs of particles that are colliding with one another.
    """
    collision_pairs = list()
    for x, y in ordered_pairs:
        if distances[(x.id, y.id)] <= CFG.collision_distance:
            collision_pairs.append({x.id, y.id})
            # print(f"Collision between {id_pair[0]} and {id_pair[1]}.")
    return collision_pairs


def collided_id_grouper(id_collection: IdCollection) -> IdCollection:
    """
    Looks at every possible ordered pair permutation and merges them if an intersection exists,\n
    repeating until all possible merges are exhausted.\n
    Returns list containing sets of mutually colliding ids.
    """
    merged = id_collection.copy()
    def merger(array: IdCollection) -> IdCollection:
        new_array = array.copy()
        for group1, group2 in ordered_pairs_permutations(array):
            if group1.intersection(group2):
                group1 |= group2
                new_array.remove(group2)
                return new_array
        return array
    #* Repeats trying to merge until all possible merges are complete.
    while (updated_merged:=merger(merged)) != merged:
        merged = updated_merged
    return merged


def collision_handler(particles: Particles, collision_pairs: IdCollection) -> None:
    """
    Takes in a `Particles` list, and an `IdCollection` representing ID pairs of particles that are both colliding with each other.\n
    Returns an abbreviated list of the updated particles, post-collision.\n
    
    Determines which particles are colliding with one another, establishes which is the largest of the group,\n
    combines the masses of the group together, averages their position, conserves their momenta, and removes the smaller particles.
    """
    mutually_colliding_ids = collided_id_grouper(collision_pairs)

    CFG.logger.info(f"'All particle states':")
    for ptcl in particles:
        CFG.logger.info(f"{ptcl.id}: mass={ptcl.mass}, pos={ptcl.position}, vel={ptcl.velocity}")

    CFG.logger.info(f"Checking all collision groups: {mutually_colliding_ids}")

    for collision_group_ids in mutually_colliding_ids:
        collision_group_particles = [particle for particle in particles if particle.id in collision_group_ids]
        CFG.logger.info(f"Collision group: {[id for id in collision_group_ids]}")
        most_massive = max(collision_group_particles, key=lambda ptcl: ptcl.mass)

        total_mass, net_position, net_momentum = 0, zeros(3), zeros(3)
        for particle in collision_group_particles:
            # CFG.logger.info(f"'Checking particle' {particle.id}")
            # CFG.logger.info(f"  ptcl mass = {particle.mass}")
            # CFG.logger.info(f"  ptcl position = {particle.position}")
            # CFG.logger.info(f"  ptcl velocity = {particle.velocity}")
            # CFG.logger.info(f"  ptcl momentum = {particle.momentum()}")
            total_mass += particle.mass
            net_position += particle.position
            net_momentum += particle.momentum()
    
        most_massive.mass = total_mass
        most_massive.position = net_position / len(collision_group_particles)
        most_massive.velocity = net_momentum / total_mass

        for smaller in get_others(most_massive, collision_group_particles):
            CFG.logger.info(f"Removing other: {smaller.id}")
            particles.remove(smaller)
            CFG.logger.info(f"IDs remaining: {[ptcl.id for ptcl in particles]}")


def get_displacements_and_distances_from_ordered_pairs(ordered_pairs: list[tuple]) -> tuple[IdPairVectorDict, IdPairFloatDict]:
    """ Takes in an ordered particle pair list and outputs `displacements` and `distances` between all particles. """
    displacements, distances = dict(), dict()
    for x, y in ordered_pairs:
        displacement = x.position - y.position
        id_pair, id_pair_rev = (x.id, y.id), (y.id, x.id)
        # Update displacements
        displacements[id_pair] = displacement
        displacements[id_pair_rev] = -displacement
        # Update distances
        distances[id_pair] = norm(displacement)
        distances[id_pair_rev] = distances[id_pair] #*Much faster to lookup than recalculate.
    return displacements, distances


def get_disp_dist_and_handle_collisions(particles: Particles) -> tuple[IdPairVectorDict, IdPairFloatDict]:
    """
    Takes in a Particles list.\n
    Returns `displacements` and `distances` for post-collision particles.\n
    Calculates disp/dist and checks for collisions, if there are any then they're handled and then the loop repeats.\n
    When no collisions remain, disp/dist are calculated, collision_pairs is empty, and loop breaks.
    """
    collision_pairs = 1    # Functions as a 'do while'
    while collision_pairs: #
        ordered_pairs_list = list(ordered_pairs_permutations(particles)) #* Must be converted to list to reuse it

        displacements, distances = get_displacements_and_distances_from_ordered_pairs(ordered_pairs_list)
        collision_pairs = collision_pairs_finder(distances, ordered_pairs_list)
        if collision_pairs:
            collision_handler(particles, collision_pairs)
    return displacements, distances
