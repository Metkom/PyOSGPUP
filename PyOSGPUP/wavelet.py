# Ref: https://gist.github.com/rowanc1/8338665
import numpy as np
pi = np.pi


def getRicker(f, t):
    #assert len(f) == 1, 'Ricker wavelet needs 1 frequency as input'
    # f = f[0]
    pift = pi * f * t
    wav = (1 - 2 * pift ** 2) * np.exp(-pift ** 2)
    return wav


def getOrmsby(f, t):
    assert len(f) == 4, 'Ormsby wavelet needs 4 frequencies as input'
    f = np.sort(f)  # Ormsby wavelet frequencies must be in increasing order
    pif = pi * f
    den1 = pif[3] - pif[2]
    den2 = pif[1] - pif[0]
    term1 = (pif[3] * np.sinc(pif[3] * t)) ** 2 - (pif[2] * np.sinc(pif[2])) ** 2
    term2 = (pif[1] * np.sinc(pif[1] * t)) ** 2 - (pif[0] * np.sinc(pif[0])) ** 2

    wav = term1 / den1 - term2 / den2
    return wav


def getKlauder(f, t, T=5.0):
    assert len(f) == 2, 'Klauder wavelet needs 2 frequencies as input'

    k = np.diff(f) / T
    f0 = np.sum(f) / 2.0
    wav = np.real(np.sin(pi * k * t * (T - t)) / (pi * k * t) * np.exp(2 * pi * 1j * f0 * t))
    return wav
