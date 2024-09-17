import numpy as np
import matplotlib.pyplot as plt
import particle_setup
import time
import random

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

class Particles:

    G = .005
    total_points = 1_000

    def __init__(self, mass_list:list, initial_positions:list, initial_velocities:list):

        if (N := len(mass_list)) == len(initial_positions) == len(initial_velocities):
            self.number = N
        else:
            raise ValueError('Inputs are not of equal length')
        
        self._timestep = 1/100
        self._max_time = 10
        self._dict = { i+1 : Particle(self, mass_list[i], initial_positions[i], initial_velocities[i] )  for i in range(N) }
        self._dict_items = self._dict.items()

        self._initialise_distances_matrix()
        self._update_distances_cubed()
        self._initialised = None
    
    def __getitem__(self, item):
         return self._dict[item]
    
    def _initialise_distances_matrix(self):
        distance_matrix = Symmetric(self.number)
        for i in range(0, self.number):
            for j in range(i+1, self.number):
                distance_matrix[i,j] = self.calculate_distance_from_to(self[i+1].position, self[j+1].position)
        self._distances = distance_matrix
    
    def _update_distances(self):
        for i in range(0, self.number):
            for j in range(i+1, self.number):
                # self[k].position, hopefully, gets us the position of particle k.
                self._distances[i,j] = self.calculate_distance_from_to(self[i+1].position, self[j+1].position)

    def _update_distances_cubed(self):
        self._distances_cubed = self._distances**3

    """ attr: self._SIMPLE_LOG_RATE """
    @property
    def _simple_log_rate(self):
        return int(self.max_time/(self.total_points*self.timestep))
    
    @_simple_log_rate.setter
    def _simple_log_rate(self, value):
        raise AttributeError("Cannot update log rate directly")

    """ attr: self.DICT """
    @property
    def dict(self):
        return self._dict
    
    @dict.setter
    def dict(self):
        raise AttributeError("Can't directly change object dictionary")
    
    """ attr: self.TIMESTEP """
    @property
    def timestep(self):
        return self._timestep
    
    @timestep.setter
    def timestep(self, value):
        print(f"Caution: timestep updated to {value:.8f}")
        self._timestep = value
        self._half_dtsq = self._timestep**2 / 2

    """ attr: self.MAX_TIME """
    @property
    def max_time(self):
        return self._max_time
    
    @max_time.setter
    def max_time(self, value):
        print(f"Caution: max_time updated to {value:.3f}")
        self._max_time = value

    """ attr: self.DISTANCES """
    @property
    def distances(self):
        return self._distances
    
    @distances.setter
    def distances(self, value):
        raise AttributeError("Can't directly change distance matrix")

    """ method: self.ACCELERATION_OF_() """
    def acceleration_of_(self, n):
        vector_sum = np.empty(3)
        for key, other_particle in self._dict_items:
            if key == n:
                continue
            else:
                vector_sum += other_particle.mass * (other_particle.position - self[n].position) / self._get_distances_cubed_from_a_to_b(n, key)
        return self.G * vector_sum
    
    def acceleration_derivate_of_(self, n):
        vector_sum = np.empty(3)
        for key, other_particle in self._dict_items:
            if key == n:
                continue
            else:
                vector_sum += other_particle.mass * (other_particle.velocity - self[n].velocity) / self._get_distances_cubed_from_a_to_b(n, key)
        return self.G * vector_sum
    
    """ method: self.CALCULATE_DISTANCE_FROM_TO() """
    def calculate_distance_from_to(self, a, b):
        if isinstance(a, int) and isinstance(b, int):
            return np.linalg.norm(self[b].position - self[a].position)
        elif isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
            return np.linalg.norm(b-a)
        
    def _get_distances_cubed_from_a_to_b(self, key1, key2):
        if not (isinstance(key1, int) and isinstance(key2, int)):
            raise TypeError('Incorrect argument type')
        else:
            return self._distances_cubed[key1-1, key2-1]
        
    """ method: self.STEP_AND_LOG_MOTION() """
    def step_and_log_motion(self):
        
        for particle_key, particle in self._dict_items:
            particle.log_position()
            particle._next_position = particle._position + particle._velocity*self.timestep + self.acceleration_of_(particle_key)*self._half_dtsq
            particle._next_velocity = particle._velocity + self.acceleration_of_(particle_key)*self.timestep + self.acceleration_derivate_of_(particle_key)*self._half_dtsq ## NEEDS FINISHING

        # Only after *all* of the next state's features are calculated, then updates positions and velocities
        for _, particle in self._dict_items:
            particle._position = particle._next_position
            particle._velocity = particle._next_velocity

        self._update_distances()
        self._update_distances_cubed()
    
class Particle(Particles):

    def __init__(self, parent:Particles, mass:float, initial_position:list, initial_velocity:list):
        self.parent = parent
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
    
    N = len(data_dict)

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
    steps = int(object.max_time/object.timestep)
    for _ in range(steps):
        object.step_and_log_motion()

def get_particles_logged_xyz(object:Particles) -> dict[ int : tuple[list,list,list] ]:

    N = object.number
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

def initialise_runtime_variables(object:Particles, max_time, time_step):
    object.timestep = time_step
    object.max_time = max_time
    
def main():

    particle_setup.Settings.N = 4
    particle_setup.Settings.seed = 'testing123'

    example_masses = particle_setup.get_masses(max_value=100_000)
    example_inpos = particle_setup.get_positions(max_value=100)
    example_invel = particle_setup.get_velocities(max_value=1)

    particles = Particles(example_masses, example_inpos, example_invel)

    initialise_runtime_variables(particles, time_step=1/1000, max_time=100)
    run_full_simulation_on(particles)

    results = get_particles_logged_xyz(particles)
    plot_results_3d(results)
    

if __name__ == "__main__":
    main()