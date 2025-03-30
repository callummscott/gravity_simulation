""" Module for executing n-body gravity simulation and plotting its results in 3D. """

from src.classes.config import CFG
from src.energy import print_gravitational_boundedness
from src.plotter import log_positions, plot_logs
from src.motion_calcs import initialise_particles, simulate_timestep
from src.particle_setup import get_configured_particles


def main():
    particles = get_configured_particles(CFG)

    print_gravitational_boundedness(particles)
    
    CFG.logger.info("'Running main.'")
    position_logs = { ptcl.id: list() for ptcl in particles }
    position_logs = log_positions(particles, position_logs)
    initialise_particles(particles)
    for i in range(CFG.timesteps + 1):
        CFG.logger.info(f"'Running timestep' #{i}.")
        simulate_timestep(particles)
        if i % CFG.simple_log_rate == 0:
            CFG.logger.info(f"Logging updated positions: {[ptcl.position for ptcl in particles]}")
            position_logs = log_positions(particles, position_logs)
    
    plot_logs(position_logs)

if __name__ == "__main__":
    main()
