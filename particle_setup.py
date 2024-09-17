import random
import config



def get_mass():
    """ Returns a single random mass value from 0 to 1"""
    return random.random()*config.max_mass

def get_position():
    """ Returns a list of 3 random (x,y,z) coords from -max_dist to """
    return [random.uniform(-1,1)*config.max_distance for _ in range(3)]

def get_velocity():
    """ Returns a list of 3 random (vx,vy,vz) velocity values from -1 to 1"""
    return [random.uniform(-1,1)*config.max_speed for _ in range(3)]


def get_masses():
    """ Returns a list of masses; one for each of the `number of particles` """
    return [get_mass() for _ in range(config.number_of_particles)]

def get_velocities():
    """ Returns a list of velocity vectors; one for each of the `number_of_particles` """
    return [get_velocity() for _ in range(config.number_of_particles)]

def get_positions():
    """ Returns a list of position vectors; one for each of the `number_of_particles` """
    return [get_position() for _ in range(config.number_of_particles)]



def get_particle_info():
        if config.random_inputs:
            return (get_mass(), get_position(), get_velocity())
        else:
            print("non-random inputs not set up yet")

def get_mass_pos_vel():
    first = get_masses()
    second = get_positions()
    third = get_velocities()
    return (first, second, third)


def result_printer():
    print("\nPositions:")
    print("-------------------------------------------")
    for i in range(config.number_of_particles):
        print(get_position(config.max_distance))
    print("\nVelocities:")
    print("-------------------------------------------")
    for i in range(config.number_of_particles):
        print(get_velocity(config.max_speed))



def main():
    result_printer(4, 10, 3)

if __name__ == "__main__":
    main()