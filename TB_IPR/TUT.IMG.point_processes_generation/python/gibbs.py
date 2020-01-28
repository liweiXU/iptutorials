# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 10:42:32 2016

@author: Yann GAVET @ Mines Saint-Etienne
"""
import numpy as np
import matplotlib.pyplot as plt
import spat_pp
from scipy.spatial.distance import pdist


def exampleEnergyFunction(distance):
    """ This function returns e with the same size as distance
    e takes the value given in the variable energy according to the steps

    Regular energy function
    """
    e = np.zeros(distance.shape)
    e[distance < 10] = 10
    return e


def agregatedEnergyFunction(distance):
    """ This function returns e with the same size as distance
    e takes the value given in the variable energy according to the steps

    Agregated energy function
    """
    e = np.zeros(distance.shape)
    e[distance < 2] = 50
    e[np.logical_and(distance >= 2, distance < 5)] = -10
    e[np.logical_and(distance >= 5, distance < 10)] = 5

    return e


def energy(P, eFunction=exampleEnergyFunction):
    """
    This computes the energy in the set of points P, with the energy function
    given as a parameter.
    return a float value
    """
    P = np.transpose(P)
    d = pdist(P)
    e = exampleEnergyFunction(d)
    return np.sum(e)


def energyFromPoint(p, P, eFunction=exampleEnergyFunction):
    """
    Compute energy from point p to all points of P
    """
    dist = np.sqrt((p[0] - P[0, :])**2 + (p[1] - P[1, :])**2)
    ee = eFunction(dist)
    return np.sum(ee)


def gibbs(nb_points, xmin, xmax, ymin, ymax, nbiter, eFunction=exampleEnergyFunction):
    """
    Gibbs point process
    xmin, xmax, ymin, ymax represents the spatial window
    nb_points: number of generated points
    nbiter: number of iterations
    returns (x,y) coordinates of the points
    """

    # start with a Poisson Point Process
    x, y = spat_pp.cond_Poisson(nb_points, xmin, xmax, ymin, ymax)
    nb_moves = 0
    e_prev = energy(np.vstack((x, y)), eFunction)
    print("initial energy: {0:f}".format(e_prev))

    for i in range(nbiter):
        # choose a random point
        j = np.random.randint(0, nb_points)
        x2 = np.delete(x, j)
        y2 = np.delete(y, j)

        P = np.vstack((x2, y2))
        e1 = energyFromPoint([x[j], y[j]], P, eFunction)

        for m in range(10):
            xm, ym = spat_pp.cond_Poisson(1, xmin, xmax, ymin, ymax)

            e2 = energyFromPoint([xm, ym], P, eFunction)
            if e2 < e1:
                nb_moves += 1
                x[j] = xm
                y[j] = ym
                e1 = e2

    print("Number of moves: " + str(nb_moves))
    print("Final energy:    " + str(e1))
    return x, y


def test_gibbs():
    N = 100
    x, y = gibbs(N, 0, 100, 0, 100, 1000, eFunction=agregatedEnergyFunction)
    print("final energy: " + str(energy((x, y))))
    plt.figure()
    plt.plot(x, y, 'o')
    plt.show()

# test_gibbs();