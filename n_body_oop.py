""" Program to generate 3D plot of n-particle motion under the influence of gravity """

import config
import particle_setup
import numpy as np
import matplotlib.pyplot as plt
import time


class Symmetric(np.ndarray):
    """ Class to define symmetric matrices that serve to represent distances -- theoretically saves (n-1)/2n ~= 40% the distance calculations. """
    # Has problems with non-2d-element-specific assignment.
    def __new__(cls, n: int):
        obj = np.zeros((n, n)).view(cls)
        return obj

    def __setitem__(self, index, value):
        i, j = index
        if not (isinstance(i, int) and isinstance(j, int)):
            raise IndexError("Index must be a tuple of two integers")
        if i == j:
            self.data[i, i] = value
        else:  # Not sure if this check is actually faster than the double-assignment
            self.data[i, j] = value
            self.data[j, i] = value

    def __array_finalize__(self, obj):
        if obj is None: return

    def __repr__(self):
        return f"symmetric({self.__array__().__str__()})"

class General:
    """ Class to handle information related to all instances of particles """
    distances_matrix = Symmetric(config.number_of_particles)
    distances_cubed = distances_matrix

    def initialise_particle_data(mass_list, initial_positions, initial_velocities):
        General.all = { i+1 : Particle(mass_list[i], initial_positions[i], initial_velocities[i]) for i in range(config.number_of_particles)}
        General.items = General.all.items()

    def update_distance_matrices():
        for i in range(0, config.number_of_particles):
            for j in range(i+1, config.number_of_particles):
                General.distances_matrix[i,j] = np.linalg.norm(General.all[i+1].position - General.all[j+1].position)
        General.distances_cubed = General.distances_matrix**3

    def distance_cubed_from_a_to_b(key_a, key_b):
        return General.distances_cubed[key_a-1, key_b-1]
    
    def acceleration_of_(key_a):
        vector_sum = np.empty(3)
        for key_b, other_particle in General.items:
            if key_b == key_a:
                continue
            else:
                vector_sum += other_particle.mass * (other_particle.position - General.all[key_a].position) / General.distance_cubed_from_a_to_b(key_a, key_b)
        return config.G * vector_sum
    
    def acceleration_derivate_of_(key_a):
        vector_sum = np.empty(3)
        for key_b, other_particle in General.items:
            if key_b == key_a:
                continue
            else:
                vector_sum += other_particle.mass * (other_particle.velocity - General.all[key_a].velocity) / General.distance_cubed_from_a_to_b(key_a, key_b)
        return config.G * vector_sum

    
    def get_particles_logged_pos():
        ...
    
class Particle:
    """ Instances represent individual particles involved in simulation. Information about their mass, position, velocity are stored here. """
    def __init__(self, mass:float, initial_position:list, initial_velocity:list):
        self.mass = mass
        self._position = np.array(initial_position)
        self._velocity = np.array(initial_velocity)
        self._next_position = None
        self._next_velocity = None
        self.position_log = []
        self.log_counter = 0
        
    """ attr: self.POSITION """
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        raise AttributeError("position cannot be changed directly by user")
    
    """ attr: self.VELOCITY """
    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        raise AttributeError("velocity cannot be changed directly by user")

    def log_position(self):
        # Contains a 'limiter' to speed up visualisation.
        self.log_counter += 1
        if self.log_counter % config.simple_log_rate == 0:
            self.position_log.append(self._position)


def step_and_log_particle_motion() -> None:
    """ Should this be a General static method or exist outside of the General class? """
    General.update_distance_matrices()

    for particle_key, particle in General.items:
        particle.log_position()
        particle._next_position = particle._position + particle._velocity*config.timestep + General.acceleration_of_(particle_key)*config.half_dtsq
        particle._next_velocity = particle._velocity + General.acceleration_of_(particle_key)*config.timestep + General.acceleration_derivate_of_(particle_key)*config.half_dtsq

    # Only after *all* of the next state's features are calculated, then updates positions and velocities
    for _, particle in General.items:
        particle._position = particle._next_position
        particle._velocity = particle._next_velocity

def get_particles_filtered_xyz() -> dict:
    """ Returns a dictionary of particle key : logged positional information -- i.e. after having filtered out some for efficiency """
    key_to_logged_xyzs = {}
    key_to_logged_positions = { key : General.all[key].position_log for key in General.all }

    for key, particle_positions in key_to_logged_positions.items():
        x_coords, y_coords, z_coords = [], [], []
        for position_index, position in enumerate(particle_positions):
            if log_to_output_filter(position_index):
                x_coords.append(position[0])
                y_coords.append(position[1])
                z_coords.append(position[2])

        key_to_logged_xyzs[key] = (x_coords, y_coords, z_coords)
    return key_to_logged_xyzs

def log_to_output_filter(index:int) -> bool:
    """ Takes in index, serves to help filter out excessive data-points for the 3D plot """
    if index % config.simple_log_rate == 0:
        return True
    else:
        return False

def plot_results_3d(data_dict:dict) -> None:
    """ Takes in a dictionary of particle key : positional data-points, generates 3D plot """
    fig = plt.figure()
    ax = plt.axes(projection='3d')   
    
    for particle in data_dict:
        xs, ys, zs = data_dict[particle]
        ax.scatter3D(xs, ys, zs, marker='o',color=particle_setup.Visuals.get_distinct_rgb_tuple(), label=f"{particle}")
        ax.plot3D(xs, ys, zs)
        ax.text3D(xs[0], ys[0], zs[0], f"Particle {particle}")
        ax.legend()

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    ax.axis('equal')

    plt.show()


def main():
    """ Retrives and sets up initial particle data from `particle_setup`,
        iteratively calculates and logs particle motion for defined period,
        converts positional data to (x,y,z) coordinates and plots results in 3D  """

    masses, positions, velocities = particle_setup.get_input_variables()
    General.initialise_particle_data(masses, positions, velocities)

    for _ in range(config.number_of_steps):    
        step_and_log_particle_motion()

    results = get_particles_filtered_xyz()
    plot_results_3d(results)
    

if __name__ == "__main__":
    main()