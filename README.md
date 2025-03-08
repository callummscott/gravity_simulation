
# File contents:
- `n_body_oop.py`:
    - main program that, when run, generates static 3D pyplot of gravitational particle simulation
    - name derives from past experiments when deciding between functional or object-oriented approach
- `config.py`:
    - stores general data to be refined by user, as well as derived variables, about simulation (e.g. randomised inputs, value of G, ...)
- `particle_setup.py`:
    - either uses user-defined intial particle qualities (e.g. velocity, position, mass) or generates randomised (seeded) inputs 
- `colours.json`:
    - simply stores 16 notably-distinct colours to be *uniquely* used by each of the particles
- `sim.log`:
    - stores the `logging` outputs of the files, *logging level* and other settings defined in `config.py` 
