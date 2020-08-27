"""The n-dimensional hyperbolic space.

Poincare half-space representation.
"""

import geomstats.backend as gs
from geomstats.geometry.hyperbolic import Hyperbolic
from geomstats.geometry.poincare_ball import PoincareBall
from geomstats.geometry.riemannian_metric import RiemannianMetric


class PoincareHalfSpace(Hyperbolic):
    """Class for the n-dimensional hyperbolic space.

    Class for the n-dimensional hyperbolic space
    as embedded in the Poincaré half space model.

    Parameters
    ----------
    dim : int
        Dimension of the hyperbolic space.
    scale : int, optional
        Scale of the hyperbolic space, defined as the set of points
        in Minkowski space whose squared norm is equal to -scale.
    """

    default_coords_type = 'half-space'
    default_point_type = 'vector'

    def __init__(self, dim, scale=1):
        super(PoincareHalfSpace, self).__init__(
            dim=dim,
            scale=scale)
        self.coords_type = PoincareHalfSpace.default_coords_type
        self.point_type = PoincareHalfSpace.default_point_type
        self.metric = PoincareHalfSpaceMetric(self.dim, self.scale)

    def belongs(self, point):
        """Test if a point belongs to the hyperbolic space.

        Test if a point belongs to the hyperbolic space based on
        the poincare ball representation.

        Parameters
        ----------
        point : array-like, shape=[..., dim]
            Point to be tested.

        Returns
        -------
        belongs : array-like, shape=[...,]
            Array of booleans indicating whether the corresponding points
            belong to the hyperbolic space.
        """
        point = gs.to_ndarray(point, 2)
        return point[:, -1] > 0


class PoincareHalfSpaceMetric(RiemannianMetric):

    default_point_type = 'vector'
    default_coords_type = 'half-space'

    def __init__(self, dim, scale=1):
        super(PoincareHalfSpaceMetric, self).__init__(
            dim=dim,
            signature=(dim, 0, 0))
        self.coords_type = PoincareHalfSpace.default_coords_type
        self.point_type = PoincareHalfSpace.default_point_type
        self.scale = scale
        self.poincare_ball = PoincareBall(dim=dim, scale=scale)

    def half_space_to_ball_coordinates(self, point):
        """Convert a point from Poincare half space to Poincare ball
        coordinates.
        """
        point = gs.to_ndarray(point, 2)
        den = 1 + gs.linalg.norm(point)**2 + 2 * point[:, -1]
        component_1 = 2 * point[:, :-1] / den
        component_2 = (gs.linalg.norm(point)**2 - 1) / den
        point_ball = gs.hstack([component_1, gs.to_ndarray(component_2, 2)])
        return gs.squeeze(point_ball)

    def ball_to_half_space_coordinates(self, point):
        """Convert a point from Poincare ball to Poincare half space
        coordinates.
        """
        point = gs.to_ndarray(point, 2)
        den = 1 + gs.linalg.norm(point)**2 - 2 * point[:, -1]
        component_1 = 2 * point[:, :-1] / den
        component_2 = (1 - gs.linalg.norm(point)**2) / den
        point_half_space = gs.hstack(
            [component_1, gs.to_ndarray(component_2, 2)])
        return gs.squeeze(point_half_space)

    def half_space_to_ball_tangent(self, tangent_vec, base_point):
        """Convert a tangent vector at base point from Poincare half space
        to Poincare ball coordinates.
        """
        base_point = gs.to_ndarray(base_point, 2)
        tangent_vec = gs.to_ndarray(tangent_vec, 2)
        den = 1 + gs.linalg.norm(base_point)**2 + 2 * base_point[:, -1]
        scalar_prod = gs.sum(base_point * tangent_vec, 1)
        component_1 = 2 * tangent_vec[:, :-1] / den - 4 * base_point[:, :-1]\
            / den**2 * (scalar_prod + tangent_vec[:, -1])
        component_2 = 2 * scalar_prod / den - 2 * (
            gs.linalg.norm(base_point)**2 - 1) / den**2 * (
            scalar_prod + tangent_vec[:, -1])
        tangent_vec_ball = gs.hstack(
            [component_1, gs.to_ndarray(component_2, 2)])
        return gs.squeeze(tangent_vec_ball)

    def ball_to_half_space_tangent(self, tangent_vec, base_point):
        """Convert a tangent vector at base point from Poincare ball to
        Poincare half space coordinates.
        """
        base_point = gs.to_ndarray(base_point, 2)
        tangent_vec = gs.to_ndarray(tangent_vec, 2)
        den = 1 + gs.linalg.norm(base_point)**2 - 2 * base_point[:, -1]
        scalar_prod = gs.sum(base_point * tangent_vec, 1)
        component_1 = 2 * tangent_vec[:, :-1] / den - 4 * base_point[:, :-1]\
            / den**2 * (scalar_prod - tangent_vec[:, -1])
        component_2 = -2 * scalar_prod / den - 2 * (
            1 - gs.linalg.norm(base_point)**2) / den**2 * (
            scalar_prod - tangent_vec[:, -1])
        tangent_vec_half_space = gs.hstack(
            [component_1, gs.to_ndarray(component_2, 2)])
        return gs.squeeze(tangent_vec_half_space)

    def exp(self, tangent_vec, base_point):
        """Compute the Riemannian exponential of a tangent vector at
        a base point.
        """
        base_point_ball = self.half_space_to_ball_coordinates(
            base_point)
        tangent_vec_ball = self.half_space_to_ball_tangent(
            tangent_vec, base_point)
        end_point_ball = self.poincare_ball.metric.exp(
            tangent_vec_ball, base_point_ball)
        end_point = self.ball_to_half_space_coordinates(
            end_point_ball)
        return end_point
