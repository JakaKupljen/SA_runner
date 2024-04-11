import numpy as np
from naloga2 import konvolucija


def test_konvolucija():
    # Manjsa slika
    slika = np.ones((3, 3, 3), dtype=np.uint8) * 10
    jedro = np.array([[1, 0, 1],
                      [0, 1, 0],
                      [1, 0, 1]], dtype=np.float32)
    rezultat = konvolucija(slika, jedro)
    assert rezultat.shape == (3, 3, 3)

    # Vecja slika
    slika = np.ones((10, 10, 3), dtype=np.uint8) * 10
    jedro = np.ones((3, 3), dtype=np.float32)
    rezultat = konvolucija(slika, jedro)
    assert rezultat.shape == (10, 10, 3)

if __name__ == "__main__":
    try:
        test_konvolucija()
        print("Success")
    except AssertionError:
        print("Test failed")
