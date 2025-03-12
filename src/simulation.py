""" Program to generate 3D plot of n-particle motion under the influence of gravity """
import numpy as np

from src.classes.config import Config
from src.classes.particle import Particle
from src.classes.symmetric import Symmetric
from src.classes.position_log import PositionLog

CONFIG = Config()


def get_distance_matrix(particles: dict) -> Symmetric:
    """ Calculates and returns the symmetric distance matrix for a dictionary of Particles """
    distance_matrix = Symmetric(len(particles))
    remaining_particle_ids = set(particles)

    distance_matrix[:] = np.nan # Resets distances
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

    distances = get_distance_matrix(particles)

    colliding_particle_pairs = []

    # Builds list of unique particle pairs that are colliding
    particle_set = set(particles)
    for id in range(CONFIG.number_of_particles):
        if id in particle_set:
            for jd in range(id+1, CONFIG.number_of_particles): #* i+1 ensures it doesn't look at [i,i] elements
                if jd in particle_set:
                    # CONFIG.logger.info(f"Checking between : i={id} & j={jd}")
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

def calculate_kinetic_energy_of_particles(particles: dict) -> float:
    total_kinetic = 0
    for particle in particles.values():
        total_kinetic += .5*particle.mass*np.linalg.norm(particle.velocity)**2
    return total_kinetic

def calculate_potential_energy_of_particles(particles: dict) -> float:
    total_potential = 0
    distances = get_distance_matrix(particles)
    if len(particles) > 1: #* Skips calculation of potential energy if only 1 particle exists
        for i in range(len(particles)):
            particle_1 = particles[i]
            for j in range(i+1, len(particles)):
                particle_2 = particles[j]
                total_potential -= CONFIG.G*particle_1.mass*particle_2.mass / distances[i, j]
        return total_potential
    else:
        return 0


def calculate_total_energy_of_particles(particles: dict) -> float:
    total_energy = calculate_kinetic_energy_of_particles(particles) + calculate_potential_energy_of_particles(particles)    
    return total_energy


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

def get_next_particle_states_verlet(particles: dict[int: Particle]) -> None:
    """ Takes in Particles, calculates changes in motion, updates Particle attributes, returns """

    distances_cubed = get_distance_matrix(particles)**3
    
    G         = CONFIG.G
    dt        = CONFIG.timestep
    half_dtsq = CONFIG.half_dtsq

    for particle_id, particle in particles.items():                
        next_position = particle.position + particle.velocity*dt + half_dtsq*get_force_on_particle(particle)/particle.mass
        next_acceleration = get_force_on_particle(particle, particles, distances_cubed)

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