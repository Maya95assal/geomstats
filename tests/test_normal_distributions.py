"""Unit tests for the manifold of normal distributions."""

import warnings

from scipy.stats import norm

import geomstats.backend as gs
import geomstats.tests
from geomstats.geometry.normal_distributions import FisherRaoMetric
from geomstats.geometry.normal_distributions import NormalDistributions


class TestNormalDistributions(geomstats.tests.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore', category=UserWarning)
        self.normal = NormalDistributions()
        self.metric = FisherRaoMetric()
        self.n_samples = 10
        self.dim = self.normal.dim

    def test_random_uniform_and_belongs(self):
        """Test random_uniform and belongs.

        Test that the random uniform method samples
        on the normal distribution space.
        """
        point = self.normal.random_uniform()
        result = self.normal.belongs(point)
        expected = True
        self.assertAllClose(expected, result)

    def test_random_uniform_and_belongs_vectorization(self):
        """Test random_uniform and belongs.

        Test that the random uniform method samples
        on the normal distribution space.
        """
        n_samples = self.n_samples
        point = self.normal.random_uniform(n_samples)
        result = self.normal.belongs(point)
        expected = gs.array([True] * n_samples)
        self.assertAllClose(expected, result)

    def test_random_uniform(self):
        """Test random_uniform.

        Test that the random uniform method samples points of the right shape
        """
        point = self.normal.random_uniform(self.n_samples)
        self.assertAllClose(gs.shape(point), (self.n_samples, self.dim))

    def test_sample(self):
        """Test samples."""
        n_points = self.n_samples
        n_samples = 100
        points = self.normal.random_uniform(n_points)
        samples = self.normal.sample(points, n_samples)
        result = samples.shape
        expected = (n_points, n_samples)

        self.assertAllClose(result, expected)

    def test_point_to_pdf(self):
        """Test point_to_pdf

        Check vectorization of the computation of the pdf.
        """
        point = self.normal.random_uniform(n_samples=2)
        pdf = self.normal.point_to_pdf(point)
        x = gs.linspace(0.0, 1.0, 10)
        result = pdf(x)
        pdf1 = norm.pdf(x, loc=point[0, 0], scale=point[0, 1])
        pdf2 = norm.pdf(x, loc=point[1, 0], scale=point[1, 1])
        expected = gs.stack([gs.array(pdf1), gs.array(pdf2)], axis=1)

        self.assertAllClose(result, expected)
