import numpy as np
import matplotlib.pyplot as plt
import particle_setup
import time
import random
import config


class Symmetric(np.ndarray):
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

class Particle:

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
        if self.log_counter % self.parent._simple_log_rate == 0:
            self.position_log.append(self._position)

def plot_results_3d(data_dict) -> None:
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')   

    print('Beginning coordinate dissection')
    
    for particle in data_dict:
        xs, ys, zs = data_dict[particle]
        ax.scatter3D(xs, ys, zs, marker='o',color=random.choice(['red', 'blue', 'green', 'yellow', 'purple', 'black', 'teal']), label=f"{particle}")
        ax.plot3D(xs, ys, zs)
        ax.text3D(xs[0], ys[0], zs[0], f"Particle {particle}")
        ax.legend()

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    ax.axis('equal')

    plt.show()


def run_full_simulation_on(object:Particles) -> None:
    steps = int(config.maximum_time/config.timestep)
    for _ in range(steps):
        object.step_and_log_motion()

def get_particles_logged_xyz(object:Particles) -> dict[ int : tuple[list,list,list] ]:

    N = config.number_of_particles
    key_to_logged_xyz = {}
    
    particle_key_to_logged_positions = { i : object[i].position_log for i in range(1,N+1) }

    for key in particle_key_to_logged_positions:
        x_coords, y_coords, z_coords = [], [], []
        for position in particle_key_to_logged_positions[key]:
            x_coords.append(position[0])
            y_coords.append(position[1])
            z_coords.append(position[2])

        key_to_logged_xyz[key] = (x_coords, y_coords, z_coords)

    return key_to_logged_xyz



def acceleration_of_particle_in_dict(all_particles:dict, key_a:int, distances_cubed:Symmetric):
    vector_sum = np.empty(3)
    for key_b, other_particle in all_particles.items():
        if key_b == key_a:
            continue
        else:
            vector_sum += other_particle.mass * (other_particle.position - all_particles[key_a].position) / distances_cubed[key_a-1, key_b-1]
    return config.G * vector_sum

def acceleration_derivate_of_(all_particles:dict, key_a, distances_cubed):
        vector_sum = np.empty(3)
        for key_b, other_particle in all_particles.items():
            if key_b == key_a:
                continue
            else:
                vector_sum += other_particle.mass * (other_particle.velocity - all_particles[key_a].velocity) / distances_cubed[key_a-1, key_b-1]
        return config.G * vector_sum

def update_distances_from_dict(distance_matrix:Symmetric, particles_dict:dict):
    for i in range(config.number_of_particles):
        for j in range(i+1, config.number_of_particles):
            # self[k].position, hopefully, gets us the position of particle k.
            distance_matrix[i,j] = calculate_distance_from_a_to_b(particles_dict[i+1], particles_dict[j+1])
    
def calculate_distance_from_a_to_b(particle_a:Particle, particle_b:Particle):
    return np.linalg.norm(particle_b.position - particle_a.position)


def log_and_calc_particle_motion(all_particles:dict, particle:Particle, distance_matrix:Symmetric):
    distances_cubed = distance_matrix**3
    particle.log_position()
    particle._next_position = particle._position + particle._velocity*config.timestep + acceleration_of_particle_in_dict(all_particles, particle, distances_cubed)*config.half_dtsq
    particle._next_velocity = particle._velocity + acceleration_of_particle_in_dict(all_particles, particle, distance_matrix)*config.timestep + acceleration_derivate_of_()*config.half_dtsq
        
def update_all_particles(particles:dict):
    for particle in particles.values():
        particle._position = particle._next_position
        particle._velocity = particle._next_velocity


def particle_generator(mass:float=None, position:np.ndarray=None, velocity:np.ndarray=None):
    if config.random_inputs:
        input_mass, input_position, input_velocity = particle_setup.get_particle_info()
        return Particle(input_mass, input_position, input_velocity)
    else:
        print("Non-random particle inputs have not been calibrated yet")
             
def get_all_particles_dictionary(all_masses=None, all_positions=None, all_velocities=None):
    output_dictionary = {}
    if config.random_inputs:
        for key in range(config.number_of_particles):
            output_dictionary[key+1] = particle_generator()
    else:
        print("Non-random, all particle inputs haven't been set up yet")
    return output_dictionary

def main():
    """
    1) Create dictionary of all particles
    2) Initialise distances matrices
    3) Begin full simulation loop: Log particle data in form that's fit for later collection
    4) Each timestep we perform all calculationss (distances, next_pos, next_vel, etc.) 'synchronously'
    5) After next pos. etc. calculated, overwrite all current data with next_data -- reset next_data?
    6) Repeat until the settings times are complete
    7) Retrieve and store logged particle data in desirable format
    8) Filter out unnecessary pyplot points before visualisation
    9) Visualize data with pyplot
    """
    # 1
    particles_dictionary = get_all_particles_dictionary() # No inputs because config.random_inputs==True
    particles_list = particles_dictionary.values()
    # 2
    distances_matrix = Symmetric(config.number_of_particles)
    # 3 4 5 6
    for _ in range(config.number_of_steps):
        update_distances_from_dict(distances_matrix, particles_dictionary)
        distances_cubed = distances_matrix**3
        for particle in particles_list: 
            log_and_calc_particle_motion(particle)

        update_all_particles(particles_dictionary)
        
    

    run_full_simulation_on(particles)

    results = get_particles_logged_xyz(particles)
    plot_results_3d(results)
    

if __name__ == "__main__":
    main()