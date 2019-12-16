# PyOSGPUP

[![GitHub version](https://badge.fury.io/gh/Metkom%2FPyOSGPUP.svg)](https://badge.fury.io/gh/Metkom%2FPyOSGPUP)
[![Build Status](https://travis-ci.org/dwyl/esta.svg?branch=master)](https://travis-ci.org/Metkom/PyOSGPUP)
![GitHub top language](https://img.shields.io/github/languages/top/Metkom/PyOSGPUP.svg)
[![PyPI version](https://badge.fury.io/py/PyOSGPUP.svg)](https://badge.fury.io/py/PyOSGPUP)
[![PyPI license](https://img.shields.io/pypi/l/PyOSGPUP.svg)](https://pypi.python.org/pypi/PyOSGPUP/)
![PyPI - Status](https://img.shields.io/pypi/status/PyOSGPUP.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/PyOSGPUP)

[![Inline docs](http://inch-ci.org/github/dwyl/hapi-auth-jwt2.svg?branch=master)](http://inch-ci.org/mheriyanto/PyOSGPUP/hapi-auth-jwt2)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Metkom/PyOSGPUP/issues)
![GitHub contributors](https://img.shields.io/github/contributors/Metkom/PyOSGPUP.svg)

[![HitCount](http://hits.dwyl.com/Metkom/PyOSGPUP.svg)](http://hits.dwyl.com/Metkom/PyOSGPUP)
[![PyPI download month](https://img.shields.io/pypi/dm/PyOSGPUP.svg)](https://pypi.python.org/pypi/PyOSGPUP/)
![GitHub All Releases](https://img.shields.io/github/downloads/Metkom/PyOSGPUP/total.svg)
![GitHub forks](https://img.shields.io/github/forks/Metkom/PyOSGPUP.svg?style=social)

![GitHub last commit](https://img.shields.io/github/last-commit/Metkom/PyOSGPUP.svg)
![GitHub Release Date](https://img.shields.io/github/release-date/Metkom/PyOSGPUP.svg)


A python packages for geophysical data processing modeling, inversion and interpretation. Please check here: for [official website](https://sites.google.com/site/metkomup/pyosgpup) and [package](https://pypi.org/project/PyOSGPUP/).

Teknik Geofisika, Universitas Pertamina Jl. Teuku Nyak Arief, Simprug, South Jakarta, DKI Jakarta, Indonesia, 12220. email: metkom.up@gmail.com

## Installation

```
pip install PyOSGPUP
or
pip3 install PyOSGPUP
```
## User Manual
User manual for this package avalaible in Bahasa ([download](https://figshare.com/articles/Petunjuk_Penggunaan_PyOSGPUP_versi_1_0_3/7325723)). Short example:

1. Create wavelet
```python
import numpy as np
import PyOSGPUP.wavelet as wav
import matplotlib.pyplot as plt

t = np.arange(-0.4 / 2, (0.4 / 2) + 0.004, 0.004)
# frequency
fgR = np.array([10])  # 1 freq
fgO = np.array([5, 10, 15, 20])  # 4 fred
fgK = np.array([5, 10])  # 2 fred
gR = wav.getRicker(fgR, t)
gO = wav.getOrmsby(fgO, t)
gK = wav.getKlauder(fgK, t)

plt.figure()
plt.plot(t, gR, linewidth=2, color="blue")
plt.plot(t, gO, linewidth=2, color="red")
plt.plot(t, gK, linewidth=2, color="green")
plt.title('Wavelet')
plt.xlabel('time [ms]')
plt.ylabel('amplitude')
plt.legend(['Ricker', 'Ormsby', 'Kaluder'])
plt.show()
```


