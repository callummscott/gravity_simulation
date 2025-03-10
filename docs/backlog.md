
# Just some ideas for future features/improvements

- Focus on implementing a 2D animated image of events from a chosen 'POV' particle, 
  choosing an arbitary view direction -- i.e. to begin with at least
    - Requires some pretty intense understanding of rotation matrices or quaternions...
- Focus on getting the 'scale' of the values, converting distances to 'AU', time to
    months, and mass to'Earth masses' units instead of the current nonsense values
    -- mainly a mathsy, cerebral process
    - Then actually implement solar-system accurate values for the simulation
- Implementing a loading bar to display how far along the simulation is
- Handle 'collisions' between particles -- thought it wasn't going to be common but is
- Add some `logging` functionality to the whole thing
- **Provide an estimation for the time to simulate given the input criteria**
- Warn the user about the ranges of specific inputs, if particles will escape,
    or if particles are likely to collide, maybe
- Randomly generate particles with different density distributions, i.e. not just randomly distributed throughout a uniform cube, but maybe a torus, a sphere, a spherical shell, etc.
