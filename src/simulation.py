""" Program to generate 3D plot of n-particle motion under the influence of gravity """
from numpy import empty, nan, ndarray, float64
from numpy.linalg import norm

from src.classes.config import CFG
from src.classes.particle import Particle
from src.classes.position_log import PositionLog

Particles = list[Particle]
IdPair = tuple[int, int]
VectorDict = tuple[IdPair: ndarray]
FloatDict = tuple[IdPair: float64]



def get_displacements_and_distances(particles: Particles) -> tuple[VectorDict, FloatDict]:
    """ v4.1 """
    displacements, distances = dict(), dict()
    particles_left = particles.copy()
    chosen = particles_left[0]
    particles_left.remove(chosen)
    while particles_left:
        for other in particles_left:
            # Calculate and assign displacements to id_pairs
            displacement = chosen.position - other.position
            displacements[(chosen.id, other.id)] = displacement
            displacements[(other.id, chosen.id)] = -displacement
        chosen = particles_left[0]
        particles_left.remove(chosen)
    # Calculate distances
    for id_pair, displacement in displacements.items():
        distances[id_pair] = norm(displacement)
    return displacements, distances


def collision_handler(particles: Particles) -> Particles:
    """ Checks if any distances are less than threshold, calculates state variables and merges all collisions with most massive particle, returns updated Particle list with other collided ones removed """

    distances = get_distance_matrix(particles)

    colliding_particle_pairs = []

    # Builds list of unique particle pairs that are colliding
    particle_set = set(particle.id for particle in particles)
    for id in range(CFG.number_of_particles):
        if id in particle_set:
            for jd in range(id+1, CFG.number_of_particles): #* i+1 ensures it doesn't look at [i,i] elements
                if jd in particle_set:
                    # CFG.logger.info(f"Checking between : i={id} & j={jd}")
                    if distances[id, jd] < CFG.collision_distance:
                        CFG.logger.info(f" ^ Collision found!")
                        colliding_particle_pairs.append({id, jd})

    # Checks for any collion-pairs and 'collides' them -- i.e. removes the collided particle with the smallest mass from the list
    if colliding_particle_pairs:
        CFG.logger.info(f"Colliding pairs: {colliding_particle_pairs}")
        CFG.logger.info(particles)
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
            CFG.logger.info(f"Particles after popping: {particles}")
    
    return particles



def collision_check(particles: Particles):
    # 
    ...

def update_particles(particles: Particles):
    # if not particle.acceleration: do the initial stuff
    ...

def calculate_and_assign_accelerations(particles: Particles, next_accel: bool=False) -> None:
    remaining_ids = list(particles)

    for _ in range(len(remaining_ids)):
        chosen_id = remaining_ids[0]
        remaining_ids.pop(0) #* Experiments suggesting this is the fastest element remover
        acceleration = empty(3)
        for other_id in remaining_ids:
            chosen, other = particles[chosen_id], particles[other_id]
            if next_accel:
                vector_from_chosen_to_other = other.next_position - chosen.next_position
            else:
                vector_from_chosen_to_other = other.position - chosen.position
            acceleration += CFG.G*other.mass*(vector_from_chosen_to_other) / norm(vector_from_chosen_to_other)**3
        if next_accel:
            particles[chosen_id].next_acceleration = acceleration
        else:
            particles[chosen_id].acceleration = acceleration
    return particles


def get_next_particle_states(particles: dict[int: Particle]) -> dict[int: Particle]:
    """ Takes in Particles, calculates changes in motion, updates Particle attributes, returns Particles """
    dt        = CFG.timestep
    half_dtsq = CFG.half_dtsq
    
    for particle in particles.values():
        particle.next_position = particle.position + particle.velocity*dt + particle.acceleration*half_dtsq   

    for particle in particles.values():
        calculate_and_assign_accelerations(particles, next_accel=True)

    for particle in particles.values():
        particle.next_velocity = particle.velocity + .5*(particle.acceleration + particle.next_acceleration)*dt       
        
    for particle in particles.values():
        particle.position = particle.next_position
        particle.velocity = particle.next_velocity
        particle.acceleration = particle.next_acceleration

    return particles


def get_updated_position_logs(position_logs: PositionLog, particles: Particles) -> PositionLog:
    for particle in particles:
        position_logs[particle.id].cache_position(particle.position)

    # CFG.logger.info(position_logs)
    return position_logs