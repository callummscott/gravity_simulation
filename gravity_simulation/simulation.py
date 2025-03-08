""" Program to generate 3D plot of n-particle motion under the influence of gravity """
import matplotlib.pyplot as plt
import numpy as np
from time import time

from gravity_simulation.config import Config
from gravity_simulation.colour_picker import choose_distinct_rgb, rgb_to_0_1_format
from gravity_simulation.particle_setup import get_random_input_variables

CONFIG = Config()

class Symmetric(np.ndarray):
    """ Class to define symmetric matrices that serve to represent distances -- theoretically saves (n-1)/2n ~= 40% the distance calculations. """
    # Has problems with non-2d-element-specific assignment.
    def __new__(cls, n: int):
        obj = np.zeros((n, n), dtype=np.float64).view(cls)
        return obj

    def __setitem__(self, index, value):
        if not isinstance(index, slice):
            i, j = index
            if not (isinstance(i, int) and isinstance(j, int)):
                raise IndexError("Index must be a tuple of two integers")
            if i == j:
                self.data[i, i] = 0 # was 'value'
            else:  # Not sure if this check is actually faster than the double-assignment
                self.data[i, j] = value
                self.data[j, i] = value

    def __array_finalize__(self, obj):
        if obj is None: return

    def __repr__(self):
        return f"symmetric({self.__array__().__str__()})"


class Particle:
    """ Instances represent individual particles involved in simulation. Information about their mass, position, velocity are stored here. """
    def __init__(self, id:int, mass:float, initial_position:list, initial_velocity:list):
        self.id = id
        self.mass = mass
        self._position = np.array(initial_position)
        self._velocity = np.array(initial_velocity)
        self.next_position = None
        self.next_velocity = None
        
    """ attr: self.POSITION """
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    """ attr: self.VELOCITY """
    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    def momentum(self):
        return self.mass*self.velocity

class PositionLog:
    def __init__(self):
        self.xs = []
        self.ys = []
        self.zs = []

    def add_position(self, value):
        """ Adds an (x,y,z) position tuple """
        if type(value) != np.ndarray:
                raise TypeError
        try:
            x,y,z = value
            self.xs.append(x)
            self.ys.append(y)
            self.zs.append(z)
        except Exception:
            if len(value) != 3:
                raise IndexError("Position not 3 dimensional")
            for item in value:
                try:
                    float(item)
                except TypeError as e:
                    raise e("Coordinates not a valid numerical value")

    def get_xyz_tuple(self):
        return (self.xs, self.ys, self.zs)


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


def get_filtered_xyz_values(position_log: dict) -> dict:
    """ Returns a dictionary of { Particle key: position log }, where some data is being filtered out for plot framerate """
    #* Builds a blank output data structure
    print("Filtering data-points before plotting")
    filtered_positions = dict()
    #* Iterates across each particle and its position log
    #*  > Length of of position logs across particles can vary
    final_log_rate = 
    for id, log in position_log.items(): # essentially, log = [ [x,y,z], [x,y,z], ... ]
        xs, ys, zs = log.xs, log.ys, log.zs
        filtered_xs, filtered_ys, filtered_zs  = [], [], []
        for i in range(len(xs)):
            if i % CONFIG.simple_log_rate == 0:
                CONFIG.logger.info(f"{i}: {xs[i]}, {ys[i]}, {zs[i]}")
                filtered_xs.append(xs[i])
                filtered_ys.append(ys[i])
                filtered_zs.append(zs[i])
        filtered_positions[id] = (filtered_xs, filtered_ys, filtered_zs)
    return filtered_positions


def plot_results_3d(filtered_positions: dict[int:PositionLog]):
    """ Takes in a dictionary of { particle key : filtered position log }, generates 3D plot """

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    past_colours = []
    for id, log in filtered_positions.items():
        xs, ys, zs = log
        particle_colour_rgb, new_past_colours = choose_distinct_rgb(past_colours)
        particle_colour_0_1 = rgb_to_0_1_format(particle_colour_rgb)
        past_colours = new_past_colours #? Change the function to one that just appends the chosen colour? 
        ax.scatter3D(xs, ys, zs, marker='o', color=particle_colour_0_1, label=f"{id}")
        ax.plot3D(xs, ys, zs)
        ax.text3D(xs[0], ys[0], zs[0], f"Particle {id}")
        ax.legend()

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    ax.axis('equal')

    yield time()

    plt.show()
