


""" Config for simulation file """
G = 0.005

number_of_particles = 5
timestep = 1/1000 #s
maximum_time = 100 #s
pov_particle = 3
total_points_number = 10_000

half_dtsq = .5*timestep**2
number_of_steps = int(maximum_time/timestep)
simple_log_rate = int(maximum_time/(total_points_number*timestep))


""" Config specifically for 'random_coords.py' file"""
random_inputs = True
random_seed  = 'betterthanthat'
max_mass     = 100_000
max_distance = 100
max_speed    = 1


def main():
    ...

if __name__ == "__main__":
    main()