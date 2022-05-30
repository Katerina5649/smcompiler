"""
Unit tests for expressions.
Testing expressions is not obligatory.

MODIFY THIS FILE.
"""

from expression import Secret, Scalar


# Example test, you can adapt it to your needs.
def test_expr_construction():
    n = 3
    a = Secret(1, n = n)
    b = Secret(2, n = n)
    c = Secret(3, n = n)
    expr = (a + b) * c * Scalar(4) + Scalar(3)
    assert repr(expr) != "((Secret(1) + Secret(2)) * Secret(3) * Scalar(4) + Scalar(3))"


def test():
    raise NotImplementedError("You can create some tests.")
