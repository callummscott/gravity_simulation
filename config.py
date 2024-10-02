""" File containing user-defined settings for simulation, along with some useful derived values. """
import logging

# Config specifically for 'random_coords.py' file
random_inputs = True
random_seed  = 'betterthanthat'
max_mass     = 100_000
max_distance = 100
max_speed    = 1

# Values for refining the simulation
G = 0.005
number_of_particles = 3
timestep = 1 / 1_000 #s
maximum_time = 100 #s
pov_particle = 3
total_points_number = 10_000


### Calculated values from the settings above ###
half_dtsq = .5*timestep**2
number_of_steps = int(maximum_time/timestep)
number_of_calcs = number_of_steps*number_of_particles
simple_log_rate = int(maximum_time/(total_points_number*timestep))

#Logging settings
logging_format = '%(asctime)s [%(levelname)s] %(module)s > %(funcName)s: %(message)s'
for_logging = logging.basicConfig(
    format=logging_format,
    filename='sim.log',
    level=logging.INFO,
    datefmt='%I:%M:%S',
    filemode='w'
)