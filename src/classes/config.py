""" Class used to read both user-defined settings and derived variables useful for the simulation. """

from yaml import safe_load
from logging import getLogger, basicConfig, INFO


class Config:
    """ Class containing useful values and accessing user-defined variables """

    def __init__(self, output_file="sim.log"):
        
        with open("src/config.yaml", 'r') as config_file:
            config = safe_load(config_file)

        self.random_inputs = config['random_inputs']
        self.seed          = config['seed']
        self.max_mass      = config['max_mass']
        self.max_distance  = config['max_distance']
        self.max_speed     = config['max_speed']

        self.G                   = config['G']
        self.dt                  = config['dt']
        self.timesteps           = config['timesteps']
        self.collision_distance  = config['collision_distance']
        self.number_of_particles = config['number_of_particles']

        self.half_dtsq            = .5*self.dt**2
        self.logging              = config['Logging info']

        self._total_plot_points   = config['total_plot_points']
        self._simple_log_rate     = int(self.number_of_particles *  self.timesteps / self.total_plot_points)

        self.logger = getLogger(__name__)
        basicConfig(
            filename=output_file,
            level=INFO,
            format=self.logging['format'],
            datefmt=self.logging['datefmt'],
            filemode="w"
        ) 

    @property
    def simple_log_rate(self):
        return self._simple_log_rate
    
    @simple_log_rate.setter
    def simple_log_rate(self, value):
        raise ValueError("Cannot change simple_log_rate.")

    @property
    def total_plot_points(self):
        return self._total_plot_points

    @total_plot_points.setter
    def total_plot_points(self, value):
        max_points = self.number_of_particles * self.timesteps
        if value > max_points:
            print(f"Warning: Too many plot points, reducing to maximum allowed: {max_points:,}.")
            self._total_plot_points = max_points
        else:
            self._total_plot_points = value


CFG = Config()
