from numpy import ndarray, float64
from classes.particle import Particle

Particles = list[Particle]
IdPairVectorDict = dict[tuple[int,int], ndarray]
IdPairFloatDict = dict[tuple[int,int],float64]
IdCollection = list[set[int]]
PositionLog = dict[int, list]
