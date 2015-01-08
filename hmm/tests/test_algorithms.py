import hmm.algorithms
import hmm.models
import unittest
import numpy
import hmm.kernel.python


class TestBaumWelchMultiple(unittest.TestCase):

    def test_if_same_as_baum_welch_after_one_step(self):
        ob = [ 1, 1, 0, 1, 1, 0, 0, 1, 1 ]
        A, B, pi = hmm.models.get_models()['equi32']

        A1, B1, pi1, prob1, it1 = hmm.algorithms.baum_welch(
                ob, A, B, pi, maxit=1, kernel=hmm.kernel.python)
        A2, B2, pi2, prob2, it2 = hmm.algorithms.baum_welch_multiple(
                [ob], A, B, pi, maxit=1, kernel=hmm.kernel.python)

        numpy.testing.assert_almost_equal(A1,A2,6)
        numpy.testing.assert_almost_equal(B1,B2,6)
        numpy.testing.assert_almost_equal(it1,it2)


class TestBaumWelch(unittest.TestCase):

    def test_if_it_even_runs(self):
        ob = [ 1, 1, 0, 1 ]
        A, B, pi = hmm.models.get_models()['equi32']
        A, B, pi, eps, it = hmm.algorithms.baum_welch(ob, A, B, pi)
        self.assertTrue(it > 0)

if __name__ == '__main__':
    unittest.main()