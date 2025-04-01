""" Module for calculating and updating the motion of particles. """

from numpy import ndarray, zeros

from src.classes.config import CFG
from src.classes.particle import Particle
from src.permutations import all_chosen_and_others
from src.collision_handler import get_disp_dist_and_handle_collisions
from src.data_types import Particles, IdPairVectorDict, IdPairFloatDict


def calc_accel_of_chosen(chosen: Particle, others: Particles, displacements: IdPairVectorDict, distances: IdPairFloatDict) -> ndarray:
    """ Calculates the acceleration of a chosen `Particle` given a list of the other `Particles` in the system. """
    total_accel = zeros(3)
    for other in others:
        total_accel += CFG.G * other.mass * displacements[(other.id, chosen.id)] / distances[(other.id, chosen.id)]**3
    return total_accel


def initialise_particles(particles: Particles) -> None:
    """ Calculates and assigns the initial accelerations of `Particles`; this is required to start the simulation loop. """
    CFG.logger.info("'Initialising particles'")
    displacements, distances = get_disp_dist_and_handle_collisions(particles)
    calc_and_update_accel(particles, displacements, distances)
        

def calc_and_update_position(particles: Particles) -> None:
    """ Updates the `position` attribute of each particle in `particles` using only its own attributes. """
    for particle in particles:
        particle.position = particle.position + particle.velocity*CFG.dt + particle.acceleration*CFG.half_dtsq


def calc_and_update_accel(particles: Particles, displacements: IdPairVectorDict, distances: IdPairFloatDict) -> None:
    """ Updates the `acceleration` attribute of each particle in `particles` using its `position` attribute. """
    for chosen, others in all_chosen_and_others(particles):
        chosen.acceleration = calc_accel_of_chosen(chosen, others, displacements, distances)


def calc_and_update_vel(particles_next: Particles, particles_last: Particles) -> None:
    """ Updates the `velocity` attribute of each particle in `particles_next` using state attributes from both `particles_next` and `particles_last`. """
    #* Requires access to last velocity and acceleration, but also next acceleration, so both particles are required.

    # Note: After collisions, length of `particles_next` and `particles_last` are different, so this 'pairing'/'matching' is first needed:
    remaining_ids = {ptcl.id for ptcl in particles_next}
    filtered_particles_last = [ptcl for ptcl in particles_last if ptcl.id in remaining_ids]

    for last, next in zip(filtered_particles_last, particles_next):
        next.velocity = last.velocity + (last.acceleration + next.acceleration)*CFG.dt/2


def simulate_timestep(particles: Particles) -> None:
    """
    Takes in a list of Particles.\n
    Returns None.\n
    First creates a copy of the old particle states, simulates a timestep on the original list,\n 
    looks for and handles any collisions, logs the updated positions.
    """
    CFG.logger.info("'Simulating timestep'")

    particles_saved = particles.copy()
    calc_and_update_position(particles)
    CFG.logger.info("'Updated positions.'")

    next_displacements, next_distances = get_disp_dist_and_handle_collisions(particles) #* Collided particles removed.
    CFG.logger.info(f"'Handled Collisions' {[ptcl.id for ptcl in particles]} remaining.")

    calc_and_update_accel(particles, next_displacements, next_distances)
    CFG.logger.info(f"'Updated accelerations'")

    calc_and_update_vel(particles, particles_saved)
    CFG.logger.info(f"'Updated velocities'")
