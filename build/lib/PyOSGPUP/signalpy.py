
import numpy as np
from numpy.fft.fftpack import fft,ifft

def hilbert(mag):
    """Compute the modified 1D discrete Hilbert transform

    Parameters
    ----------
    mag : ndarray
        The magnitude spectrum. Should be 1D with an even length, and
        preferably a fast length for FFT/IFFT.
    """
    # Adapted based on code by Niranjan Damera-Venkata,
    # Brian L. Evans and Shawn R. McCaslin (see refs for `minimum_phase`)
    sig = np.zeros(len(mag))
    # Leave Nyquist and DC at 0, knowing np.abs(fftfreq(N)[midpt]) == 0.5
    midpt = len(mag) // 2
    sig[1:midpt] = 1
    sig[midpt+1:] = -1
    # eventually if we want to support complex filters, we will need a
    # np.abs() on the mag inside the log, and should remove the .real
    recon = ifft(mag * np.exp(fft(sig * ifft(np.log(mag))))).real
    return recon

