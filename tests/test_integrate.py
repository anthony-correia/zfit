import math as mt

import pytest
import tensorflow as tf
import numpy as np

from zfit import ztf
from zfit.core import basepdf as zbasepdf
import zfit.core.integrate as zintegrate
from zfit.core.limits import Range
import zfit.core.math as zmath
from zfit.core.parameter import FitParameter
from zfit.pdfs.basic import Gauss

limits1_5deps = [(1., -1., 2., 4., 3.), (5., 4., 5., 8., 9.)]
# limits_simple_5deps = (0.9, 4.7)
limits_simple_5deps = [(1., -1., -5., 3.4, 2.1), (5., 5.4, -1.1, 7.6, 3.5)]


def func1_5deps(x):
    a, b, c, d, e = tf.unstack(x)
    return a + b * c ** 2 + d ** 2 * e ** 3


def func1_5deps_fully_integrated(limits):
    lower, upper = limits
    a_lower, b_lower, c_lower, d_lower, e_lower = lower
    a_upper, b_upper, c_upper, d_upper, e_upper = upper

    val = -e_lower ** 4 * (
        a_lower * b_lower * c_lower * d_lower ** 3 / 12 - a_lower * b_lower * c_lower *
        d_upper ** 3 / 12 - a_lower * b_lower * c_upper * d_lower ** 3 / 12 + a_lower *
        b_lower * c_upper * d_upper ** 3 / 12 - a_lower * b_upper * c_lower * d_lower **
        3 / 12 + a_lower * b_upper * c_lower * d_upper ** 3 / 12 + a_lower * b_upper *
        c_upper * d_lower ** 3 / 12 - a_lower * b_upper * c_upper * d_upper ** 3 / 12 -
        a_upper * b_lower * c_lower * d_lower ** 3 / 12 + a_upper * b_lower * c_lower *
        d_upper ** 3 / 12 + a_upper * b_lower * c_upper * d_lower ** 3 / 12 - a_upper *
        b_lower * c_upper * d_upper ** 3 / 12 + a_upper * b_upper * c_lower * d_lower **
        3 / 12 - a_upper * b_upper * c_lower * d_upper ** 3 / 12 - a_upper * b_upper *
        c_upper * d_lower ** 3 / 12 + a_upper * b_upper * c_upper * d_upper ** 3 / 12) - \
          e_lower * (
              a_lower ** 2 * b_lower * c_lower * d_lower / 2 - a_lower ** 2 * b_lower *
              c_lower * d_upper / 2 - a_lower ** 2 * b_lower * c_upper * d_lower / 2 +
              a_lower ** 2 * b_lower * c_upper * d_upper / 2 - a_lower ** 2 * b_upper *
              c_lower * d_lower / 2 + a_lower ** 2 * b_upper * c_lower * d_upper / 2 +
              a_lower ** 2 * b_upper * c_upper * d_lower / 2 - a_lower ** 2 * b_upper *
              c_upper * d_upper / 2 + a_lower * b_lower ** 2 * c_lower ** 3 * d_lower / 6
              - a_lower * b_lower ** 2 * c_lower ** 3 * d_upper / 6 - a_lower * b_lower
              ** 2 * c_upper ** 3 * d_lower / 6 + a_lower * b_lower ** 2 * c_upper ** 3 *
              d_upper / 6 - a_lower * b_upper ** 2 * c_lower ** 3 * d_lower / 6 + a_lower
              * b_upper ** 2 * c_lower ** 3 * d_upper / 6 + a_lower * b_upper ** 2 *
              c_upper ** 3 * d_lower / 6 - a_lower * b_upper ** 2 * c_upper ** 3 *
              d_upper / 6 - a_upper ** 2 * b_lower * c_lower * d_lower / 2 + a_upper ** 2
              * b_lower * c_lower * d_upper / 2 + a_upper ** 2 * b_lower * c_upper *
              d_lower / 2 - a_upper ** 2 * b_lower * c_upper * d_upper / 2 + a_upper ** 2
              * b_upper * c_lower * d_lower / 2 - a_upper ** 2 * b_upper * c_lower *
              d_upper / 2 - a_upper ** 2 * b_upper * c_upper * d_lower / 2 + a_upper ** 2
              * b_upper * c_upper * d_upper / 2 - a_upper * b_lower ** 2 * c_lower ** 3 *
              d_lower / 6 + a_upper * b_lower ** 2 * c_lower ** 3 * d_upper / 6 + a_upper
              * b_lower ** 2 * c_upper ** 3 * d_lower / 6 - a_upper * b_lower ** 2 *
              c_upper ** 3 * d_upper / 6 + a_upper * b_upper ** 2 * c_lower ** 3 *
              d_lower / 6 - a_upper * b_upper ** 2 * c_lower ** 3 * d_upper / 6 - a_upper
              * b_upper ** 2 * c_upper ** 3 * d_lower / 6 + a_upper * b_upper ** 2 *
              c_upper ** 3 * d_upper / 6) + e_upper ** 4 * (
              a_lower * b_lower * c_lower * d_lower ** 3 / 12 - a_lower * b_lower *
              c_lower * d_upper ** 3 / 12 - a_lower * b_lower * c_upper * d_lower ** 3 /
              12 + a_lower * b_lower * c_upper * d_upper ** 3 / 12 - a_lower * b_upper *
              c_lower * d_lower ** 3 / 12 + a_lower * b_upper * c_lower * d_upper ** 3 /
              12 + a_lower * b_upper * c_upper * d_lower ** 3 / 12 - a_lower * b_upper *
              c_upper * d_upper ** 3 / 12 - a_upper * b_lower * c_lower * d_lower ** 3 /
              12 + a_upper * b_lower * c_lower * d_upper ** 3 / 12 + a_upper * b_lower *
              c_upper * d_lower ** 3 / 12 - a_upper * b_lower * c_upper * d_upper ** 3 /
              12 + a_upper * b_upper * c_lower * d_lower ** 3 / 12 - a_upper * b_upper *
              c_lower * d_upper ** 3 / 12 - a_upper * b_upper * c_upper * d_lower ** 3 /
              12 + a_upper * b_upper * c_upper * d_upper ** 3 / 12) + e_upper * (
              a_lower ** 2 * b_lower * c_lower * d_lower / 2 - a_lower ** 2 * b_lower *
              c_lower * d_upper / 2 - a_lower ** 2 * b_lower * c_upper * d_lower / 2 +
              a_lower ** 2 * b_lower * c_upper * d_upper / 2 - a_lower ** 2 * b_upper *
              c_lower * d_lower / 2 + a_lower ** 2 * b_upper * c_lower * d_upper / 2 +
              a_lower ** 2 * b_upper * c_upper * d_lower / 2 - a_lower ** 2 * b_upper *
              c_upper * d_upper / 2 + a_lower * b_lower ** 2 * c_lower ** 3 * d_lower / 6
              - a_lower * b_lower ** 2 * c_lower ** 3 * d_upper / 6 - a_lower * b_lower
              ** 2 * c_upper ** 3 * d_lower / 6 + a_lower * b_lower ** 2 * c_upper ** 3 *
              d_upper / 6 - a_lower * b_upper ** 2 * c_lower ** 3 * d_lower / 6 + a_lower *
              b_upper ** 2 * c_lower ** 3 * d_upper / 6 + a_lower * b_upper ** 2 * c_upper **
              3 * d_lower / 6 - a_lower * b_upper ** 2 * c_upper ** 3 * d_upper / 6 - a_upper
              ** 2 * b_lower * c_lower * d_lower / 2 + a_upper ** 2 * b_lower * c_lower *
              d_upper / 2 + a_upper ** 2 * b_lower * c_upper * d_lower / 2 - a_upper ** 2 *
              b_lower * c_upper * d_upper / 2 + a_upper ** 2 * b_upper * c_lower * d_lower /
              2 - a_upper ** 2 * b_upper * c_lower * d_upper / 2 - a_upper ** 2 * b_upper *
              c_upper * d_lower / 2 + a_upper ** 2 * b_upper * c_upper * d_upper / 2 -
              a_upper * b_lower ** 2 * c_lower ** 3 * d_lower / 6 + a_upper * b_lower ** 2 *
              c_lower ** 3 * d_upper / 6 + a_upper * b_lower ** 2 * c_upper ** 3 * d_lower /
              6 - a_upper * b_lower ** 2 * c_upper ** 3 * d_upper / 6 + a_upper * b_upper **
              2 * c_lower ** 3 * d_lower / 6 - a_upper * b_upper ** 2 * c_lower ** 3 *
              d_upper / 6 - a_upper * b_upper ** 2 * c_upper ** 3 * d_lower / 6 + a_upper *
              b_upper ** 2 * c_upper ** 3 * d_upper / 6)
    return val


limits2 = (-1., 2.)


def func2_1deps(x):
    a = x
    return a ** 2


def func2_1deps_fully_integrated(limits):
    lower, upper = limits

    def func_int(x):
        return (1 / 3) * x ** 3

    return func_int(upper) - func_int(lower)


limits3 = [(-1., -4.3), (2.3, -1.2)]


def func3_2deps(x):
    a, b = tf.unstack(x)
    return a ** 2 + b ** 2


def func3_2deps_fully_integrated(limits, params=None):
    lower, upper = limits.get_boundaries()
    # print("DEBUG": lower, upper", lower, upper)
    lower_a, lower_b = lower[0]
    upper_a, upper_b = upper[0]
    integral = (lower_a ** 3 - upper_a ** 3) * (lower_b - upper_b)
    integral += (lower_a - upper_a) * (lower_b ** 3 - upper_b ** 3)
    integral /= 3
    return integral


limits4_2dim = [(-4., 1.), (-1., 4.5)]
limits4_1dim = (-2., 3.)

func4_values = np.array([-12., -4.5, 1.9, 4.1])
func4_2values = np.array([[-12., -4.5, 1.9, 4.1], [-11., 3.2, 7.4, -0.3]])


# func4_2values = np.array([[-12., -12],
#                           [-4.5, -4.5],
#                           [1.9, 1.9],
#                           [4.1, 4.1]])


def func4_3deps(x):
    # a, b, c = tf.unstack(x)
    a, b, c = x
    return a ** 2 + b ** 3 + 0.5 * c


def func4_3deps_0and2_integrated(x, limits):
    b = x
    lower, upper = limits
    a_lower, c_lower = lower
    a_upper, c_upper = upper
    integral = -c_lower ** 2 * (-0.25 * a_lower + 0.25 * a_upper) - c_lower * (
        -0.333333333333333 * a_lower ** 3 - 1.0 * a_lower * b ** 3 + 0.333333333333333 *
        a_upper ** 3 + 1.0 * a_upper * b ** 3) + c_upper ** 2 * (
                   -0.25 * a_lower + 0.25 * a_upper) + c_upper * (
                   -0.333333333333333 * a_lower ** 3 - 1.0 * a_lower * b ** 3 + 0.333333333333333
                   * a_upper
                   ** 3 + 1.0 * a_upper * b ** 3)

    return integral


def func4_3deps_1_integrated(x, limits):
    a, c = x
    b_lower, b_upper = limits

    integral = -0.25 * b_lower ** 4 - b_lower * (
        1.0 * a ** 2 + 0.5 * c) + 0.25 * b_upper ** 4 + b_upper * (1.0 * a ** 2 + 0.5 * c)
    return integral


# @pytest.mark.parametrize


def test_mc_integration():
    # simpel example
    num_integral = zintegrate.mc_integrate(func=func1_5deps,
                                           limits=Range.from_boundaries(*limits_simple_5deps,
                                                                        dims=tuple(range(5))),
                                           n_dims=5,
                                           draws_per_dim=5)
    num_integral2 = zintegrate.mc_integrate(func=func2_1deps,
                                            limits=Range.from_boundaries(*limits2,
                                                                         dims=tuple(range(1))),
                                            n_dims=1)
    num_integral3 = zintegrate.mc_integrate(func=func3_2deps,
                                            limits=Range.from_boundaries(*limits3,
                                                                         dims=tuple(range(2))),
                                            n_dims=2,
                                            draws_per_dim=70)

    with tf.Session() as sess:
        integral = sess.run(num_integral)
        integral2 = sess.run(num_integral2)
        integral3 = sess.run(num_integral3)

        assert not hasattr(integral, "__len__")
        assert not hasattr(integral2, "__len__")
        assert not hasattr(integral3, "__len__")
        assert func1_5deps_fully_integrated(limits_simple_5deps) == pytest.approx(integral,
                                                                                  rel=0.1)
        assert func2_1deps_fully_integrated(limits2) == pytest.approx(integral2, rel=0.03)
        assert func3_2deps_fully_integrated(
            Range.from_boundaries(*limits3, dims=(0, 1))) == pytest.approx(integral3, rel=0.03)


def test_mc_partial_integration():
    num_integral = zintegrate.mc_integrate(x=ztf.convert_to_tensor(func4_values),
                                           func=func4_3deps,
                                           limits=Range.from_boundaries(*limits4_2dim,
                                                                        dims=(0, 2)),
                                           draws_per_dim=70)
    vals_tensor = ztf.convert_to_tensor(func4_2values)
    vals_reshaped = tf.transpose(vals_tensor)
    num_integral2 = zintegrate.mc_integrate(x=vals_reshaped,
                                            func=func4_3deps,
                                            limits=Range.from_boundaries(*limits4_1dim, dims=(1,)),
                                            draws_per_dim=100)

    with tf.Session() as sess:
        integral = sess.run(num_integral)
        integral2 = sess.run(num_integral2)
        # print("DEBUG", values:", sess.run(vals_reshaped))
        assert len(integral) == len(func4_values)
        assert len(integral2) == len(func4_2values[1])
        assert func4_3deps_0and2_integrated(x=func4_values,
                                            limits=limits4_2dim) == pytest.approx(integral,
                                                                                  rel=0.03)

        assert func4_3deps_1_integrated(x=func4_2values,
                                        limits=limits4_1dim) == pytest.approx(integral2, rel=0.03)


def test_analytic_integral():
    class DistFunc3(zbasepdf.BasePDF):
        def _unnormalized_prob(self, x):
            return func3_2deps(x)

    mu_true = 1.4
    sigma_true = 1.8
    limits = -4.3, 1.9
    mu = FitParameter("mu", mu_true, mu_true - 2., mu_true + 7.)
    sigma = FitParameter("sigma", sigma_true, sigma_true - 10., sigma_true + 5.)
    gauss_params1 = Gauss(mu=mu, sigma=sigma, name="gauss_params1")
    try:
        infinity = mt.inf
    except AttributeError:  # py34
        infinity = float('inf')
    gauss_integral_infs = gauss_params1.integrate(limits=(-infinity, infinity))

    DistFunc3.register_analytic_integral(func=func3_2deps_fully_integrated,
                                         limits=Range.from_boundaries(*limits3, dims=(0, 1)), dims=None)

    dist_func3 = DistFunc3()
    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        gauss_integral_infs = sess.run(gauss_integral_infs)
        func3_integrated = sess.run(
            ztf.convert_to_tensor(
                dist_func3.integrate(limits=Range.from_boundaries(*limits3, dims=(0, 1))),
                dtype=tf.float64))
        assert func3_integrated == func3_2deps_fully_integrated(limits=Range.from_boundaries(
            *limits3, dims=(0, 1)))
        assert gauss_integral_infs == pytest.approx(np.sqrt(np.pi * 2.) * sigma_true, rel=0.0001)





def test_analytic_integral_selection():
    class DistFuncInts(zbasepdf.BasePDF):
        def _unnormalized_prob(self, x):
            return x ** 2

    int1 = lambda x: 1
    int2 = lambda x: 2
    int22 = lambda x: 22
    int3 = lambda x: 3
    int4 = lambda x: 4
    int5 = lambda x: 5
    limits1 = (-1, 5)
    dims1 = (1,)
    limits2 = ((None, 5),)
    dims2 = (1,)
    limits3 = ((None, None), (1, 5))
    dims3 = (0, 1)
    limits4 = ((None, None), (0, 5), (None, 42))
    dims4 = (0, 1, 2)
    limits5 = ((None, 10), (1, None))
    dims5 = (1, 2)
    DistFuncInts.register_analytic_integral(int1, limits=limits1, dims=dims1)
    DistFuncInts.register_analytic_integral(int2, limits=limits2, dims=dims2)
    DistFuncInts.register_analytic_integral(int22, limits=limits2, dims=dims2, priority=60)
    DistFuncInts.register_analytic_integral(int3, limits=limits3, dims=dims3)
    DistFuncInts.register_analytic_integral(int4, limits=limits4, dims=dims4)
    DistFuncInts.register_analytic_integral(int5, limits=limits5, dims=dims5)
    dims = DistFuncInts._analytic_integral.get_max_dims(limits=((-5, 4), (1, 5)), dims=dims3)
    assert dims3 == dims