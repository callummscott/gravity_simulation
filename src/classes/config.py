""" Class used to read both user-defined settings and derived variables useful for the simulation. """

from yaml import safe_load
from logging import getLogger, basicConfig, INFO


class Config:
    """ Class containing useful values and accessing user-defined variables """

    def __init__(self, config_filename : str = ".config/config.yaml", output_filename: str = "sim.log") -> None:
        
        with open(config_filename, 'r') as config_file:
            config = safe_load(config_file)

        self.random_seed = config['random_seed']
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
            filename=output_filename,
            level=INFO,
            format=self.logging['format'],
            datefmt=self.logging['datefmt'],
            filemode="w"
        ) 

    @property
    def simple_log_rate(self) -> int:
        return self._simple_log_rate
    
    @simple_log_rate.setter
    def simple_log_rate(self, value):
        raise ValueError("Cannot change simple_log_rate.")

    @property
    def total_plot_points(self) -> int:
        return self._total_plot_points

    @total_plot_points.setter
    def total_plot_points(self, value: int) -> int:
        if (not isinstance(value, int)) or (value <= 0):
            raise ValueError("Plot points must be a positive integer.")

        max_points = self.number_of_particles * self.timesteps
        if value > max_points:
            print(f"Warning: Too many plot points, reducing to maximum allowed: {max_points:,}.")
            self._total_plot_points = max_points
        else:
            self._total_plot_points = value


CFG = Config()
