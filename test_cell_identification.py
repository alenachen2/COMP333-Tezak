import numpy as np
from cell_identification import split_channels, clean, normalize, extract_ROI


def test_split_channels():
    """
    split_channels should correctly return (b, g, r) channels.
    """
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    img[:, :, 0] = 50   # blue
    img[:, :, 1] = 100  # green
    img[:, :, 2] = 150  # red

    b, g, r = split_channels(img)

    assert np.all(b == 50)
    assert np.all(g == 100)
    assert np.all(r == 150)


def test_normalize():
    """
    normalize should scale image values between 0–255.
    """
    img = np.array([[10, 20], [30, 40]], dtype=np.uint8)
    norm = normalize(img)

    assert norm.min() == 0
    assert norm.max() == 255


def test_clean():
    """
    clean should return three cleaned + normalized channels.
    """
    r = np.full((5, 5), 200, dtype=np.uint8)
    g = np.full((5, 5), 50, dtype=np.uint8)
    b = np.full((5, 5), 10, dtype=np.uint8)

    cleaned = clean(r, g, b)

    assert len(cleaned) == 3
    for channel in cleaned:
        assert channel.dtype == np.uint8
        assert channel.shape == (5, 5)


def test_extract_ROI_red():
    """
    extract_ROI('red') should return unique labels from masks[0].
    """
    masks = [
        np.array([[0, 1, 1], [2, 2, 2]]),
        np.zeros((2, 3)),
        np.zeros((2, 3)),
    ]

    rois = extract_ROI("red", masks)
    assert np.array_equal(rois, np.array([0, 1, 2]))


def test_extract_ROI_blue():
    """
    extract_ROI('blue') should return unique labels from masks[2].
    """
    masks = [
        np.zeros((2, 3)),
        np.zeros((2, 3)),
        np.array([[0, 5, 5], [7, 7, 0]]),
    ]

    rois = extract_ROI("blue", masks)
    assert np.array_equal(rois, np.array([0, 5, 7]))
