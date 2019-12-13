import numpy as np
import matplotlib.pyplot as plt
import PyOSGPUP.wavelet as wavelet


def getPlotLog(d, log, dmax=200):
    d = np.array(d, dtype=float)
    log = np.array(log, dtype=float)

    dplot = np.kron(d, np.ones(2))
    logplot = np.kron(log, np.ones(2))

    # dplot   = dplot[1:]
    dplot = np.append(dplot[1:], dmax)

    return dplot, logplot


def getImpedance(rholog, vlog):
    """
    Acoustic Impedance is the product of density and velocity
    $$
    Z = \\rho v
    $$
    """
    rholog, vlog = np.array(rholog, dtype=float), np.array(vlog, dtype=float),
    return rholog * vlog


def getReflectivity(d, rho, v, usingT=True):
    """
    The reflection coefficient of an interface is $$ R_i = \\frac{Z_{i+1} - Z_{i}}{Z_{i+1}+Z_{i}} $$ The reflectivity
    can also include the effect of transmission through above layers, in which case the reflectivity is given by $$
    \\text{reflectivity} = R_i \\pi_{j = 1}^{i-1}(1-R_j^2) $$
    """
    Z = getImpedance(rho, v)  # acoustic impedance
    dZ = (Z[1:] - Z[:-1])
    sZ = (Z[:-1] + Z[1:])
    R = dZ / sZ  # reflection coefficients

    nlayer = len(v)  # number of layers

    rseries = R

    if usingT:
        for i in range(nlayer - 1):
            rseries[i + 1:] = rseries[i + 1:] * (1. - R[i] ** 2)

    return rseries, R


def getTimeDepth(d,v,dmax=200):
    """
    The time depth conversion is computed by determining the two-way travel time for a reflection from a given depth.
    """

    d = np.sort(d)
    d = np.append(d,dmax)

    twttop = 2.*np.diff(d)/v    # 2-way travel time within each layer
    twttop = np.append(0.,twttop)
    twttop = np.cumsum(twttop)       # 2-way travel time from surface to top of each layer

    return d, twttop


def getLogs(d, rho, v, usingT=True):
    """
    Function to make plotting convenient
    """
    dpth, rholog = getPlotLog(d, rho)
    _, vlog = getPlotLog(d, v)
    zlog = getImpedance(rholog, vlog)
    rseries, _ = getReflectivity(d, rho, v, usingT)
    return dpth, rholog, vlog, zlog, rseries


def plotLogFormat(log, dpth, xlim, col='blue'):
    """
    Nice formatting for plotting logs as a function of depth
    """
    ax = plt.plot(log, dpth, linewidth=2, color=col)
    plt.xlim(xlim)
    plt.ylim((dpth.min(), dpth.max()))
    plt.grid()
    plt.gca().invert_yaxis()
    plt.setp(plt.xticks()[1], rotation='90', fontsize=9)
    plt.setp(plt.yticks()[1], fontsize=9)

    return ax


def plotLogs(d, rho, v, usingT=True):
    """
    Plotting wrapper to plot density, velocity, acoustic impedance and reflectivity as a function of depth.
    """
    d = np.sort(d)

    dpth, rholog, vlog, zlog, rseries = getLogs(d, rho, v, usingT)
    nd = len(dpth)

    xlimrho = (1.95, 5.05)
    xlimv = (0.25, 4.05)
    xlimz = (xlimrho[0] * xlimv[0], xlimrho[1] * xlimv[1])

    # Plot Density
    plt.figure(1)

    plt.subplot(141)
    plotLogFormat(rholog * 10 ** -3, dpth, xlimrho, 'blue')
    plt.title('$\\rho$')
    plt.xlabel('Density \n $\\times 10^3$ (kg /m$^3$)', fontsize=9)
    plt.ylabel('Depth (m)', fontsize=9)

    plt.subplot(142)
    plotLogFormat(vlog * 10 ** -3, dpth, xlimv, 'red')
    plt.title('$v$')
    plt.xlabel('Velocity \n $\\times 10^3$ (m/s)', fontsize=9)
    plt.setp(plt.yticks()[1], visible=False)

    plt.subplot(143)
    plotLogFormat(zlog * 10. ** -6., dpth, xlimz, 'green')
    plt.gca().set_title('$Z = \\rho v$')
    plt.gca().set_xlabel('Impedance \n $\\times 10^{6}$ (kg m$^{-2}$ s$^{-1}$)', fontsize=9)
    plt.setp(plt.yticks()[1], visible=False)

    plt.subplot(144)
    plt.hlines(d[1:], np.zeros(nd - 1), rseries, linewidth=2)
    plt.plot(np.zeros(nd), dpth, linewidth=2, color='black')
    plt.title('Reflectivity')
    plt.xlim((-1., 1.))
    plt.gca().set_xlabel('Reflectivity')
    plt.grid()
    plt.gca().invert_yaxis()
    plt.setp(plt.xticks()[1], rotation='90', fontsize=9)
    plt.setp(plt.yticks()[1], visible=False)

    plt.tight_layout()
    plt.show()


def plotLogsInteract(d2, d3, rho1, rho2, rho3, v1, v2, v3, usingT=False):
    """
    interactive wrapper of plotLogs
    """
    d = np.array((0., d2, d3), dtype=float)
    rho = np.array((rho1, rho2, rho3), dtype=float)
    v = np.array((v1, v2, v3), dtype=float)
    plotLogs(d, rho, v, usingT)


def plotTimeDepth(d,v):
    """
    Wrapper to plot time-depth conversion based on the provided velocity model
    """

    dpth,t = getTimeDepth(d,v)
    plt.figure()
    plt.plot(dpth,t,linewidth=2)
    plt.title('Depth-Time')
    plt.grid()
    plt.gca().set_xlabel('Depth (m)',fontsize=9)
    plt.gca().set_ylabel('Two Way Time (s)',fontsize=9)

    plt.tight_layout()
    plt.show()


def syntheticSeismogram(d, rho, v, wavf, wavA=1., usingT=True, wavtyp = 'RICKER', dt=0.0001, dmax=200):
    """
    function syntheticSeismogram(d, rho, v, wavtyp, wavf, usingT)
    syntheicSeismogram generates a synthetic seismogram for
    a simple 1-D layered model.
    Inputs:
        d      : depth to the top of each layer (m)
        rho    : density of each layer (kg/m^3)
        v      : velocity of each layer (m/s)
                    The last layer is assumed to be a half-space
        wavf   : wavelet frequency
        wavA   : wavelet amplitude
        usintT : using Transmission coefficients?
        wavtyp : type of Wavelet
                    The wavelet options are:
                        Ricker: takes one frequency
                        Gaussian: still in progress
                        Ormsby: takes 4 frequencies
                        Klauder: takes 2 frequencies
        usingT : use transmission coefficients?
    Lindsey Heagy
    lheagy@eos.ubc.ca
    Created:  November 30, 2013
    Modified: October 3, 2014
    """

    v, rho, d = np.array(v, dtype=float),   np.array(rho, dtype=float), np.array(d, dtype=float)
    usingT    = np.array(usingT, dtype=bool)

    _, t = getTimeDepth(d,v,dmax)
    rseries,R = getReflectivity(d,rho,v)

    # time for reflectivity series
    tref   = t[1:-1]

    # create time vector
    t = np.arange(t.min(),t.max(),dt)

    # make wavelet
    twav   = np.arange(-2.0/np.min(wavf), 2.0/np.min(wavf), dt)

    # Get source wavelet
    wav = {'RICKER':wavelet.getRicker, 'ORMSBY':wavelet.getOrmsby, 'KLAUDER':wavelet.getKlauder}[wavtyp](wavf,twav)
    wav = wavA*wav

    rseriesconv = np.zeros(len(t))
    for i in range(len(tref)):
         index = np.abs(t - tref[i]).argmin()
         rseriesconv[index] = rseries[i]

    # Do the convolution
    seis  = np.convolve(wav,rseriesconv)
    tseis = np.min(twav)+dt*np.arange(len(seis))
    index = np.logical_and(tseis >= 0, tseis <= np.max(t))
    tseis = tseis[index]
    seis  = seis[index]

    return tseis, seis, twav, wav, tref, rseries


def plotSeismogram(d, rho, v, wavf, wavA=1., noise = 0., usingT=True, wavtyp='RICKER'):
    """
    Plotting function to show physical property logs (in depth) and seismogram (in time).
    """

    dpth, rholog, vlog, zlog, rseries  = getLogs(d, rho, v, usingT)
    tseis, seis, twav, wav, tref, rseriesconv = syntheticSeismogram(d, rho, v, wavf, wavA, usingT,wavtyp)

    noise  = noise*np.max(np.abs(seis))*np.random.randn(seis.size)
    filt   = np.arange(1.,21.)
    filtr  = filt[::-1]
    filt   = np.append(filt,filtr[1:])*1./21.
    noise  = np.convolve(noise,filt)
    noise  = noise[0:seis.size]

    xlimrho = (1.95,5.05)
    xlimv   = (0.25,4.05)
    xlimz   = (xlimrho[0]*xlimv[0], xlimrho[1]*xlimv[1])

    seis = seis + noise

    plt.figure()

    plt.subplot(131)
    plotLogFormat(rholog*10**-3,dpth,xlimrho,'blue')
    plt.title('$\\rho$')
    plt.xlabel('Density \n $\\times 10^3$ (kg /m$^3$)',fontsize=9)
    plt.ylabel('Depth (m)',fontsize=9)

    plt.subplot(132)
    plotLogFormat(vlog*10**-3,dpth,xlimv,'red')
    plt.title('$v$')
    plt.xlabel('Velocity \n $\\times 10^3$ (m/s)',fontsize=9)
    plt.ylabel('Depth (m)',fontsize=9)

    plt.subplot(133)
    plt.plot(seis,tseis,color='black',linewidth=1)
    plt.title('Seismogram')
    plt.grid()
    plt.ylim((tseis.min(),tseis.max()))
    plt.gca().invert_yaxis()
    plt.xlim((-0.5,0.5))
    plt.setp(plt.xticks()[1],rotation='90',fontsize=9)
    plt.setp(plt.yticks()[1],fontsize=9)
    plt.gca().set_xlabel('Amplitude',fontsize=9)
    plt.gca().set_ylabel('Time (s)',fontsize=9)

    plt.tight_layout()
    plt.show()