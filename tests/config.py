from logging import getLogger, basicConfig, DEBUG

class TestConfig:
    __test__ = False
    
    def __init__(self):
        self.G = 100
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