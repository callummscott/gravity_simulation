from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import time

class Symmetric(np.ndarray):

    # Has problems with non-2d-element-specific assignment.

    def __new__(cls, n: int):
        obj = np.zeros((n, n)).view(cls)
        return obj

    def __setitem__(self, index, value):
        i, j = index
        if not (isinstance(i, int) and isinstance(j, int)):
            raise IndexError("Index must be a tuple of two integers")
        self.data[i, j] = value
        self.data[j, i] = value

    def __array_finalize__(self, obj):
        if obj is None: return

    def __repr__(self):
        return f"symmetric({self.__array__().__str__()})"


class FONParticle:
    # Fixed Origin, Newtonian Particle
    #  i.e. acceleration calculated relative to fixed 'origin', not other bodies
    GM = 1.781e-2

    def __init__(self, initial_position:list, initial_velocity:list):
        # Takes lists as input because it's easier to input
        self.position = np.array(initial_position)
        self.velocity = np.array(initial_velocity)
        self._traj_checker()
    
    # self.POS_MAG
    @property
    def pos_mag(self):
        return self._pos_mag
    
    @pos_mag.setter
    def pos_mag(self, value):
        raise AttributeError("Cannot be changed directly")

    # self.POSITION
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        # This 'on-demand' definition saves a tonne of time somehow
        self._position = value
        self._pos_mag = mag(value)

    # self.VEL_MAG
    @property
    def vel_mag(self):
        # This 'on-demand' definition saves like 3.5s to the constant-update def.
        return self._vel_mag
    
    @vel_mag.setter
    def vel_mag(self, value):
        raise AttributeError("Cannot be changed directly")

    # self.VELOCITY
    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        self._velocity = value
        self._vel_mag = mag(value)

    # self.ACCELERATION
    @property
    def acceleration(self) -> np.ndarray:
        return -FONParticle.GM*self.position/self.pos_mag**3
    
    @acceleration.setter
    def acceleration(self, value):
        raise AttributeError("Access level: 'God' required to perform that action")
    
    # self.ENERGY
    @property
    def energy(self) -> float:
        return .5*self.vel_mag**2 - self.GM/self.pos_mag

    # self._TRAJ_CHECKER()
    def _traj_checker(self) -> None:
        metric = self.pos_mag*self.vel_mag**2
        if metric > 2*FONParticle.GM:
            print(f"{metric:.5f} > {2*FONParticle.GM:.5f}")
            return (response := input("Particle is on an escape trajectory, continue? (y/n) ").lower().strip())*(response=='n')
        else:
            return True
    
    # self.UPDATE_MOTION
    def update_motion(self, time_step:float) -> None:
        accel_dt = time_step*self.acceleration   # Whenever self.accelerate is called, it gets re-defined.

        # Erm, so the velocity calc calls for the old (t_i, not t_{i+1}) self.pos_mag, so I just reordered them,
        #  but I forgot that self.position calls for the v(t_i), so now r(t_i) depends on v_(t_{i+1}), which makes no sense.
        # However, it turns out that it somehow at least looks to be leading to way better results this way???
        self.velocity += accel_dt + (FONParticle.GM*self.velocity*time_step**2)/self.pos_mag**4 # ( was half_dt_accel*(3-2*timestep/self.pos_mag) )
        self.position += time_step*(self.velocity + accel_dt/2)


def get_all_axes(delta_t:float, max_time:int):

    divisions = int(max_time/delta_t)

    ts = np.linspace(0, max_time, divisions)
    xs, ys, zs = [np.empty(divisions) for _ in [1,2,3]]
    

    return (ts, xs, ys, zs)

def mag(array:np.array)->float:
    return np.linalg.norm(array)

def plot_results_3d(data_3d:tuple[np.array, np.array, np.array]) -> None:

    x_data, y_data, z_data = data_3d

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')

    ax.plot3D(x_data, y_data, z_data, 'blue')
    ax.plot3D(x_data[0], y_data[0], z_data[0], 'o', label='initial pos. 1', color='blue')
    ax.plot3D(0,0,0, 'o', label='origin', color='black')

    ax.axis('equal')
    ax.legend()

    plt.show()

def sfe_initial_to_results(initial_pos_list:list[float,float,float], initial_vel_list:list[float, float, float]) -> tuple[np.array, np.array, np.array]:

    t = time.process_time()

    particle = FONParticle(initial_pos_list, initial_vel_list)
    ts, x_results, y_results, z_results = get_all_axes(dt:=1/100, max_time:=10_000)
    
    # Timing UI
    divisions = max_time/dt
    percent = 0

    for i, _ in enumerate(ts):
        x_results[i], y_results[i], z_results[i] = particle.position
        particle.update_motion(dt)

        # Progress information
        if percent < (percent := round(i*100/divisions)):
            print(
                f"""Loading: {percent}%, Time elapsed: {time.process_time()-t:.2f}s""",
                end='\r')
            #print(f"Energy: {particle.energy:.9f} ")

    # More timing stuff
    elapsed_time = time.process_time() - t
    print(f"Total time elapsed: {elapsed_time}s" + ' '*20)

    return (x_results, y_results, z_results)

def sun_from_earth() -> None:

    # Good base values
    #pos: [4,10,.1]
    #vel: [-.05, .005, .002]

    # Interesting spread
    #[4, 8, .1]
    #[-.030, .01, .002]

    initial_position = [4, 8, .1]
    initial_velocity = [-.030, .01, .002]

    plot_results_3d(results:= sfe_initial_to_results(initial_position, initial_velocity))
    
    return None

def main():
    sun_from_earth()


if __name__ == "__main__":
    #shm3d()
    sun_from_earth()
    ...