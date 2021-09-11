import pytest

from pypette import BashJob


def test_function_validation() -> None:
    """Tests the function validation mechanism."""
    with pytest.raises(AssertionError):
        BashJob(1)  # type: ignore
    with pytest.raises(AssertionError):
        BashJob('test')  # type: ignore


def test_string_representation() -> None:
    """Tests printable representation of BashJobs."""
    assert 'BashJob(cmd=ls -l)' == BashJob(['ls', '-l']).__repr__()
    assert 'BashJob(cmd=pwd)' == BashJob(['pwd']).__repr__()


def test_equality() -> None:
    """Validates equality of bash jobs."""
    assert BashJob(['ls']) == BashJob(['ls'])
    assert BashJob(['ls -l']) == BashJob(['ls -l'])
    assert BashJob(['pwd']) != BashJob(['ls'])
