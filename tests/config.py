from yaml import safe_load
from logging import getLogger, basicConfig, DEBUG

from src.classes.config import Config



class TestConfig(Config):
    __test__ = False
    
    def __init__(self):
        
        with open("src/config.yaml", "r") as config_file:
            grav_constant = safe_load(config_file)['G']
            self.G = grav_constant
            
        self.number_of_particles = 3
        self.max_mass = 10_000
        self.max_distance = 100_000
        self.max_speed = 100_000
        self.number_of_steps = 1_000

        self.logger = getLogger(__name__)
        basicConfig(
            filename="testing.log",
            level=DEBUG,
            format='%(asctime)s [%(levelname)s] %(module)s > %(funcName)s: %(message)s',
            datefmt='%I:%M:%S',
            filemode="w"
        )