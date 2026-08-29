from evals.wilson import wilson_ci


def test_wilson_ci_known_bounds():
    p, low, high = wilson_ci(0, 10)
    assert p == 0.0
    assert low == 0.0
    assert 0 < high < 1

    p, low, high = wilson_ci(10, 10)
    assert p == 1.0
    assert 0 < low < 1
    assert high == 1.0

    assert wilson_ci(0, 0) == (0.0, 0.0, 0.0)
