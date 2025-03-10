""" Program to generate 3D plot of n-particle motion under the influence of gravity """
import numpy as np

from gravity_simulation.classes.config import Config
from gravity_simulation.classes.particle import Particle
from gravity_simulation.classes.symmetric import Symmetric
from gravity_simulation.classes.position_log import PositionLog

from gravity_simulation.particle_setup import get_random_input_variables

CONFIG = Config()


def initialise_random_particles(n: int, max_mass: float, max_distance: float, max_speed: float) -> dict:
    """ Sets up and returns a dict of n Particles with random attributes """       

    if not isinstance(n, int):
        raise TypeError
    elif n < 0:
        raise ValueError("N cannot be less than 0")
    elif n > 16:
        raise ValueError("Too many particles for the number of colours")
    
    masses, initial_positions, initial_velocities = get_random_input_variables(n, max_mass, max_distance, max_speed)
    CONFIG.logger.info("Input variables recieved")

    particles = { i: Particle( id=i, mass=masses[i], initial_position=initial_positions[i], initial_velocity=initial_velocities[i]) for i in range(n) }
    return particles


def get_distance_matrix(particles: dict) -> Symmetric:
    """ Calculates and returns the symmetric distance matrix for a dictionary of Particles """
    distance_matrix = Symmetric(CONFIG.number_of_particles)
    all_particle_ids = list(range(CONFIG.number_of_particles))
    remaining_particle_ids = set(particles)

    distance_matrix[:] = np.nan
    for id in remaining_particle_ids:
        for jd in remaining_particle_ids:
            distance_matrix[id, jd] = np.linalg.norm(particles[id].position - particles[jd].position)
    
    return distance_matrix


def get_force_on_particle(particle_id: int, particles: dict, distance_cubed_matrix: Symmetric) -> np.array:
    """  """
    # Requiring distance matrix as argument to save on re-computing it every single time
    vector_sum = np.empty(3)
    for other_id, other_particle in particles.items():
        if other_id == particle_id:
            continue
        else:
            # F = m * a
            vector_sum += other_particle.mass * (other_particle.position - particles[particle_id].position) / distance_cubed_matrix[particle_id, other_id]
    
    return vector_sum   #* Don't forget the removed CONFIG.G referece


def get_impulse_on_particle(particle_id: int, particles: dict, distance_cubed_matrix: Symmetric) -> np.array:
    vector_sum = np.empty(3)
    for other_id, other_particle in particles.items():
        if other_id == particle_id:
            continue
        else:
            # F = m * a -- in a sense
            vector_sum += other_particle.mass * (other_particle.velocity - particles[particle_id].velocity) / distance_cubed_matrix[particle_id, other_id]
    return vector_sum  #* Don't forget the removed CONFIG.G referece


def collision_handler(particles: dict[int: Particle]) -> dict[int: Particle]:
    """ Checks if any distances are less than threshold, calculates state variables and merges all collisions with most massive particle, returns updated Particle dictionary with other collided ones removed """

    CONFIG.logger.info("--- Handling potential Collisions ---")
    distances = get_distance_matrix(particles)

    colliding_particle_pairs = []

    # Builds list of unique particle pairs that are colliding
    particle_set = set(particles)
    for id in range(CONFIG.number_of_particles):
        if id in particle_set:
            for jd in range(id+1, CONFIG.number_of_particles): #* i+1 ensures it doesn't look at [i,i] elements
                if jd in particle_set:
                    CONFIG.logger.info(f"Checking between : i={id} & j={jd}")
                    if distances[id, jd] < CONFIG.collision_distance:
                        CONFIG.logger.info(f" ^ Collision found!")
                        colliding_particle_pairs.append({id, jd})

    # Checks for any collion-pairs and 'collides' them, removing smallest from particles
    if colliding_particle_pairs:
        CONFIG.logger.info(f"Colliding pairs: {colliding_particle_pairs}")
        CONFIG.logger.info(particles)
        #* Iterate across every colliding pair
        #* Merge smallest into largest (i.e. combine masses, remove smallest)
        #* Conserve momentum
        for pair_ids in colliding_particle_pairs:
            first, second = (particles[id] for id in pair_ids)
            total_momentum = first.momentum() + second.momentum()
            total_mass = first.mass + second.mass

            biggest, smallest = (first, second) if (first.mass >= second.mass) else (second, first)
            biggest.mass = total_mass
            biggest.velocity = total_momentum/total_mass

            particles.pop(smallest.id)
            CONFIG.logger.info(f"Particles after popping: {particles}")
    
    return particles


def get_next_particle_states(particles: dict[int: Particle]) -> None:
    """ Takes in Particles, calculates changes in motion, updates Particle attributes, returns """

    distances_cubed = get_distance_matrix(particles)**3
    
    G         = CONFIG.G
    dt        = CONFIG.timestep
    half_dtsq = CONFIG.half_dtsq

    for particle_id, particle in particles.items():                
        force = get_force_on_particle(particle_id, particles, distances_cubed)
        impulse = get_impulse_on_particle(particle_id, particles, distances_cubed)

        delta_pos = particle.velocity*dt + G*force*half_dtsq/particle.mass
        delta_vel = G*(force*dt + impulse*half_dtsq)/particle.mass

        particle.next_position = particle.position + delta_pos
        particle.next_velocity = particle.velocity + delta_vel

    # Have to separate these reassignments so that the calculations all apply to the particle's state in the *previous* step
    for particle in particles.values():
        particle.position = particle.next_position
        particle.velocity = particle.next_velocity

    return particles


def get_updated_position_logs(position_logs: PositionLog, particles: Particle) -> PositionLog:
    for id, particle in particles.items():
        position_logs[id].add_position(particle.position)

    # CONFIG.logger.info(position_logs)
    return position_logs