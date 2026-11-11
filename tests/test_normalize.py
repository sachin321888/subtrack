import pytest

from subtrack.normalize import normalize_merchant


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("NETFLIX.COM 8007", "Netflix"),
        ("NETFLIX.COM 8011", "Netflix"),
        ("SPOTIFY INDIA", "Spotify"),
        ("SWIGGY ORDER 4412", "Swiggy"),
    ],
)
def test_normalize_merchant(raw, expected):
    assert normalize_merchant(raw) == expected