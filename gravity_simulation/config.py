""" File containing user-defined settings for simulation, along with some useful derived values. """
import logging
from random import seed
from yaml import safe_load

class Config:

    def __init__(self, output_file="sim.log"):
        
        with open("gravity_simulation/config.yaml", 'r') as config_file:
            config = safe_load(config_file)

        self.random_inputs = config['random_inputs']
        self.seed          = config['seed']
        self.max_mass      = config['max_mass']
        self.max_distance  = config['max_distance']
        self.max_speed     = config['max_speed']

        self.G                   = config['G']
        self.number_of_particles = config['number_of_particles']
        self.timestep            = config['timestep']
        self.maximum_time        = config['maximum_time']
        self.collision_distance  = config['collision_distance']

        self.total_points_number = config['total_points_number']
        self.logging             = config['Logging info']

        self.half_dtsq       = self.timestep**2 / 2
        self.number_of_steps = int(self.maximum_time/self.timestep)
        self.number_of_calcs = self.number_of_steps*self.number_of_particles
        self.simple_log_rate = int(self.maximum_time / (self.total_points_number * self.timestep))

        log_cfg = config['Logging info']
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=output_file, level=logging.INFO, format=log_cfg['format'], datefmt=log_cfg['datefmt'], filemode="w")

        seed(self.seed)
