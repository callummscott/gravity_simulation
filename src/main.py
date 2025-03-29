""" Retrives and sets up initial particle data from `particle_setup`, iteratively calculates and logs particle motion for defined period converts positional data to (x,y,z) coordinates and plots results in 3D  """

from time import time
from src.classes.config import CFG

from src.plotter import *
from src.particle_setup import get_configured_particles
from src.simulation import collision_handler, get_updated_position_logs, get_next_particle_states, calculate_and_assign_accelerations



def main():

    start_time = time()
    print("Starting simulation...", end="\r")

    particles = get_configured_particles()

    position_logs = { particle.id: PositionLog() for particle in particles }
    particles = collision_handler(particles)
    calculate_and_assign_accelerations(particles)
    for i in range(CFG.number_of_steps): #* `i` reserved for logging, don't delete
        particles = collision_handler(particles)
        position_logs = get_updated_position_logs(position_logs, particles)
        particles = get_next_particle_states(particles)

    print("\x1b[2K", end="\r")
    print("Simulation complete.")
    print("Processing position data...", end="\r")
    plot_data = get_filtered_xyz_values(position_logs)

    for finish_time in plot_results_3d(plot_data): # Yields the `finish_time` before the plot is closed by the user.
        total_time = finish_time - start_time
        print(f"Total runtime: {total_time:.2f}s")

    
if __name__ == "__main__":
    main()