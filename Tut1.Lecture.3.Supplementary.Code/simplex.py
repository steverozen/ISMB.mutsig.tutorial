'''Functions for drawing 2-simplex contours.'''


# Source code adapted from
# https://gist.github.com/agitter/46b2169a035ad25b5d2b024a00344d54, author: Thomas Boggs
# by ferran.muinos@irbbarcelona.org


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from functools import reduce
from scipy.stats import entropy


_corners = np.array([[0, 0], [1, 0], [0.5, 0.75**0.5]])
_triangle = tri.Triangulation(_corners[:, 0], _corners[:, 1])
_midpoints = [(_corners[(i + 1) % 3] + _corners[(i + 2) % 3]) / 2.0 \
              for i in range(3)]


def xy2bc(xy, tol=1.e-3):
    '''Converts 2D Cartesian coordinates to barycentric.
    Arguments:
        `xy`: A length-2 sequence containing the x and y value.
    '''
    s = [(_corners[i] - _midpoints[i]).dot(xy - _midpoints[i]) / 0.75 \
         for i in range(3)]
    return np.clip(s, tol, 1.0 - tol)


class Dirichlet:

    def __init__(self, alpha):
        '''Creates Dirichlet distribution with parameter `alpha`.'''
        from math import gamma
        from operator import mul
        self._alpha = np.array(alpha)
        self._coef = gamma(np.sum(self._alpha)) / \
                     reduce(mul, [gamma(a) for a in self._alpha])
    def pdf(self, x):
        '''Returns pdf value for `x`.'''
        from operator import mul
        return self._coef * reduce(mul, [xx ** (aa - 1)
                                         for (xx, aa)in zip(x, self._alpha)])
    def sample(self, N):
        '''Generates a random sample of size `N`.'''
        return np.random.dirichlet(self._alpha, N)


def draw_pdf_contours(dist, border=False, nlevels=200, subdiv=8, **kwargs):
    '''Draws pdf contours over an equilateral triangle (2-simplex).
    Arguments:
        `dist`: A distribution instance with a `pdf` method.
        `border` (bool): If True, the simplex border is drawn.
        `nlevels` (int): Number of contours to draw.
        `subdiv` (int): Number of recursive mesh subdivisions to create.
        kwargs: Keyword args passed on to `plt.triplot`.
    '''
    from matplotlib import ticker, cm
    import math

    refiner = tri.UniformTriRefiner(_triangle)
    trimesh = refiner.refine_triangulation(subdiv=subdiv)
    pvals = [dist.pdf(xy2bc(xy)) for xy in zip(trimesh.x, trimesh.y)]

    plt.tricontourf(trimesh, pvals, nlevels, **kwargs)
    plt.axis('equal')
    plt.xlim(0, 1)
    plt.ylim(0, 0.75**0.5)
    plt.axis('off')
    if border is True:
        plt.triplot(_triangle, linewidth=1)


def plot_points(X, barycentric=True, border=True, **kwargs):
    '''Plots a set of points in the simplex.
    Arguments:
        `X` (ndarray): A 2xN array (if in Cartesian coords) or 3xN array
                       (if in barycentric coords) of points to plot.
        `barycentric` (bool): Indicates if `X` is in barycentric coords.
        `border` (bool): If True, the simplex border is drawn.
        kwargs: Keyword args passed on to `plt.plot`.
    '''
    if barycentric is True:
        X = X.dot(_corners)
    plt.plot(X[:, 0], X[:, 1], 'k.', ms=1, **kwargs)
    plt.axis('equal')
    plt.xlim(0, 1)
    plt.ylim(0, 0.75**0.5)
    plt.axis('off')
    if border is True:
        plt.triplot(_triangle, linewidth=1)


def plot_dirichlet(alpha):

    plt.ioff()

    dist = Dirichlet(alpha)
    draw_pdf_contours(dist)

    title = r'$\alpha$ = (%.3f, %.3f, %.3f)' % tuple(alpha)
    plt.title(title, fontdict={'fontsize': 12})
    plt.savefig(r'dirichlet_plots_%.3f_%.3f_%.3f.png' % tuple(alpha),
                	dpi=200,
                bbox_inches='tight')


class JensenShannon:

    def __init__(self, alpha):
        self._alpha = np.array(alpha)

    @staticmethod
    def js(x, y):
        m = 0.5 * (x + y)
        return 0.5 * (entropy(x, m) + entropy(y, m))

    def pdf(self, x):
        return self.js(self._alpha, x)


class Cosine:

    def __init__(self, alpha):
        self._alpha = np.array(alpha)

    def pdf(self, x):
        return 1 - abs(np.dot(self._alpha, x)) / (np.linalg.norm(self._alpha) * np.linalg.norm(x))


def plot_similarity(alpha, option='cosine'):

    plt.ioff()

    if option == 'cosine':
        dist = Cosine(alpha)
    else:
        dist = JensenShannon(alpha)
    draw_pdf_contours(dist)

    title = r'$\alpha$ = (%.3f, %.3f, %.3f)' % tuple(alpha)
    plt.title(title, fontdict={'fontsize': 12})
    plt.savefig(r'similarity_%s_plots_%.3f_%.3f_%.3f.png' % tuple([option] + alpha),
                dpi=200,
                bbox_inches='tight')


if __name__ == '__main__':

    pass
