""" Retrives and sets up initial particle data from `particle_setup`, iteratively calculates and logs particle motion for defined period converts positional data to (x,y,z) coordinates and plots results in 3D  """

from time import time
from numpy.linalg import norm
from gravity_simulation.classes.config import Config
from gravity_simulation.simulation import *
from gravity_simulation.plotter import *

from gravity_simulation.simulation import get_distance_matrix # Testing


CONFIG = Config()

def calculate_energy_of_particles(particles: dict):
    total_energy = 0
    for id in particles:
        particle = particles[id]
        particle_mass = particle.mass
        particle_velocity = particle.velocity
        distances = get_distance_matrix(particles)

        kinetic_energy = .5*particle_mass*norm(particle_velocity)**2
        potential_energy = 0
        for other_id in particles:
            if other_id != id:
                other_particle = particles[other_id]
                potential_energy += CONFIG.G*particle.mass*other_particle.mass / distances[id, other_id]
        
        total_energy += kinetic_energy + potential_energy
    return total_energy


def main():

    start_time = time()

    particles = initialise_random_particles(
        n            = CONFIG.number_of_particles,
        max_mass     = CONFIG.max_mass,
        max_distance = CONFIG.max_distance,
        max_speed    = CONFIG.max_speed
    )
    CONFIG.logger.info("Particles initialised")

    position_logs = { id: PositionLog() for id in particles }
    for i in range(CONFIG.number_of_steps):
        # CONFIG.logger.info(f"Step: {i}")
        particles = collision_handler(particles)
        position_logs = get_updated_position_logs(position_logs, particles)
        particles = get_next_particle_states(particles)

    plot_data = get_filtered_xyz_values(position_logs)

    for finish_time in plot_results_3d(plot_data): # Yields the `finish_time` before the plot is closed by the user.
        total_time = finish_time - start_time
        print(f"Total runtime: {total_time:.2f}s")

    

if __name__ == "__main__":
    main()