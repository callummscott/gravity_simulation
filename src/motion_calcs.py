""" Module for calculating and updating the motion of particles. """

from numpy import ndarray, zeros
from copy import deepcopy

from src.classes.config import Config
from src.classes.particle import Particle
from src.permutations import all_chosen_and_others
from src.collision_handler import get_disp_dist_and_handle_collisions
from src.data_types import Particles, IdPairVectorDict, IdPairFloatDict


def calc_accel_of_chosen(chosen: Particle, others: Particles, displacements: IdPairVectorDict, distances: IdPairFloatDict, config_object: Config) -> ndarray:
    """ Calculates the acceleration of a chosen `Particle` given a list of the other `Particles` in the system. """
    total_accel = zeros(3)
    for other in others:
        total_accel += config_object.G * other.mass * displacements[(other.id, chosen.id)] / distances[(other.id, chosen.id)]**3
    return total_accel


def initialise_particles(particles: Particles, config_object: Config) -> None:
    """ Calculates and assigns the initial accelerations of `Particles`; this is required to start the simulation loop. """
    displacements, distances = get_disp_dist_and_handle_collisions(particles, config_object)
    calc_and_update_accel(particles, displacements, distances, config_object)
        

def calc_and_update_position(particles: Particles, config_object: Config) -> None:
    """ Updates the `position` attribute of each particle in `particles` using only its own attributes. """
    for particle in particles:
        particle.position = particle.position + particle.velocity*config_object.dt + particle.acceleration*config_object.half_dtsq


def calc_and_update_accel(particles: Particles, displacements: IdPairVectorDict, distances: IdPairFloatDict, config_object: Config) -> None:
    """ Updates the `acceleration` attribute of each particle in `particles` using its `position` attribute. """
    for chosen, others in all_chosen_and_others(particles):
        chosen.acceleration = calc_accel_of_chosen(chosen, others, displacements, distances, config_object)


def calc_and_update_vel(particles_next: Particles, particles_last: Particles, config_object: Config) -> None:
    """ Updates the `velocity` attribute of each particle in `particles_next` using state attributes from both `particles_next` and `particles_last`. """
    #* Requires access to last velocity and acceleration, but also next acceleration, so both particles are required.

    # Note: After collisions, length of `particles_next` and `particles_last` are different, so this 'pairing'/'matching' is first needed:
    remaining_ids = {ptcl.id for ptcl in particles_next}
    filtered_particles_last = [ptcl for ptcl in particles_last if ptcl.id in remaining_ids]

    for last, next in zip(filtered_particles_last, particles_next):
        next.velocity = last.velocity + (last.acceleration + next.acceleration)*config_object.dt/2


def simulate_timestep(particles: Particles, config_object: Config) -> None:
    """
    Takes in a list of Particles.\n
    Returns None.\n
    First creates a copy of the old particle states, simulates a timestep on the original list,\n 
    looks for and handles any collisions, logs the updated positions.
    """
    # config_object.logger.info("'Simulating timestep'")

    particles_saved = deepcopy(particles) #* `deepcopy` Doesn't *seem* to make a difference but may as well use it to be sure.
    calc_and_update_position(particles, config_object)
    # config_object.logger.info("'Updated positions.'")

    next_displacements, next_distances = get_disp_dist_and_handle_collisions(particles, config_object) #* Collided particles removed.
    # config_object.logger.info(f"'Handled Collisions' {[ptcl.id for ptcl in particles]} remaining.")

    calc_and_update_accel(particles, next_displacements, next_distances, config_object)
    # config_object.logger.info(f"'Updated accelerations'")

    calc_and_update_vel(particles, particles_saved, config_object)
    # config_object.logger.info(f"'Updated velocities'")
