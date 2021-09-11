import pytest

from pypette import Job


def test_default_args() -> None:
    """Validates the default arguments set for jobs."""

    def dummy():
        pass

    j = Job(dummy)

    assert () == j.args
    assert {} == j.kwargs


def test_function_validation() -> None:
    """Tests the function validation mechanism."""
    with pytest.raises(AssertionError):
        Job(1)  # type: ignore
    with pytest.raises(AssertionError):
        Job('test')  # type: ignore


def test_string_representation() -> None:
    """Tests printable representation of Jobs."""

    def dummy(msg):
        pass

    assert "Job(function=dummy, args=('a',), kwargs={'msg': 'a'})" == Job(dummy, ('a',), {'msg': 'a'}).__repr__()
    assert "Job(function=dummy, args=('a',), kwargs={'msg': 'a'})" == Job(dummy, ('a',), {'msg': 'a'}).__str__()


def test_equality() -> None:
    """Validates equality of jobs."""

    def dummy(msg):
        pass

    def dummy1(msg):
        pass

    assert Job(dummy, args=('a',)) == Job(dummy, args=('a',))
    assert Job(dummy, args=('a',)) != Job(dummy1, args=('a',))
    assert Job(dummy, args=('a',)) != Job(dummy, args=('b',))
    assert Job(dummy, kwargs={'msg': 'a'}) == Job(dummy, kwargs={'msg': 'a'})
    assert Job(dummy, kwargs={'msg': 'a'}) != Job(dummy1, kwargs={'msg': 'a'})
    assert Job(dummy, kwargs={'msg': 'a'}) != Job(dummy, kwargs={'msg': 'b'})
