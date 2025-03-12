""" Retrives and sets up initial particle data from `particle_setup`, iteratively calculates and logs particle motion for defined period converts positional data to (x,y,z) coordinates and plots results in 3D  """

from time import time
from src.classes.config import Config

from src.plotter import *
from particle_setup import initialise_random_particles
from src.simulation import collision_handler, get_updated_position_logs, get_next_particle_states


CONFIG = Config()


def main():

    start_time = time()
    print("Starting simulation...")

    particles = initialise_random_particles(
        n            = CONFIG.number_of_particles,
        max_mass     = CONFIG.max_mass,
        max_distance = CONFIG.max_distance,
        max_speed    = CONFIG.max_speed
    )
    CONFIG.logger.info("Particles initialised")

    position_logs = { id: PositionLog() for id in particles }
    for i in range(CONFIG.number_of_steps): #* `i` reserved for logging, don't delete
        particles = collision_handler(particles)
        position_logs = get_updated_position_logs(position_logs, particles)
        particles = get_next_particle_states(particles)

    print("Simulation complete.")
    print("Processing position data...")
    plot_data = get_filtered_xyz_values(position_logs)

    for finish_time in plot_results_3d(plot_data): # Yields the `finish_time` before the plot is closed by the user.
        total_time = finish_time - start_time
        print(f"Total runtime: {total_time:.2f}s")

    
if __name__ == "__main__":
    main()