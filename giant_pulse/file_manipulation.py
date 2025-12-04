import numpy as np
import astropy.units as u
from baseband import guppi
from baseband_tasks.combining import Concatenate
from baseband_tasks import dm
from baseband_tasks.base import SetAttribute
from baseband_tasks.functions import Square
from baseband_tasks.integration import Integrate
from baseband_tasks.dispersion import DedisperseSamples, Dedisperse

__all__ = ['combine_files_freq']

def combine_files_freq(file_names, samples_per_frame=1024, axis=2):
    """Reads in multiple baseband files and combines them along 
    the frequency axis. Additionally defines the associated frequency
    channels.

    Parameters
    ----------
    file_names : list of str
        List of file paths to the baseband files to combine.

    samples_per_frame : int, optional
        Number of samples per frame for the combined file. Default is 1024.

    axis : int, optional
        Axis along which to combine the files. Should be the frequency axis.
        Default is 2.

    Returns
    -------
    combined : str
        File path to the combined baseband file.
    """

    fs = [guppi.open(filename) for filename in file_names]

    base_freqs = [f.header0["OBSFREQ"] * u.MHz for f in fs]
    chan_bw = fs[0].header0["CHAN_BW"] * u.MHz
    n_chans = fs[0].header0["OBSNCHAN"]
    # band_size = chan_bw * n_chans
    # total_chans = n_chans * len(fs)

    freqs = np.array([base_freq + np.linspace(0, n_chans-1, n_chans) * chan_bw for base_freq in base_freqs])
    freqs = np.reshape(freqs, freqs.shape[0]*freqs.shape[1])
    freqs = freqs * u.MHz

    # base_freq = fs[0].header0["OBSFREQ"] * u.MHz
    # chan_bw = fs[0].header0["CHAN_BW"] * u.MHz
    # n_chans = fs[0].header0["OBSNCHAN"]
    # band_size = chan_bw * n_chans
    # total_chans = n_chans * len(fs)
    # freqs = base_freq + np.linspace(0, total_chans - 1, total_chans) * chan_bw

    fs = [SetAttribute(f, samples_per_frame=samples_per_frame) for f in fs]

    combined = Concatenate(fs, axis=axis)
    combined = SetAttribute(combined, frequency=freqs, sideband=1)

    # for f in fs:
    #     f.close()

    return combined
