import numpy as np

class Map(object):

    def __init__(self, mapfile):
        with open(mapfile) as f:
            self.tileschar = np.array([list(line) for line in f.read().splitlines()]).transpose()
