""" Module for abbrevating data structures found throughout the gravity simulation. """

from numpy import ndarray, float64
from src.classes.particle import Particle

Particles = list[Particle]
IdCollection = list[set[int]]
PositionLog = dict[int, list]
IdPairVectorDict = dict[tuple[int,int], ndarray]
IdPairFloatDict = dict[tuple[int,int],float64]
